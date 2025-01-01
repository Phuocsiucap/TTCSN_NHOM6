# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from Order.models import Order, OrderGood
from good.models import Good
from Order.serializers import OrderSerializer, OrderGoodSerializer
from Voucher.models import Voucher
from Voucher.serializers import VoucherUserSerializer,VoucherSerializer
# Quản lý đơn hàng
class OrderListView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy danh sách các đơn hàng
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    # Tạo đơn hàng mới
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Quản lý chi tiết đơn hàng
class OrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Lấy chi tiết đơn hàng
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Cập nhật thông tin đơn hàng
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Xóa đơn hàng
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

from django.shortcuts import get_object_or_404
# Quản lý sản phẩm trong đơn hàng
from good.serializer import GoodSerializer
class OrderGoodListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Lấy danh sách sản phẩm trong đơn hàng
    def get(self, request, order_pk):
        order = get_object_or_404(Order, order_id=order_pk)
        order_serializer = OrderSerializer(order)
        order_goods = OrderGood.objects.filter(order=order)
        order_goods_serializer = OrderGoodSerializer(order_goods, many=True)
        voucher=Voucher.objects.filter(order=order)
        # voucher_title=voucher_id.split("-")
        # voucher=Voucher.objects.filter(title=voucher_title[1])
        Voucher_serializer=VoucherSerializer(voucher,many=True)
        # Lấy danh sách các sản phẩm liên quan đến đơn hàng
        goods_in_order = Good.objects.filter(ordergood__order=order).distinct()
        goods_serializer = GoodSerializer(goods_in_order, many=True)
        response_data = {
            "order": order_serializer.data,
            "order_good": order_goods_serializer.data,
            "good": goods_serializer.data,
            "voucher":Voucher_serializer.data,
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)
    # Thêm sản phẩm vào đơn hàng
    def post(self, request, order_pk):
        data = request.data
        data['order'] = order_pk  # Gán order_id vào dữ liệu
        serializer = OrderGoodSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.db.models import Sum
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, IsAdminUser
class MonthlyRevenueAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Khởi tạo danh sách chứa doanh thu các tháng
        monthly_revenues = []

        # Lấy năm hiện tại
        current_year = timezone.now().year

        # Lặp qua từng tháng từ 1 đến 12
        for month in range(1, 13):
            # Lọc đơn hàng theo tháng và trạng thái 'Delivered'
            orders = Order.objects.filter(
                shipping_status='Delivered',
                purchase_date__month=month,
                purchase_date__year=current_year  # Đảm bảo lọc theo năm hiện tại
            )

            # Tính tổng doanh thu của tháng
            total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

            # Thêm dữ liệu vào danh sách
            monthly_revenues.append({
                'month': f'Tháng {month}',
                'total_revenue': total_revenue,
            })

        # Tách dữ liệu ra hai danh sách: tên tháng và doanh thu để thuận tiện sử dụng trong frontend
        months = [item['month'] for item in monthly_revenues]
        revenues = [item['total_revenue'] for item in monthly_revenues]

        # Trả về dữ liệu dạng JSON
        return Response({
            'months': months,
            'revenues': revenues,
        })


class WeeklyRevenueAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Lấy ngày đầu tuần và cuối tuần của tuần hiện tại
        today = timezone.now()
        start_of_week = today - timezone.timedelta(days=today.weekday())  # Ngày thứ hai trong tuần
        end_of_week = start_of_week + timezone.timedelta(days=6)  # Ngày chủ nhật trong tuần

        # Lọc đơn hàng trong tuần này có trạng thái 'Delivered'
        orders = Order.objects.filter(
            shipping_status='Delivered',
            purchase_date__range=[start_of_week, end_of_week]  # Sử dụng purchase_date để lọc theo tuần
        )

        # Tính tổng doanh thu cho mỗi ngày trong tuần
        daily_revenues = []
        for i in range(7):
            day_start = start_of_week + timezone.timedelta(days=i)
            day_end = day_start + timezone.timedelta(days=1)

            # Lọc các đơn hàng trong ngày đó
            daily_orders = orders.filter(purchase_date__range=[day_start, day_end])
            daily_revenue = daily_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            daily_revenues.append(daily_revenue)

        # Trả về dữ liệu doanh thu tuần này
        return Response({
            'labels': ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"],
            'revenue': daily_revenues,  # Doanh thu cho từng ngày trong tuần
        })