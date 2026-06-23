from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from products.models import Product

class AddToCartView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = Product.objects.get(id=product_id)

        # get or create cart
        cart, created = Cart.objects.get_or_create(user=user)

        # check if item already exists
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({"message": "Product added to cart"})
    





class CartDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        items = cart.items.all()

        data = []
        total = 0

        for item in items:
            data.append({
                "product": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "subtotal": item.subtotal()
            })
            total += item.subtotal()

        return Response({
            "items": data,
            "total_price": total
        })    
    


class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        user = request.user

        cart = Cart.objects.get(user=user)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"message": "Item removed from cart"})
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity"))

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.get(user=request.user)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.quantity = quantity
            item.save()

            return Response({"message": "Quantity updated"})
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )