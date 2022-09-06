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

    def pre_social_login(self, request, sociallogin):
        # check if user is already had an account
        if request.user.is_authenticated:
            sociallogin.connect(request, request.user)
            raise ImmediateHttpResponse(
                redirect("/info/{pk}/".format(pk=request.user.pk)))

        return super().pre_social_login(request, sociallogin)

    def get_connect_redirect_url(self, request, socialaccount):
        path = "/info/{pk}/"
        # check if user is already had an account
        if request.user.is_authenticated:
            path = path.format(pk=request.user.pk)
        return path.format(pk=request.user.pk)

    def get_login_redirect_url(self, request):
        path = "/"
        print("Signed In : " + request.user.ign)
        return path

    def populate_user(self, request, sociallogin, data):
        user = sociallogin.user
        if user.email:
            return
        email = data.get('email')
        if email:
            user.email = email
            return
        user.email = data.get('username') + '@gmail.com'

        return super().populate_user(request, sociallogin, data)


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    print("Signed Up : " + user.ign)

    return redirect("/info/{pk}/".format(pk=user.pk))
