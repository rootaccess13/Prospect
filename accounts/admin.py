from django.contrib import admin
from .models import CustomUser, ProfileHighlights, ReviewUser

admin.site.register(CustomUser)
admin.site.register(ProfileHighlights)
admin.site.register(ReviewUser)
