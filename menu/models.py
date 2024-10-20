from django.db import models
from enum import Enum

class Category(Enum):
    HOT = 'hot'
    SOUP = 'soup'
    DESSERT = 'dessert'
    SALAD = 'salad'
    DRINK = 'drink'

class MenuItem(models.Model):
    name = models.CharField(max_length=100)  # Название пункта меню
    description = models.TextField()  # Описание
    category = models.CharField(max_length=20, choices=[(tag.value, tag.name.capitalize()) for tag in Category])  # Категория пункта
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена

    def __str__(self):
        return self.name  # Возвращаем название пункта для удобства