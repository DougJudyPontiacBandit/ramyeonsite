from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.customer_product_service import CustomerProductService
import logging

logger = logging.getLogger(__name__)

class CustomerProductListView(APIView):
    """
    GET /api/customer/products/
    Get all active products with optional filters and pagination
    
    Query Parameters:
    - page: Page number (default: 1)
    - limit: Items per page (default: 20)
    - category_id: Filter by category (CTGY-###)
    - subcategory_name: Filter by subcategory
    - search: Search by product name or SKU
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - sort_by: Field to sort by (default: product_name)
    - sort_order: asc or desc (default: asc)
    """
    
    def get(self, request):
        try:
            service = CustomerProductService()
            
            # Extract query parameters
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            sort_by = request.GET.get('sort_by', 'product_name')
            sort_order = request.GET.get('sort_order', 'asc')
            
            # Build filters
            filters = {}
            if request.GET.get('category_id'):
                filters['category_id'] = request.GET.get('category_id')
            if request.GET.get('subcategory_name'):
                filters['subcategory_name'] = request.GET.get('subcategory_name')
            if request.GET.get('search'):
                filters['search'] = request.GET.get('search')
            if request.GET.get('min_price'):
                filters['min_price'] = request.GET.get('min_price')
            if request.GET.get('max_price'):
                filters['max_price'] = request.GET.get('max_price')
            
            # Get products
            result = service.get_all_active_products(
                filters=filters if filters else None,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'products': result['products'],
                        'pagination': result['pagination']
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Error retrieving products')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except ValueError as ve:
            logger.error(f"Invalid query parameters: {ve}")
            return Response({
                'success': False,
                'message': 'Invalid query parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in CustomerProductListView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerProductDetailView(APIView):
    """
    GET /api/customer/products/<product_id>/
    Get single product details with promotions
    """
    
    def get(self, request, product_id):
        try:
            service = CustomerProductService()
            
            result = service.get_product_by_id(product_id)
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': result['product']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Product not found')
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error in CustomerProductDetailView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerProductSearchView(APIView):
    """
    GET /api/customer/products/search/
    Search products by name or SKU
    
    Query Parameters:
    - q: Search query (required)
    - page: Page number (default: 1)
    - limit: Items per page (default: 20)
    """
    
    def get(self, request):
        try:
            search_term = request.GET.get('q', '').strip()
            
            if not search_term:
                return Response({
                    'success': False,
                    'message': 'Search query (q) is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            service = CustomerProductService()
            
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            
            result = service.search_products(
                search_term=search_term,
                page=page,
                limit=limit
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'products': result['products'],
                        'pagination': result['pagination'],
                        'search_term': search_term
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Search failed')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except ValueError as ve:
            logger.error(f"Invalid query parameters: {ve}")
            return Response({
                'success': False,
                'message': 'Invalid query parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in CustomerProductSearchView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerProductByCategoryView(APIView):
    """
    GET /api/customer/products/category/<category_id>/
    Get products by category and optional subcategory
    
    Query Parameters:
    - subcategory_name: Optional subcategory filter
    - page: Page number (default: 1)
    - limit: Items per page (default: 20)
    """
    
    def get(self, request, category_id):
        try:
            service = CustomerProductService()
            
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            subcategory_name = request.GET.get('subcategory_name')
            
            result = service.get_products_by_category(
                category_id=category_id,
                subcategory_name=subcategory_name,
                page=page,
                limit=limit
            )
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'products': result['products'],
                        'pagination': result['pagination'],
                        'category_id': category_id,
                        'subcategory_name': subcategory_name
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Error retrieving products')
                }, status=status.HTTP_404_NOT_FOUND)
                
        except ValueError as ve:
            logger.error(f"Invalid query parameters: {ve}")
            return Response({
                'success': False,
                'message': 'Invalid query parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in CustomerProductByCategoryView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerFeaturedProductsView(APIView):
    """
    GET /api/customer/products/featured/
    Get featured products for homepage
    
    Query Parameters:
    - limit: Number of featured products (default: 10)
    """
    
    def get(self, request):
        try:
            service = CustomerProductService()
            
            limit = int(request.GET.get('limit', 10))
            
            result = service.get_featured_products(limit=limit)
            
            if result['success']:
                return Response({
                    'success': True,
                    'data': {
                        'products': result['products'],
                        'count': result['count']
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': result.get('message', 'Error retrieving featured products')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except ValueError as ve:
            logger.error(f"Invalid limit parameter: {ve}")
            return Response({
                'success': False,
                'message': 'Invalid limit parameter'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in CustomerFeaturedProductsView: {e}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)