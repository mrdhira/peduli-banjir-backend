from django.contrib.auth.models import UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class UserCustomManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().order_by("full_name")

    def get_by_username(self, username):
        user = self.filter(username).first()
        if not user:
            raise ObjectDoesNotExist()
        else:
            return user