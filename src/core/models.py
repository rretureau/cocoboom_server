from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from annoying import fields


class CustomUser(AbstractUser):
    balance = models.PositiveIntegerField(default=0)


class TwitchProfile(models.Model):
    user = fields.AutoOneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="twitch"
    )
    twitch_id = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    profile_type = models.CharField(max_length=50, default="")
    profile_image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="achievements"
    )


class Skin(models.Model):
    RARITY_CHOICES = (
        ('COMMON', 'Common'),
        ('RARE', 'Rare'),
        ('EPIC', 'Epic'),
    )
    name = models.CharField(max_length=100, unique=True, null=False)
    rarity = models.CharField(max_length=50, choices=RARITY_CHOICES)
    unlocked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PurchaseableSkin(models.Model):
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()


class AchievementUnlockableSkin(models.Model):
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)
    achievement_required = models.ForeignKey(
        'Achievement', on_delete=models.CASCADE)


class GameHistory(models.Model):
    rank = models.PositiveIntegerField(null=False)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
