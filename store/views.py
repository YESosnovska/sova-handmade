from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from store.models import Topic, Form, Product
from store.permissions import IsAdminOrReadOnly
from store.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    TopicSerializer,
    FormSerializer,
)


class CombinedViewSet(viewsets.ViewSet):
    def list(self, request):
        topics = Topic.objects.all()
        forms = Form.objects.all()

        topics_data = TopicSerializer(topics, many=True).data
        forms_data = FormSerializer(forms, many=True).data

        combined_data = {"topics": topics_data, "forms": forms_data}

        return Response(combined_data)


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Product.objects.prefetch_related("form", "topic")
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        form = self.request.query_params.get("form")
        topic = self.request.query_params.get("topic")
        exclude = self.request.query_params.get("exclude")
        max_length = self.request.query_params.get("max_length")

        queryset = self.queryset

        if form:
            queryset = queryset.filter(form__name__icontains=form)

        if topic:
            queryset = queryset.filter(topic__name__icontains=topic)

        if exclude:
            queryset = queryset.exclude(id__in=exclude)

        queryset = queryset.distinct()

        if max_length:
            max_length = int(max_length)
            queryset = queryset[:max_length]

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        if self.action == "upload_image":
            return ProductImageSerializer

        return ProductSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "form",
                type=OpenApiTypes.STR,
                description="Filter by form (ex. ?form=підсвічник)",
            ),
            OpenApiParameter(
                "topic",
                type=OpenApiTypes.STR,
                description="Filter by topic (ex. ?topic=весна)",
            ),
            OpenApiParameter(
                "max_length",
                type=OpenApiTypes.INT,
                description="Limit length of queryset (ex. max_length=5)",
            ),
            OpenApiParameter(
                "exclude",
                type=OpenApiTypes.INT,
                description="Get queryset except one product (ex. exclude=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
