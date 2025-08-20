from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # extra fields for Pixora
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.username
