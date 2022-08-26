from django.urls import path
from . views import *


urlpatterns = [
    path('', signup, name='index'),
    path('signin/', signin, name='signin'),
    path('info/<str:pk>/', completeProfile, name='completeinfo'),
    path('logout/', logout_view, name='logout'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('oauthtiktok/', oauthtiktok, name='oauthtiktok'),
    path('<slug:slug>/', UserDetailView.as_view(), name='userinfo'),
    path('<slug:slug>/review/add/', create_review, name='create_review'),
    path('follow/<str:loggedinuser>/<str:pk>/',
         followToggle, name='followtoggle'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
