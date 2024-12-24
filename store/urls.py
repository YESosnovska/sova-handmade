from django.urls import path, include
from rest_framework import routers

from store.views import ProductViewSet, CombinedViewSet

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("tags", CombinedViewSet, basename="combined")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "store"
