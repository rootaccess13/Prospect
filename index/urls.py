from django.urls import path
from . views import *


urlpatterns = [
    path('', signup, name='index'),
    path('signin/', signin, name='signin'),
    path('info/<str:pk>/', completeProfile, name='completeinfo'),
    path('logout/', logout_view, name='logout'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('<slug:slug>/', UserDetailView.as_view(), name='userinfo'),
    path('followtoggle/<str:pk>/', followToggle, name='followtoggle'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
