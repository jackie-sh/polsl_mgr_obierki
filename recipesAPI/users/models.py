from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "%s" % self.username

    class Meta:
        ordering = ['username', 'email']
        swappable = 'AUTH_USER_MODEL'
