from rest_framework import generics
from .models import Good
from .serializer import GoodSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny


class GoodListView(generics.ListCreateAPIView):
    permission_classes  = [AllowAny]

    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        'brand': ['exact'],
        'category': ['exact'],
    }

class GoodDetailView(generics.RetrieveAPIView):
    permission_classes  = [AllowAny]

    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    lookup_field = 'id'  # Assuming 'id' is the primary key field in your Good mode