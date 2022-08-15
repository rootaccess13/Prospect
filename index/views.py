from decimal import Context
from itertools import count
from multiprocessing import context
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
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.conf import settings
from accounts.models import CustomUser
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from accounts.forms import AvatarForm
from django.conf import settings


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
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'index/index.html', {'form': form, 'userdata': userdataobjects})


def signin(request):
    # Get CustomUser object except for staff users
    userdata = CustomUser.objects.exclude(is_staff=True)
    # get 10 objects from CustomUser object
    userdataobjects = userdata[:10]
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('index')
    context = {
        'userdata': userdataobjects,
        'COMPRESS_ROOT': settings.COMPRESS_ROOT,
    }
    return render(request, 'index/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


class UserDetailView(HitCountDetailView, View):
    model = CustomUser
    template_name = 'accounts/profile_view.html'
    context_object_name = 'userinfos'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    # def get_context_data(self, **kwargs):
    #     context = super(UserDetailView, self).get_context_data(**kwargs)
    #     context.update({
    #         'popular_posts': CustomUser.objects.order_by('-hit_count_generic__hits')[:3],
    #     })
    #     return context


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
def completeProfile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        avatarform = AvatarForm(request.POST or None,
                                request.FILES or None, instance=user)
        if avatarform.is_valid():
            user.gamerole = request.POST['gamerole']
            user.gametype = request.POST['gametype']
            user.formerteam = request.POST['formerteam']
            user.save()
            avatarform.save()
            return redirect('index')
    else:
        avatarform = AvatarForm(instance=user)
    return render(request, 'accounts/complete_profile.html', {'avatarForm': avatarform, 'user': user})


def success(request):
    return render(request, 'accounts/success.html')


def logout_view(request):
    logout(request)
    return redirect('index')
