from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import mongodb_views
from . import pos_views

# Import new customer auth views
from api.views.auth_views import (
    customer_login,
    customer_register,
    customer_me,
    customer_change_password
)

# Create router and register viewsets
router = DefaultRouter()
# COMMENTED OUT - To be fixed later
# router.register(r'categories', views.CategoryViewSet, basename='category')
# router.register(r'products', views.ProductViewSet, basename='product')
# router.register(r'vouchers', views.VoucherViewSet, basename='voucher')
# router.register(r'promotions', views.PromotionViewSet, basename='promotion')
# router.register(r'cart', views.CartViewSet, basename='cart')
# router.register(r'orders', views.OrderViewSet, basename='order')
# router.register(r'user-vouchers', views.UserVoucherViewSet, basename='user-voucher')
# router.register(r'loyalty-rewards', views.LoyaltyRewardViewSet, basename='loyalty-reward')
# router.register(r'user-rewards', views.UserRewardViewSet, basename='user-reward')
# router.register(r'points-transactions', views.PointsTransactionViewSet, basename='points-transaction')
# router.register(r'promotion-redemptions', views.PromotionRedemptionViewSet, basename='promotion-redemption')

urlpatterns = [
    # ========================================
    # NEW CUSTOMER AUTH ENDPOINTS (customers collection)
    # ========================================
    path('auth/customer/login/', customer_login, name='customer-login'),
    path('auth/customer/register/', customer_register, name='customer-register'),
    path('auth/customer/me/', customer_me, name='customer-me'),
    path('auth/customer/password/change/', customer_change_password, name='customer-change-password'),
    
    # ========================================
    # OLD AUTH ENDPOINTS (users collection - commented out)
    # ========================================
    # path('auth/register/', mongodb_views.register_mongodb, name='register'),
    # path('auth/login/', mongodb_views.login_mongodb, name='login'),
    # path('auth/logout/', views.logout_view, name='logout'),
    # path('auth/profile/', views.profile_view, name='profile'),
    # path('auth/profile/update/', views.update_profile_view, name='update-profile'),
    
    # ========================================
    # POINTS AND QR CODE ENDPOINTS (commented out)
    # ========================================
    # path('points/history/', views.get_points_history, name='points-history'),
    # path('qrcode/', views.get_user_qr_code, name='user-qr-code'),
    
    # ========================================
    # NEWSLETTER AND CONTACT (commented out)
    # ========================================
    # path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe-newsletter'),
    # path('contact/', views.contact_message, name='contact-message'),
    
    # ========================================
    # POS (Point of Sale) ENDPOINTS
    # ========================================
    path('pos/scan-user/', pos_views.scan_user_qr, name='pos-scan-user'),
    path('pos/scan-promotion/', pos_views.scan_promotion_qr, name='pos-scan-promotion'),
    path('pos/redeem-promotion/', pos_views.redeem_promotion, name='pos-redeem-promotion'),
    path('pos/award-points/', pos_views.award_points_manual, name='pos-award-points'),
    path('pos/process-order-points/', pos_views.process_order_points, name='pos-process-order-points'),
    path('pos/user/<str:qr_code>/', pos_views.get_user_by_qr, name='pos-get-user'),
    path('pos/promotion/<str:qr_code>/', pos_views.get_promotion_by_qr, name='pos-get-promotion'),
    path('pos/dashboard/', pos_views.pos_dashboard, name='pos-dashboard'),
    
    # ========================================
    # ROUTER URLs (commented out)
    # ========================================
    # path('', include(router.urls)),
]