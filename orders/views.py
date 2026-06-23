from decimal import Decimal

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart


class CheckoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(customer=user)

        total_price = Decimal("0.00")

        for item in cart_items:

            if item.quantity > item.product.stock:
                order.delete()
                return Response(
                    {
                        "error": f"Not enough stock for {item.product.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total_price += item.product.price * item.quantity

            item.product.stock -= item.quantity
            item.product.save()

        order.total_price = total_price
        order.save()

        cart_items.delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)