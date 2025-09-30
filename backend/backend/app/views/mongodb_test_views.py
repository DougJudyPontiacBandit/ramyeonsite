"""
Test views for MongoDB connection
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

from app.services.mongodb_service import mongodb_service

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def test_connection(request):
    """Test MongoDB connection and return database stats"""
    try:
        stats = mongodb_service.get_database_stats()
        return JsonResponse({
            'status': 'success',
            'message': 'MongoDB connection successful',
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error testing MongoDB connection: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to connect to MongoDB: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_users(request):
    """Get all users from MongoDB"""
    try:
        users = mongodb_service.get_all_users()
        return JsonResponse({
            'status': 'success',
            'message': 'Users retrieved successfully',
            'data': users,
            'count': len(users)
        })
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to get users: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_products(request):
    """Get all products from MongoDB"""
    try:
        products = mongodb_service.get_all_products()
        return JsonResponse({
            'status': 'success',
            'message': 'Products retrieved successfully',
            'data': products,
            'count': len(products)
        })
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to get products: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_customers(request):
    """Get all customers from MongoDB"""
    try:
        customers = mongodb_service.get_all_customers()
        return JsonResponse({
            'status': 'success',
            'message': 'Customers retrieved successfully',
            'data': customers,
            'count': len(customers)
        })
    except Exception as e:
        logger.error(f"Error getting customers: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to get customers: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_promotions(request):
    """Get all promotions from MongoDB"""
    try:
        promotions = mongodb_service.get_all_promotions()
        return JsonResponse({
            'status': 'success',
            'message': 'Promotions retrieved successfully',
            'data': promotions,
            'count': len(promotions)
        })
    except Exception as e:
        logger.error(f"Error getting promotions: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to get promotions: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_sales_logs(request):
    """Get all sales logs from MongoDB"""
    try:
        sales_logs = mongodb_service.get_all_sales_logs()
        return JsonResponse({
            'status': 'success',
            'message': 'Sales logs retrieved successfully',
            'data': sales_logs,
            'count': len(sales_logs)
        })
    except Exception as e:
        logger.error(f"Error getting sales logs: {e}")
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to get sales logs: {str(e)}'
        }, status=500)
