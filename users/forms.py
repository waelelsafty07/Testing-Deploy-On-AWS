from rest_framework import serializers
from .models import Users
from django.contrib.auth.forms import UserChangeForm
from django import forms


class CustomUserChangeFrom(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Users
        fields = UserChangeForm.Meta.fields
        widgets = {
            'bio': forms.Textarea
        }
