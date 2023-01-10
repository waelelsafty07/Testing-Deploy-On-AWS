from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    email_confirm = models.BooleanField(default=False)
    bio = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
