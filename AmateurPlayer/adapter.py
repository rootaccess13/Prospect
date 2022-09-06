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


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login to 
    perform some actions right after successful login
    '''

    def pre_social_login(self, request, sociallogin):
        # check if user is already had an account
        if sociallogin.is_existing:
            print("Existing User : " + str(sociallogin.user.email))
        else:
            print("New User : " + str(sociallogin.user.email))
        return super().pre_social_login(request, sociallogin)


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    ''' Login and redirect
    This is done in order to tackle the situation where user's email retrieved
    from one provider is different from already existing email in the database
    (e.g facebook and google both use same email-id). Specifically, this is done to
    tackle following issues:
    * https://github.com/pennersr/django-allauth/issues/215

    '''
    # get user model
    user_model = get_user_model()
    # get email from sociallogin
    email = sociallogin.account.extra_data.get('email')
    # get user with this email
    user = user_model.objects.filter(email=email).first()
    # if user exists
    if user:
        # login user
        perform_login(request, user, email_verification='none')
        # redirect to home
        raise ImmediateHttpResponse(
            redirect('completeinfo', pk=request.user.pk))
    # if user does not exist
    else:
        # log error message

        # redirect to signup page
        raise ImmediateHttpResponse(redirect('/'))


@receiver(user_signed_up)
def user_signed_up(self, request, user, sociallogin=None, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == 'facebook':
            user.ign = sociallogin.account.extra_data['name']
            user.email = sociallogin.account.extra_data['email']
            user.save()
        elif sociallogin.account.provider == 'google':
            user.ign = sociallogin.account.extra_data['name']
            user.email = sociallogin.account.extra_data['email']
            user.save()
