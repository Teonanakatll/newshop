from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField("Аватар", upload_to='users_images', blank=True, null=True)
    phone = models.CharField("Номер телефона", max_length=10, blank=True, null=True)

    class Meta:
        db_table = "user"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username

