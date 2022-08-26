from django.urls import path
from . views import *


urlpatterns = [
    path('review/', CreateReview.as_view()),
]
