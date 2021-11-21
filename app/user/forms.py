from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _
from .models import User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
            "email": {"unique": _("This email has already been taken.")},
        }


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
