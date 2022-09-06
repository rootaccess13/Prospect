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

    def pre_social_login(self, request, sociallogin):
        if sociallogin.account.provider == 'google':
            # get user model
            User = get_user_model()
            # get user email
            email = sociallogin.account.extra_data['email']
            # get user by email
            user = User.objects.filter(email=email).first()
            # check if user is already had an account
            if user:
                # login user
                perform_login(request, user, email_verification='optional')
                # redirect to home page
                raise ImmediateHttpResponse(redirect('/'))
        if sociallogin.account.provider == 'facebook':
            # get user model
            User = get_user_model()
            # get user email
            email = sociallogin.account.extra_data['email']
            # get user by email
            user = User.objects.filter(email=email).first()
            # check if user is already had an account
            if user:
                # login user
                perform_login(request, user, email_verification='optional')
                # redirect to home page
                raise ImmediateHttpResponse(redirect('/'))

    def populate_user(self, request, sociallogin, data):
        # get user model
        User = get_user_model()
        # get user email
        email = sociallogin.account.extra_data['email']
        # get user by email
        user = User.objects.filter(email=email).first()
        # check if user is already had an account
        if user:
            # set user
            sociallogin.connect(request, user)
            # redirect to home page
            raise ImmediateHttpResponse(redirect('/'))

    def save_user(self, request, sociallogin, form=None):
        # get user model
        User = get_user_model()
        # get user email
        email = sociallogin.account.extra_data['email']
        # get user by email
        user = User.objects.filter(email=email).first()
        # check if user is already had an account
        if user:
            # set user
            sociallogin.connect(request, user)
            # redirect to home page
            raise ImmediateHttpResponse(redirect('/'))


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
