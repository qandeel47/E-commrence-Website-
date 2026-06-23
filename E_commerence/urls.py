from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ---------------- Swagger Setup ----------------
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ---------------- Main URLs ----------------
urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger URLs
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),

    # API routes
    path("api/users/", include("users.urls")),
    path("api/products/", include("products.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/orders/", include("orders.urls")),
]