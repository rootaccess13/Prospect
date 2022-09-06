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
def pre_social_login(sender, request, sociallogin, **kwargs):
    # Get email from sociallogin
    email = sociallogin.account.extra_data.get('email')
    # Get user model
    User = get_user_model()
    # Check if user exists
    try:
        user = User.objects.get(email=email)
        # If user exists, perform login
        perform_login(request, user, email_verification='none')
        # Redirect to home page
        raise ImmediateHttpResponse(redirect('/'))
    except User.DoesNotExist:
        # If user doesn't exist, redirect to signup page
        raise ImmediateHttpResponse(
            redirect(settings.LOGIN_REDIRECT_URL, pk=request.user.pk))
