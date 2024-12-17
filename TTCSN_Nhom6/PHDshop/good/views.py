from rest_framework import generics
from .models import Good
from .serializer import GoodSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
class GetListViewFromCategory(APIView):
    
   def get(self,request, category_id):
       queryset = Good.objects.filter(category__id = category_id)
       seralizer_objects = GoodSerializer(queryset, many = True)
       
       return Response(seralizer_objects.data, status = status.HTTP_200_OK)

class GetListViewFromBrand(APIView):
    
    def get(self,request, brand_id):
        queryset = Good.objects.filter(brand__id = brand_id)
        serializer_objects = GoodSerializer(queryset, many = True)
        return Response(serializer_objects.data, status = status.HTTP_200_OK)