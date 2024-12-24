from django.urls import path, include
from rest_framework import routers

from order.views import OrderViewSet, OrderItemViewSet

router = routers.DefaultRouter()
router.register("", OrderViewSet)
router.register("order-item", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "order"
