from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..services.promotion_service import PromotionService
import logging

logger = logging.getLogger(__name__)

class PromotionHealthCheckView(APIView):
    """Health check endpoint"""
    def get(self, request):
        return Response({
            "service": "Customer Promotions",
            "status": "active",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat()
        }, status=status.HTTP_200_OK)


class PromotionListView(APIView):
    """Get all active promotions"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request):
        """Get all active promotions with optional filtering"""
        try:
            # Extract query parameters
            filters = {}
            
            if request.GET.get('type'):
                filters['type'] = request.GET.get('type')
            
            if request.GET.get('target_type'):
                filters['target_type'] = request.GET.get('target_type')
            
            # Search functionality
            if request.GET.get('q'):
                filters['search_query'] = request.GET.get('q')
            
            # Pagination parameters
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            sort_by = request.GET.get('sort_by', 'created_at')
            sort_order = request.GET.get('sort_order', 'desc')
            
            result = self.promotion_service.get_all_promotions(
                filters=filters,
                page=page,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order
            )
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in PromotionListView.get: {e}")
            return Response(
                {"error": f"Error retrieving promotions: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PromotionDetailView(APIView):
    """Get specific promotion details"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request, promotion_id):
        """Get promotion by PROM-#### ID"""
        try:
            result = self.promotion_service.get_promotion_by_id(promotion_id)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Error in PromotionDetailView.get: {e}")
            return Response(
                {"error": f"Error retrieving promotion: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ActivePromotionsView(APIView):
    """Get all currently active promotions"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request):
        """Get all active promotions"""
        try:
            result = self.promotion_service.get_active_promotions()
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in ActivePromotionsView.get: {e}")
            return Response(
                {"error": f"Error retrieving active promotions: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PromotionsByProductView(APIView):
    """Get promotions applicable to a specific product"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request, product_id):
        """Get promotions for specific product"""
        try:
            result = self.promotion_service.get_promotions_by_product(product_id)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in PromotionsByProductView.get: {e}")
            return Response(
                {"error": f"Error retrieving promotions: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PromotionsByCategoryView(APIView):
    """Get promotions applicable to a specific category"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request, category_id):
        """Get promotions for specific category"""
        try:
            result = self.promotion_service.get_promotions_by_category(category_id)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in PromotionsByCategoryView.get: {e}")
            return Response(
                {"error": f"Error retrieving promotions: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PromotionDiscountCalculatorView(APIView):
    """Calculate best discount for an order"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def post(self, request):
        """Calculate discount for order (preview only, doesn't track usage)"""
        try:
            order_data = request.data
            
            # Validate order data
            if not order_data.get('items'):
                return Response(
                    {"error": "Order must include items"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not order_data.get('total_amount'):
                return Response(
                    {"error": "Order must include total_amount"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = self.promotion_service.calculate_discount_for_order(order_data)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error in PromotionDiscountCalculatorView.post: {e}")
            return Response(
                {"error": f"Error calculating discount: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PromotionSearchView(APIView):
    """Search promotions by name or description"""
    def __init__(self):
        super().__init__()
        self.promotion_service = PromotionService()
    
    def get(self, request):
        """Search promotions"""
        try:
            query = request.GET.get('q', '')
            if not query:
                return Response(
                    {"error": "Query parameter 'q' is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Build search filter
            filters = {'search_query': query}
            
            # Add pagination
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            
            result = self.promotion_service.get_all_promotions(
                filters=filters,
                page=page,
                limit=limit
            )
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in PromotionSearchView.get: {e}")
            return Response(
                {"error": f"Error searching promotions: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )