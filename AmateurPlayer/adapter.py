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

    def new_user(self, request, sociallogin):
        user = super(MySocialAccountAdapter, self).new_user(
            request, sociallogin)
        user.ign = sociallogin.account.extra_data['name']
        user.save()
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super(MySocialAccountAdapter, self).save_user(
            request, sociallogin, form)
        user.ign = sociallogin.account.extra_data['name']
        user.save()
        return super().save_user(request, sociallogin, form)

    def pre_social_login(self, request, sociallogin):
        print("Signed In : " + sociallogin.account.extra_data['name'])
        return super(MySocialAccountAdapter, self).pre_social_login(request, sociallogin)

    def get_login_redirect_url(self, request):
        path = "/"
        print("Signed In : " + request.user.ign)
        return path
