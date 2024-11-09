from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order, OrderStatus, OrderType, OrderItem
from orders.serializers import OrderSerializer, OrderCreateSerializer
from cart.models import Cart
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrderCreateView(generics.CreateAPIView):
    """
    Создать заказ на основе текущей корзины пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        # Получаем корзину пользователя
        cart = Cart.objects.get(user=request.user)

        # Проверяем, пуста ли корзина
        if not cart or cart.items.count() == 0:
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем параметры из запроса или используем значения по умолчанию
        order_type = request.data.get('order_type', OrderType.DELIVERY.value)
        address = request.data.get('address', None) if order_type == OrderType.DELIVERY.value else None
        scheduled_time = request.data.get('scheduled_time', None) if order_type == OrderType.DELIVERY.value else None
        delivery_type = request.data.get('delivery_type', None)  # Тип доставки для DELIVERY заказов

        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            status=OrderStatus.PROCESSING.value,  # Статус по умолчанию "processing"
            order_type=order_type,
            delivery_address=address,
            scheduled_time=scheduled_time,
            delivery_type=delivery_type if order_type == OrderType.DELIVERY.value else None
        )

        # Дублируем элементы из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(order=order, menu_item=item.item, quantity=item.quantity)

        # Очищаем корзину пользователя после создания заказа
        cart.items.all().delete()

        # Возвращаем сериализованные данные заказа
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    

class CancelOrderView(generics.UpdateAPIView):
    """
    Отмена заказа (пользователь может отменить заказ, если он в статусах 'processing' или 'preparing').
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()  # Specify the queryset for the view
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # Проверяем, может ли пользователь отменить заказ
        if order.user != request.user or order.status not in [OrderStatus.PROCESSING.value, OrderStatus.PREPARING.value]:
            return Response({"error": "Order cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)

        # Отменяем заказ
        order.status = OrderStatus.CANCELED.value
        order.save()
        return Response({"message": "Order canceled"}, status=status.HTTP_200_OK)
    
    
class OrderListView(generics.ListAPIView):
    """
    Получить все заказы пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()  # Ensure that a queryset is defined
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    # Фильтрация по статусу заказа
    filterset_fields = {
        'status': ['exact'],  # Фильтрация по статусу заказа
        'created_at': ['gte', 'lte'],  # Диапазон по дате создания
    }
    ordering_fields = ['created_at', 'status']  # Позволяет сортировку по дате и статусу
    search_fields = ['user__username', 'status']  # Поиск по имени пользователя и статусу

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Статус заказа", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'created_at', openapi.IN_QUERY, description="Дата создания заказа", type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Получение списка заказов пользователя с поддержкой фильтров, сортировки и поиска.
        """
        return super().get(request, *args, **kwargs)