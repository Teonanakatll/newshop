
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    slug = models.SlugField("url", max_length=200, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    slug = models.SlugField("url", max_length=200, unique=True, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    image = models.ImageField("Фото товара", upload_to='goods_images', blank=True, null=True)
    price = models.DecimalField("Цена", default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField("Скидка в %", default=0.00, max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=0)
    time_create = models.DateTimeField("Дата Добавления", auto_now_add=True)
    time_update = models.DateTimeField("Дата изменения", auto_now=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        'Вывод отформатированного id'
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)

        return self.price

