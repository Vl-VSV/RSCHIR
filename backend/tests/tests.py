from django.test import TestCase
from django.utils.timezone import now, timedelta
from cart.models import MenuItem, Cart
from orders.models import Order, OrderItem, OrderStatus, OrderType, DeliveryType
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и объект меню
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.menu_item = MenuItem.objects.create(name="Burger", price=10.0)

    def test_create_order(self):
        """Проверка создания заказа"""
        order = Order.objects.create(
            user=self.user,
            status=OrderStatus.PROCESSING.value,
            order_type=OrderType.DELIVERY.value,
            delivery_type=DeliveryType.IMMEDIATE.value,
            delivery_address="123 Test Street"
        )
        self.assertEqual(order.status, OrderStatus.PROCESSING.value)
        self.assertEqual(order.order_type, OrderType.DELIVERY.value)
        self.assertEqual(order.delivery_address, "123 Test Street")

    def test_save_resets_scheduled_time_for_immediate_delivery(self):
        """Проверка сброса времени для мгновенной доставки"""
        order = Order.objects.create(
            user=self.user,
            status=OrderStatus.PROCESSING.value,
            order_type=OrderType.DELIVERY.value,
            delivery_type=DeliveryType.IMMEDIATE.value,
            delivery_address="123 Test Street",
            scheduled_time=now() + timedelta(days=1)
        )
        self.assertIsNone(order.scheduled_time)

    def test_create_order_item(self):
        """Проверка создания элемента заказа"""
        order = Order.objects.create(
            user=self.user,
            status=OrderStatus.PROCESSING.value,
            order_type=OrderType.DELIVERY.value
        )
        order_item = OrderItem.objects.create(order=order, menu_item=self.menu_item, quantity=2)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.menu_item.name, "Burger")

    def test_order_item_string_representation(self):
        """Проверка строкового представления OrderItem"""
        order = Order.objects.create(user=self.user)
        order_item = OrderItem.objects.create(order=order, menu_item=self.menu_item, quantity=3)
        self.assertEqual(str(order_item), "Burger x 3")

    def test_filter_orders_by_status(self):
        """Проверка фильтрации заказов по статусу"""
        Order.objects.create(user=self.user, status=OrderStatus.PROCESSING.value)
        Order.objects.create(user=self.user, status=OrderStatus.DELIVERED.value)

        processing_orders = Order.objects.filter(status=OrderStatus.PROCESSING.value)
        self.assertEqual(processing_orders.count(), 1)

    def test_order_string_representation(self):
        """Проверка строкового представления Order"""
        order = Order.objects.create(user=self.user)
        self.assertEqual(str(order), f"Order {order.id} - testuser")