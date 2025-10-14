from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..services.customer_category_service import CustomerCategoryService
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerCategoryListView(APIView):
    """
    GET /api/customer/categories/
    Get all active categories with product counts
    """
    
    def get(self, request):
        try:
            service = CustomerCategoryService()
            
            result = service.get_all_active_categories()
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'categories': result['categories'],
                        'count': result['count']
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Error retrieving categories')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in CustomerCategoryListView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerCategoryDetailView(APIView):
    """
    GET /api/customer/categories/<category_id>/
    Get single category details with subcategories
    """
    
    def get(self, request, category_id):
        try:
            service = CustomerCategoryService()
            
            result = service.get_category_by_id(category_id)
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': result['category']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Category not found')
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error in CustomerCategoryDetailView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerCategoryWithProductsView(APIView):
    """
    GET /api/customer/categories/<category_id>/products/
    Get category with its available products (paginated)
    
    Query Parameters:
    - subcategory_name: Optional subcategory filter
    - page: Page number (default: 1)
    - limit: Items per page (default: 20)
    """
    
    def get(self, request, category_id):
        try:
            service = CustomerCategoryService()
            
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            subcategory_name = request.GET.get('subcategory_name')
            
            result = service.get_category_with_products(
                category_id=category_id,
                subcategory_name=subcategory_name,
                page=page,
                limit=limit
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'category': result['category'],
                        'products': result['products'],
                        'pagination': result['pagination']
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Error retrieving category products')
                }, status=status.HTTP_404_NOT_FOUND)
                
        except ValueError as ve:
            logger.error(f"Invalid query parameters: {ve}")
            return Response({
                'success': False,
                'message': 'Invalid query parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in CustomerCategoryWithProductsView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)