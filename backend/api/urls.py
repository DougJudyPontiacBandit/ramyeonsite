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

# Create router and register viewsets
router = DefaultRouter()

urlpatterns = [
    # ========================================
    # NEW CUSTOMER AUTH ENDPOINTS (customers collection)
    # ========================================
    path('auth/customer/login/', customer_login, name='customer-login'),
    path('auth/customer/register/', customer_register, name='customer-register'),
    path('auth/customer/me/', customer_me, name='customer-me'),
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