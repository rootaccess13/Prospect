from django.urls import path
from . views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('info/user/<slug:slug>/', UserDetailView.as_view(), name='userinfo'),
    path('info/<str:pk>/', CompleteInfoView.as_view(), name='completeinfo'),
    path('logout/', logout_view, name='logout'),
    path('<slug:slug>/review/add/',
         CreateReviewView.as_view(), name='create_review'),
    path('follow/<str:loggedinuser>/<str:pk>/',
         UserFollowView.as_view(), name='followtoggle'),
    path('activate/<slug:uidb64>/<slug:token>/',
         SignUpActivateView.as_view(), name='activate'),
]
