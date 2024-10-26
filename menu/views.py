from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    # Фильтрация по категориям, а также добавление диапазона цены
    filterset_fields = {
        'category': ['exact'],    # Фильтрация по категории
        'price': ['gte', 'lte'],  # Диапазон цены (>= и <=)
    }
    ordering_fields = ['name', 'price']  # Позволяет сортировку по имени и цене
    search_fields = ['name', 'description']  # Поиск по имени и описанию

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Категория меню", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'price__gte', openapi.IN_QUERY, description="Минимальная цена", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'price__lte', openapi.IN_QUERY, description="Максимальная цена", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY, description="Сортировка по name или price", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Поиск по имени и описанию", type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Получение списка пунктов меню с поддержкой фильтров, сортировки и поиска.
        """
        return super().get(request, *args, **kwargs)