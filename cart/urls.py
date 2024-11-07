from django.urls import path
from cart.views import CartView, AddCartItemView, RemoveCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:menu_item_id>/', AddCartItemView.as_view(), name='add_to_cart'),
    path('remove/<int:menu_item_id>/', RemoveCartItemView.as_view(), name='remove_from_cart'), 
]