# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from good.models import Good
from good.serializer import GoodSerializer

class GoodListView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy danh sách các sản phẩm
    def get(self, request):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

    # Thêm sản phẩm mới
    def post(self, request):
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoodDetailView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy thông tin sản phẩm
    def get(self, request, pk):
        try:
            good = Good.objects.get(pk=pk)
            serializer = GoodSerializer(good)
            return Response(serializer.data)
        except Good.DoesNotExist:
            return Response({"detail": "Good not found."}, status=status.HTTP_404_NOT_FOUND)

    # Cập nhật thông tin sản phẩm
    def put(self, request, pk):
        try:
            good = Good.objects.get(pk=pk)
            serializer = GoodSerializer(good, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Good.DoesNotExist:
            return Response({"detail": "Good not found."}, status=status.HTTP_404_NOT_FOUND)

    # Cập nhật một phần thông tin sản phẩm
    def patch(self, request, pk):
        try:
            good = Good.objects.get(pk=pk)
            serializer = GoodSerializer(good, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Good.DoesNotExist:
            return Response({"detail": "Good not found."}, status=status.HTTP_404_NOT_FOUND)

    # Xóa sản phẩm
    def delete(self, request, pk):
        try:
            good = Good.objects.get(pk=pk)
            good.delete()
            return Response({"detail": "Good deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Good.DoesNotExist:
            return Response({"detail": "Good not found."}, status=status.HTTP_404_NOT_FOUND)
