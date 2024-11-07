from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import MenuItem
from .serializers import MenuItemSerializer, MenuItemDetailSerializer

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
    search_fields = ['nameч', 'description']  # Поиск по имени и описанию

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Категория меню", type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Получение списка пунктов меню с поддержкой фильтров, сортировки и поиска.
        """
        return super().get(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        """
        Добавление нового блюда (только для админов).
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Получение информации об одном блюде.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Включаем описание только для отдельного блюда
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Частичное обновление информации о блюде (только для админов).
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        Обновление информации о блюде (только для админов).
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Удаление блюда (только для админов).
        """
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)