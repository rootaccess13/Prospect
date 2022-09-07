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
        # get the user model
        user_model = get_user_model()
        # get the user from the social login
        user = sociallogin.user
        print("Social Login : " + str(user))
        # check if the user is already in the database
        if user_model.objects.filter(email=user.email).exists():
            # if the user is already in the database, just login
            user = user_model.objects.get(email=user.email)
            perform_login(request, user, email_verification='optional')
            raise ImmediateHttpResponse(redirect('/'))
        else:
            # if the user is not in the database, create a new user
            # user_model.objects.create_user(
            #     email=sociallogin.,
            #     ign=user.email.split('@')[0],
            #     password=user_model.objects.make_random_password(),
            # )
            # # login the new user
            # user = user_model.objects.get(email=user.email)
            # perform_login(request, user, email_verification='optional')
            # raise ImmediateHttpResponse(
            #     redirect('/info/{pk}/'.format(pk=user.pk)))
            user.ign = user.email.split('@')[0]
            user.email = user.email
            user.save()
            perform_login(request, user, email_verification='optional')
            raise ImmediateHttpResponse(
                redirect('/info/{pk}/'.format(pk=user.pk)))

    def user_signed_up(self, request, user):
        print("User Signed Up : " + str(user))
        user.ign = user.email.split('@')[0]
        user.email = user.email
        user.save()


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    ''' Login and redirect
    This is done in order to tackle the situation where user's email retrieved
    from one provider is different from already existing email in the database
    (e.g facebook and google both use same email-id). Specifically, this is done to
    tackle following issues:
    * https://github.com/pennersr/django-allauth/issues/215

    '''
    email_address = sociallogin.account.extra_data['email']
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(
            redirect(settings.LOGIN_REDIRECT_URL.format(pk=users[0].pk)))


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    print("User Signed Up : " + str(user))
    user.ign = user.email.split('@')[0]
    user.email = user.email
    user.save()
