from rest_framework import serializers
from orders.models import Order, OrderType, DeliveryType, OrderItem
from cart.models import CartItem

                
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['menu_item_name', 'menu_item_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        
        
class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Включаем элементы заказа в сериализатор

    class Meta:
        model = Order
        fields = ['order_type', 'delivery_address', 'scheduled_time', 'delivery_type', 'items']
        read_only_fields = ['user', 'status', 'created_at']

    def create(self, validated_data):
        # Здесь можно настроить логику для сохранения, например, присваивать пользователя
        request = self.context.get('request')
        user = request.user  # Получаем пользователя из контекста запроса
        order_type = validated_data.get('order_type')
        address = validated_data.get('delivery_address', None) if order_type == 'delivery' else None
        scheduled_time = validated_data.get('scheduled_time', None) if order_type == 'delivery' else None
        delivery_type = validated_data.get('delivery_type', None)

        # Создаем заказ
        order = Order.objects.create(
            user=user,
            order_type=order_type,
            delivery_address=address,
            scheduled_time=scheduled_time,
            delivery_type=delivery_type
        )

        # Получаем корзину пользователя
        cart = Cart.objects.get(user=user)
        
        # Дублируем элементы из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity
            )

        # Очищаем корзину после создания заказа
        cart.items.all().delete()

        return order