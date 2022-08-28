from django.shortcuts import render, redirect


def index(request):
    return render(request, 'accounts/account_setting.html')
