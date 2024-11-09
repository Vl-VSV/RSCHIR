from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart, CartItem
from menu.models import MenuItem
from cart.serializers import CartSerializer, AddCartItemSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CartView(generics.RetrieveAPIView):
    """
    View and clear the cart.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    quantity_param = openapi.Parameter(
        'quantity', openapi.IN_QUERY, description="Количество удаляемого товара", type=openapi.TYPE_INTEGER, default=1
    )
    
    @swagger_auto_schema(manual_parameters=[quantity_param])
    def delete(self, request, *args, **kwargs):
        """
        Clear all items in the cart.
        """
        cart = self.get_object()
        cart.items.all().delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)

class AddCartItemView(generics.CreateAPIView):
    """
    Add a MenuItem to the cart by its ID, with an optional quantity.
    """
    permission_classes = [IsAuthenticated]
    serializer_class=AddCartItemSerializer

    quantity_param = openapi.Parameter(
        'quantity', openapi.IN_QUERY, description="Количество добавляемого товара", type=openapi.TYPE_INTEGER, default=1
    )
    
    @swagger_auto_schema(manual_parameters=[quantity_param])
    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        menu_item_id = kwargs['menu_item_id']
        quantity = int(request.query_params.get('quantity', 1))

        # Check if the MenuItem exists
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "MenuItem not found"}, status=status.HTTP_404_NOT_FOUND)

        # Add item or increase quantity if it already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=menu_item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)

class RemoveCartItemView(generics.DestroyAPIView):
    """
    Remove a specific quantity of a MenuItem from the cart by its ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        menu_item_id = kwargs['menu_item_id']
        quantity = int(request.query_params.get('quantity', 1))

        # Check if the item exists in the cart
        try:
            cart_item = cart.items.get(item__id=menu_item_id)
            if cart_item.quantity <= quantity:
                cart_item.delete()  # Remove item completely if quantity is less than or equal
            else:
                cart_item.quantity -= quantity
                cart_item.save()

            return Response({"message": "Item quantity updated in cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)