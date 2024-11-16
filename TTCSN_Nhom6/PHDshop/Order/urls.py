from django.urls import path
from .views import CreateOrderAPI, OrderDetailAPI

urlpatterns = [
    path('', CreateOrderAPI.as_view(), name='place-order'),  # Đặt hàng
    path('order_detail/<int:pk>/', OrderDetailAPI.as_view(), name='order-detail'),  # Xem chi tiết đơn hàng
    path('order_list/', OrderDetailAPI.as_view(), name='order-list'),  # Xem danh sách đơn hàng của người dùng
]
