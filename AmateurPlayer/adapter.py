import email
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
import json
from allauth.account.signals import user_signed_up


class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        path = "/info/{pk}/"
        # check if user is already had an account
        if request.user.is_authenticated:
            path = path.format(pk=request.user.pk)
        return path.format(pk=request.user.pk)

    def get_login_redirect_url(self, request):
        path = "/"
        print("Signed In : " + request.user.ign)
        return path

    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(
            request, user, form, commit=False)
        user.ign = form.cleaned_data.get('ign')
        user.save()
        return user


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login to 
    perform some actions right after successful login
    '''

    def pre_social_login(self, request, sociallogin):

        if get_user_model().objects.filter(email=sociallogin.user.email).exists():
            user = get_user_model().objects.get(email=sociallogin.user.email)
            perform_login(request, user, email_verification='optional')
            raise ImmediateHttpResponse(redirect('/'))
        else:
            # if user is new, create an account
            user = sociallogin.user
            user.ign = sociallogin.account.extra_data['name']
            user.save()
            perform_login(request, user, email_verification='optional')
            raise ImmediateHttpResponse(
                redirect('/info/{pk}/'.format(pk=user.pk)))

#     def save_user(self, request, sociallogin, form=None):
#         user = super(MySocialAccountAdapter, self).save_user(
#             request, sociallogin, form=None)
#         user.ign = sociallogin.account.extra_data['name']
#         user.save()
#         return super().save_user(request, sociallogin, form)


# @receiver(user_signed_up)
# def retrieve_social_data(sender, request, sociallogin, **kwargs):
#     if sociallogin.account.provider == 'facebook':
#         email = sociallogin.account.extra_data['email']
#         first_name = sociallogin.account.extra_data['first_name']
#         last_name = sociallogin.account.extra_data['last_name']
#         sociallogin.user.email = email
#         print("Email : " + email)
#         print("First Name : " + first_name)
#         print("Last Name : " + last_name)
