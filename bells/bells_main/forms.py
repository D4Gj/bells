from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Bell, BellMovementRequest, Belltower, CustomUser


class LoginForm(AuthenticationForm):
    def clean_username(self):
        email = self.cleaned_data.get("username")
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                return email
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid email")
        else:
            raise forms.ValidationError("Email is required")


class BellMovementRequestForm(forms.ModelForm):
    class Meta:
        model = BellMovementRequest
        fields = [
            "reason",
            "bell",
            "temple_from",
            "temple_to",
            "belltowerfrom",
            "belltowerto",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and (user.user_type != "moderator" and not user.is_superuser):
            self.fields.pop("status")


class BellForm(forms.ModelForm):
    class Meta:
        model = Bell
        fields = ["name", "weight", "manufacturer", "audio_file", "image", "belltower"]


class BellCreationForm(forms.ModelForm):
    class Meta:
        model = Bell
        fields = [
            "name",
            "weight",
            "manufacturer",
            "audio_file",
            "image",
            "belltower",
            "status",
        ]


class BellTowerCreationForm(forms.ModelForm):
    class Meta:
        model = Belltower
        fields = ["temple", "belltower_name"]


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
