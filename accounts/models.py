from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    ign = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    gametype = models.CharField(max_length=50, blank=True, null=True)
    gamerole = models.CharField(max_length=50, blank=True, null=True)
    formerteam = models.CharField(max_length=50, blank=True, null=True)
    follower = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name='prodpect_followers')
    following = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name='prodpect_following')
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    signup_confirmation = models.BooleanField(default=False)
    rememberuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ign', 'avatar']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ign).replace(' ', '-')
        # convert white space to hyphen
        self.ign = self.ign.replace(' ', '-')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('userinfo', args=[self.slug])

    def get_avatar(self):
        return self.avatar.url

    def get_gametype(self):
        return self.gametype

    def get_gamerole(self):
        return self.gamerole

    def get_formerteam(self):
        return self.formerteam

    def unfollow(self, user):
        self.following.remove(user)

    def follow(self, user):
        self.following.add(user)

    def check_follow(self, user):
        return self.following.filter(pk=user.pk).exists()


class ProfileHighlights(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    highlight = models.URLField(max_length=200, blank=True, null=True,
                                default='https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    def __str__(self):
        return self.user.ign + ' ' + self.highlight

    def save(self, *args, **kwargs):
        # get parameters from url
        url = self.highlight
        video_id = url.split('v=')[1]
        self.highlight = 'https://www.youtube.com/embed/' + video_id
        super().save(*args, **kwargs)


class ReviewUser(models.Model):
    # rate_choice = (
    #     (1, '1'),
    #     (2, '2'),
    #     (3, '3'),
    #     (4, '4'),
    #     (5, '5'),
    # )
    # star = models.IntegerField(choices=rate_choice, default=5)
    author = models.CharField(
        max_length=50, blank=True, null=True, default='Anonymous')
    avatar = models.URLField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    review = models.TextField(max_length=4000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author

    def get_date(self):
        return self.date.strftime('%d %b %Y')

    def review_count(self):
        return ReviewUser.objects.filter(user=self.user).count()
