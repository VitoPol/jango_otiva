from django.contrib.auth.models import AbstractUser
from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Users(AbstractUser):
    moderator = 'moderator'
    admin = 'admin'
    user = 'user'
    unknown = 'unknown'

    roles = [(moderator, moderator), (admin, admin), (user, user), (unknown, unknown)]

    role = models.CharField(max_length=40, null=True, choices=roles, default=unknown)
    age = models.IntegerField(null=True)
    location = models.ManyToManyField(Locations)
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]
