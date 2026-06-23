from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveFromCartView, UpdateCartItemView

urlpatterns = [
    path("add/", AddToCartView.as_view()),
    path("", CartDetailView.as_view()),
    path("remove/", RemoveFromCartView.as_view()),
    path("update/", UpdateCartItemView.as_view()),
]