"""
URL configuration for MongoDB test endpoints
"""
from django.urls import path
from app.views.mongodb_test_views import (
    test_connection,
    get_users,
    get_products,
    get_customers,
    get_promotions,
    get_sales_logs
)

urlpatterns = [
    path('connection/', test_connection, name='test_mongodb_connection'),
    path('users/', get_users, name='get_users'),
    path('products/', get_products, name='get_products'),
    path('customers/', get_customers, name='get_customers'),
    path('promotions/', get_promotions, name='get_promotions'),
    path('sales-logs/', get_sales_logs, name='get_sales_logs'),
]
