from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail
# from . tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth.decorators import login_required as lr
from django.utils import timezone
from accounts.forms import SignUpForm
from accounts.tokens import account_activation_token
from django.urls import reverse
from django.conf import settings
from accounts.models import CustomUser, ProfileHighlights, ReviewUser
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from accounts.forms import AvatarForm
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.template.defaulttags import register
from django.views.decorators.http import require_http_methods


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


def signup(request):
    # Get CustomUser object except for staff users
    userdata = CustomUser.objects.exclude(is_staff=True)
    # get 10 objects from CustomUser object
    userdataobjects = userdata[:10]
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            rememberuser = form.cleaned_data.get('remember')
            if not rememberuser:
                request.session.set_expiry(0)
                request.session.modified = True
                print(request.session.get_expiry_date())
            user = form.save(commit=False)
            user.is_active = False
            if not rememberuser:
                user.rememberuser = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'

            message = render_to_string('accounts/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            messages.add_message(
                request, messages.SUCCESS, 'Account created successfully. Please check your email to activate your account.')
            return redirect('index')
        else:
            # raise form messages
            messages.add_message(request, messages.ERROR,
                                 'Sign up failed, please try again.')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'index/index.html', {'form': form, 'userdata': userdataobjects})


@require_http_methods(["GET", "POST"])
def signin(request):
    userdata = CustomUser.objects.exclude(is_staff=True)
    userdataobjects = userdata[:10]
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully logged in.')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Sign in failed, invalid email or password.')
            return redirect('index')
    context = {
        'userdata': userdataobjects,
        'COMPRESS_ROOT': settings.COMPRESS_ROOT,
    }
    return render(request, 'index/index.html', context)


@require_http_methods(["GET", "POST"])
def followToggle(request, pk, loggedinuser):
    user = CustomUser.objects.get(pk=pk)
    if request.user in user.follower.all():
        user.follower.remove(request.user)
        messages.add_message(request, messages.SUCCESS,
                             'You unfollowed ' + user.ign + '.')
    else:
        user.follower.add(request.user)
        messages.add_message(request, messages.SUCCESS,
                             'You followed ' + user.ign + '.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def oauthtiktok(request):
    # Math.random().toString(36).substring(2)
    csrf_state = request.GET.get('csrfmiddlewaretoken')
    params = {
        'client_key': 'awf17r3fssnrj8za',
        'redirect_uri': 'https://samateurprospect.herokuapp.com/',
        'response_type': 'code',
        'scope': 'user.info.basic',
        'state': csrf_state,
    }
    url = 'https://tiktok.com/oauth/authorize?client_key={client_key}&redirect_uri={redirect_uri}&response_type={response_type}&scope={scope}&state={state}'.format(
        **params)
    print(url)
    return redirect(url)


def logout_view(request):
    logout(request)
    return redirect('index')


class UserDetailView(LoginRequiredMixin, HitCountDetailView, View):
    model = CustomUser
    template_name = 'accounts/profile_view.html'
    context_object_name = 'userinfos'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_highlights'] = ProfileHighlights.objects.filter(
            user=self.object)
        context['reviewuserdata'] = ReviewUser.objects.filter(
            user=self.object).order_by('-date')
        context['review_count'] = ReviewUser.objects.filter(
            user=self.object).count()
        context['following_count'] = self.object.follower.count()
        context['follower_count'] = self.object.following.count()

        return context

        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        highlight = request.POST['highlight']
        if highlight and 'youtube' in highlight:
            ProfileHighlights.objects.create(
                user=user, highlight=highlight)
            messages.add_message(request, messages.SUCCESS,
                                 'Highlight added successfully.')
            return redirect('userinfo', user.slug)
        else:
            messages.add_message(request, messages.ERROR,
                                 'Highlights upload failed, invalid url. Please try again.')
        return redirect('userinfo', user.slug)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 'You need to be logged in to view this page.')
        return super().dispatch(request, *args, **kwargs)


@lr
@require_http_methods(["POST"])
def create_review(request, slug):
    user = CustomUser.objects.get(slug=slug)
    review = request.POST['reviews']

    if review:
        ReviewUser.objects.create(
            user=user, author=request.user.ign, review=review, avatar=request.user.avatar)

        messages.add_message(request, messages.SUCCESS,
                             'Review added successfully.')
        return redirect('userinfo', user.slug)
    else:
        messages.add_message(request, messages.ERROR,
                             'Review upload failed, invalid url. Please try again.')
    return redirect('userinfo', user.slug)


def activation_sent_view(request):
    return render(request, 'accounts/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.signup_confirmation = True
        user.last_login = timezone.now()
        user.save()
        login(request, user)

        return redirect('completeinfo', pk=user.pk)
    else:
        return render(request, 'accounts/activation_invalid.html')


@lr
@require_http_methods(["GET", "POST"])
def completeProfile(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.gamerole = request.POST['gamerole']
            user.gametype = request.POST['gametype']
            user.formerteam = request.POST['formerteam']
            user.save()
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Profile updated successfully.')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('completeinfo', pk=user.pk)
    else:
        form = AvatarForm(instance=user)
    return render(request, 'accounts/complete_profile.html', {'form': form, 'user': user})


def success(request):
    return render(request, 'accounts/success.html')


def logout_view(request):
    logout(request)
    return redirect('index')
