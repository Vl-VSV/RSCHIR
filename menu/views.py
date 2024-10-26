from .serializers import MenuItemSerializer
from rest_framework import generics
from .models import MenuItem
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()  # Получаем все пункты меню
    serializer_class = MenuItemSerializer  # Указываем сериализатор
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи могут получить доступ

    @swagger_auto_schema()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)  # Получаем параметр category
        if category:
            queryset = queryset.filter(category=category)  # Фильтруем по категории
        return queryset