from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=255)
    is_published = models.BooleanField()

    def __str__(self):
        return self.name
