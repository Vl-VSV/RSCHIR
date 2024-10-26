from django.urls import path
from .views import MenuItemListView, MenuItemDetailView

urlpatterns = [
    path('items/', MenuItemListView.as_view(), name='menu-items'),
    path('items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
]