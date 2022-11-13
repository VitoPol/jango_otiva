from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Locations(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=40)
    age = models.IntegerField()
    location = models.ManyToManyField(Locations)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Ads(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.CharField(max_length=500, null=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to="logos/")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
