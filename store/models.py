from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    price =models.PositiveIntegerField(
        verbose_name="Цена (в центах)",
        help_text="Цена указывается в минорных единицах валюты. Например, 1000 = 10.00 $"
    )
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

