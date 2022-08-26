from cProfile import label
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, ProfileHighlights, ReviewUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from django.utils.html import escape


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    ign = forms.CharField(label="IGN", widget=forms.TextInput(attrs={
                          'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'placeholder': 'IGN'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'ign', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'placeholder': 'name@gmail.com'})
        self.fields['password'].widget.attrs.update(
            {'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'placeholder': 'Password'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        password = cleaned_data.get("password")
        ign = cleaned_data.get("ign")
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)
        if ign:
            # escape the html characters
            ign = escape(ign)
            # check if the ign is already in use
            if CustomUser.objects.filter(ign=ign).exists():
                self.add_error('ign', 'This IGN is already in use.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if not user:
                raise forms.ValidationError("Invalid email")
            if not user.check_password(password):
                raise forms.ValidationError("Invalid password")
        return cleaned_data


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
                              'class': 'block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400', 'placeholder': 'Upload Avatar', 'accept': 'image/*', 'label': ''}))

    class Meta:
        model = CustomUser
        fields = ['avatar']

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        avatar = cleaned_data.get('avatar')
        # validate extension
        if avatar:
            extension = avatar.name.split('.')[-1]
            if extension not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                raise forms.ValidationError("Invalid extension")
        return cleaned_data


# class ReviewForm(forms.ModelForm):
#     review = forms.CharField(label="Review", widget=forms.Textarea(attrs={
#                              'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Your message...', 'rows': '4'}))

#     class Meta:
#         model = ReviewUser
#         fields = ['review']

#     def clean(self, *args, **kwargs):
#         cleaned_data = super().clean(*args, **kwargs)
#         review = cleaned_data.get('review')
#         if review:
#             # escape the html characters
#             review = escape(review)

#         return cleaned_data
