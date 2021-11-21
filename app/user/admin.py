from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            _("Personal Info"),
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone_number",
                    "gender",
                    "display_picture",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "full_name",
        "is_superuser",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "full_name",
    )

    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
    )


admin.site.register(User, UserAdmin)
