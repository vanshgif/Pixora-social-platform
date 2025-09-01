from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # extra fields for Pixora
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")  # prevents duplicate follows

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"
