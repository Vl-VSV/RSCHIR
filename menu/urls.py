from django.urls import path
from .views import MenuItemListView

urlpatterns = [
    path('items/', MenuItemListView.as_view(), name='menu-items'),
]