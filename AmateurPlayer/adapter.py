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
    # Handle facebook login
    if sociallogin.account.provider == 'facebook':
        # get user data from facebook
        extra_data = sociallogin.account.extra_data
        # get facebook id
        facebook_id = extra_data['id']
        # get facebook email
        facebook_email = extra_data['email']
        print("Facebook ID : " + facebook_id)
        print("Facebook Email : " + facebook_email)
        # get facebook name
        facebook_name = extra_data['name']
        # get facebook picture
        facebook_picture = extra_data['picture']['data']['url']
