from django.db.models import fields
from rest_framework import serializers
from . models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'ign', 'slug', 'avatar', 'gametype', 'gamerole', 'formerteam',
                  'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
        read_only_fields = ('slug',)


class ProfileHighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileHighlights
        fields = ('user', 'highlight')
        read_only_fields = ('user',)


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewUser
        fields = ('user', 'author', 'review', 'avatar')
        read_only_fields = ('user',)
