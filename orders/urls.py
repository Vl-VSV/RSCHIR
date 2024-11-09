from django.urls import path
from orders.views import OrderCreateView, CancelOrderView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='create-order'),  # Создание заказа
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel-order'),  # Отмена заказа пользователем
]