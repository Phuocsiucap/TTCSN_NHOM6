from django.urls import path
from .views import VoucherListView, RedeemVoucherView, RedeemedVouchersView, UserPointsView, UpdateUserPointsView

urlpatterns = [
    path('', VoucherListView.as_view(), name='voucher_list'),
    path('redeem/', RedeemVoucherView.as_view(), name='redeem_voucher'),
    path('redeemed_vouchers/', RedeemedVouchersView.as_view(), name='redeemed_vouchers')
]