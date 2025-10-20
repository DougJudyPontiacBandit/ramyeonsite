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
    customer_change_password,
    customer_update_profile
)

# Import new customer product and category views
from api.views.customer_product_views import (
    CustomerProductListView,
    CustomerProductDetailView,
    CustomerProductSearchView,
    CustomerProductByCategoryView,
    CustomerFeaturedProductsView
)
from api.views.customer_category_views import (
    CustomerCategoryListView,
    CustomerCategoryDetailView,
    CustomerCategoryWithProductsView
)

# Import customer promotion views
from api.views.promotion_views import (
    PromotionHealthCheckView,
    PromotionListView,
    PromotionDetailView,
    ActivePromotionsView,
    PromotionsByProductView,
    PromotionsByCategoryView,
    PromotionDiscountCalculatorView,
    PromotionSearchView
)

# Import loyalty points views
from api.views.loyalty_views import (
    get_loyalty_balance,
    get_loyalty_history,
    validate_points_redemption,
    redeem_points,
    award_points,
    loyalty_health_check
)

# Create router and register viewsets
router = DefaultRouter()

urlpatterns = [
    # ========================================
    # NEW CUSTOMER AUTH ENDPOINTS (customers collection)
    # ========================================
    path('auth/customer/login/', customer_login, name='customer-login'),
    path('auth/customer/register/', customer_register, name='customer-register'),
    path('auth/customer/me/', customer_me, name='customer-me'),
    path('auth/customer/profile/update/', customer_update_profile, name='customer-update-profile'),
    path('auth/customer/password/change/', customer_change_password, name='customer-change-password'),
   
    # ========================================
    # CUSTOMER PRODUCT ENDPOINTS (Read-Only)
    # ========================================
    path('customer/products/', CustomerProductListView.as_view(), name='customer-product-list'),
    path('customer/products/featured/', CustomerFeaturedProductsView.as_view(), name='customer-featured-products'),
    path('customer/products/search/', CustomerProductSearchView.as_view(), name='customer-product-search'),
    path('customer/products/category/<str:category_id>/', CustomerProductByCategoryView.as_view(), name='customer-products-by-category'),
    path('customer/products/<str:product_id>/', CustomerProductDetailView.as_view(), name='customer-product-detail'),
    
    # ========================================
    # CUSTOMER CATEGORY ENDPOINTS (Read-Only)
    # ========================================
    path('customer/categories/', CustomerCategoryListView.as_view(), name='customer-category-list'),
    path('customer/categories/<str:category_id>/', CustomerCategoryDetailView.as_view(), name='customer-category-detail'),
    path('customer/categories/<str:category_id>/products/', CustomerCategoryWithProductsView.as_view(), name='customer-category-products'),
   
    # ========================================
    # CUSTOMER PROMOTION ENDPOINTS (Read-Only)
    # ========================================
    path('customer/promotions/health/', PromotionHealthCheckView.as_view(), name='promotion-health'),
    path('customer/promotions/', PromotionListView.as_view(), name='customer-promotion-list'),
    path('customer/promotions/active/', ActivePromotionsView.as_view(), name='customer-active-promotions'),
    path('customer/promotions/search/', PromotionSearchView.as_view(), name='customer-promotion-search'),
    path('customer/promotions/calculate-discount/', PromotionDiscountCalculatorView.as_view(), name='customer-calculate-discount'),
    path('customer/promotions/product/<str:product_id>/', PromotionsByProductView.as_view(), name='customer-promotions-by-product'),
    path('customer/promotions/category/<str:category_id>/', PromotionsByCategoryView.as_view(), name='customer-promotions-by-category'),
    path('customer/promotions/<str:promotion_id>/', PromotionDetailView.as_view(), name='customer-promotion-detail'),
   
    # ========================================
    # CUSTOMER LOYALTY POINTS ENDPOINTS
    # ========================================
    path('customer/loyalty/balance/', get_loyalty_balance, name='customer-loyalty-balance'),
    path('customer/loyalty/history/', get_loyalty_history, name='customer-loyalty-history'),
    path('customer/loyalty/validate-redemption/', validate_points_redemption, name='customer-validate-redemption'),
    path('customer/loyalty/redeem/', redeem_points, name='customer-redeem-points'),
    path('customer/loyalty/award/', award_points, name='customer-award-points'),
    path('customer/loyalty/health/', loyalty_health_check, name='customer-loyalty-health'),
   
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