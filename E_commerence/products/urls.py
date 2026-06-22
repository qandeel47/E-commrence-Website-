from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    SellerProductCreateView,
    SellerProductListView,
)

urlpatterns = [
    # public
    path("", ProductListView.as_view()),
    path("<int:pk>/", ProductDetailView.as_view()),

    # seller APIs
    path("seller/create/", SellerProductCreateView.as_view()),
    path("seller/my-products/", SellerProductListView.as_view()),
]