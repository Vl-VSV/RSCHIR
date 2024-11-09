from django.db import models
from enum import Enum
from django.contrib.auth import get_user_model
from cart.models import Cart, MenuItem

User = get_user_model()

# Определение статуса заказа
class OrderStatus(Enum):
    PROCESSING = 'processing'
    PREPARING = 'preparing'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls]

# Определение типа заказа
class OrderType(Enum):
    DELIVERY = 'delivery'
    PICKUP = 'pickup'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls]

# Определение типа доставки
class DeliveryType(Enum):
    IMMEDIATE = 'immediate'
    SCHEDULED = 'scheduled'

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls]

# Модель для элементов заказа
class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)  # Меню, добавленное в заказ
    quantity = models.PositiveIntegerField()  # Количество каждого элемента

    def __str__(self):
        return f'{self.menu_item.name} x {self.quantity}'

# Модель заказа
class Order(models.Model):
    STATUS_CHOICES = OrderStatus.choices()
    ORDER_TYPE_CHOICES = OrderType.choices()
    DELIVERY_TYPE_CHOICES = DeliveryType.choices()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OrderStatus.PROCESSING.value)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES, default=OrderType.DELIVERY.value)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPE_CHOICES, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order_type == OrderType.DELIVERY.value and self.delivery_type == DeliveryType.IMMEDIATE.value:
            self.scheduled_time = None  # Сброс времени для мгновенной доставки

    def __str__(self):
        return f'Order {self.id} - {self.user.username}'