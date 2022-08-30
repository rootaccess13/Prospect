from django.contrib import admin
from .models import CustomUser, ProfileHighlights, ReviewUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'ign', 'slug', 'avatar', 'gametype',
                    'gamerole', 'formerteam',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('email', 'ign', 'slug')


@admin.register(ProfileHighlights)
class ProfileHighlightsAdmin(admin.ModelAdmin):
    list_display = ('user', 'highlight')
    search_fields = ('user', 'highlight')


@admin.register(ReviewUser)
class ReviewUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'review', 'avatar')
    search_fields = ('user', 'author', 'review', 'avatar')
