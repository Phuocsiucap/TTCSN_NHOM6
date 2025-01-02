# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from Order.models import Order, OrderGood
from good.models import Good
from Order.serializers import OrderSerializer, OrderGoodSerializer

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

# Quản lý sản phẩm trong đơn hàng
class OrderGoodListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Lấy danh sách sản phẩm trong đơn hàng
    def get(self, request, order_pk):
        order_goods = OrderGood.objects.filter(order__pk=order_pk)
        serializer = OrderGoodSerializer(order_goods, many=True)
        # goods_in_order = Good.objects.filter().distinct()
        return Response(serializer.data)

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

#hùng sửa
from django.utils import timezone
from datetime import timedelta

class WeeklyRevenueAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Lấy ngày giờ hiện tại và điều chỉnh sang múi giờ Việt Nam (UTC+7)
        today = timezone.now() + timedelta(hours=7)

        # Lấy ngày đầu tuần và cuối tuần của tuần hiện tại
        start_of_week = today - timedelta(days=today.weekday())  # Ngày thứ hai trong tuần
        end_of_week = start_of_week + timedelta(days=6)  # Ngày chủ nhật trong tuần

        # Điều chỉnh ngày giờ để bắt đầu từ 00:00:00 (ngày đầu tuần) và kết thúc vào 23:59:59 (ngày cuối tuần)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Lọc đơn hàng trong tuần này có trạng thái 'Delivered'
        orders = Order.objects.filter(
            shipping_status='Delivered',
            purchase_date__range=[start_of_week, end_of_week]  # Sử dụng purchase_date để lọc theo tuần
        )

        # Tính tổng doanh thu cho mỗi ngày trong tuần
        daily_revenues = []
        for i in range(7):
            day_start = start_of_week + timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            # Lọc các đơn hàng trong ngày đó
            daily_orders = orders.filter(purchase_date__range=[day_start, day_end])
            daily_revenue = daily_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            daily_revenues.append(daily_revenue)

        # Trả về dữ liệu doanh thu tuần này
        return Response({
            'labels': ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"],
            'revenue': daily_revenues,  # Doanh thu cho từng ngày trong tuần
        })

class DeliveredOrdersCountAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Lọc đơn hàng có trạng thái 'Delivered'
        delivered_orders_count = Order.objects.filter(shipping_status='Delivered').count()

        # Trả về số lượng đơn hàng đã giao thành công
        return Response({
            'delivered_orders_count': delivered_orders_count
        }, status=status.HTTP_200_OK)


class TodayRevenueAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]  # Chỉ admin mới được phép truy cập

    def get(self, request):
        # Lấy ngày hôm nay
        today = timezone.now().date()  # Lấy ngày hiện tại mà không có giờ
        
        # Lọc các đơn hàng có trạng thái 'Delivered' và ngày mua là hôm nay
        orders = Order.objects.filter(
            shipping_status='Delivered',
            purchase_date__day=today.day,
            purchase_date__month=today.month,
            purchase_date__year=today.year,
            
        )

        # Tính tổng doanh thu (tổng số tiền từ các đơn hàng đã giao)
        total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Trả về doanh thu cho ngày hôm nay
        return Response({
            'date': today,
            'revenue': total_revenue,
        })