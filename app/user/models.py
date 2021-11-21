from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from app.location.models import Location
from .managers import UserCustomManager

# Create your models here.
class User(AbstractUser):
    class GENDER(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="user",
        blank=True,
        null=True,
    )
    full_name = models.CharField(_("Full name of user"), max_length=255)
    email = models.EmailField(_("Email of user"), max_length=255, unique=True)
    phone_number = models.CharField(
        _("Phone number of user"),
        max_length=20,
        blank=True,
        null=True,
    )
    gender = models.CharField(
        _("Gender of user"),
        max_length=1,
        choices=GENDER.choices,
        blank=True,
        null=True,
    )
    display_picture = models.ImageField(
        upload_to="display_picture/",
        blank=True,
        null=True,
    )
    google_id = models.CharField(max_length=255, blank=True, null=True)

    objects = UserCustomManager()

    def __str__(self):
        return self.full_name

    def get_display_picture(self):
        if self.display_picture:
            if settings.ENV == "local":
                return "http://127.0.0.1:3000" + self.display_picture.url
            else:
                return self.display_picture.url
        return ""

    class Meta:
        db_table = "users"
