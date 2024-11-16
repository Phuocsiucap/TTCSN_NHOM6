from rest_framework import generics
from .models import Good
from .serializer import GoodSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class GoodListView(generics.ListCreateAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        'brand': ['exact'],
        'category': ['exact'],
    }
