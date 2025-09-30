from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Promotions
from .services import PromotionService
from app.decorators.authenticationDecorator import require_authentication, require_admin
import logging

logger = logging.getLogger(__name__)

class PromotionListView(APIView):
    """View for listing and creating promotions"""
    def __init__(self):
        self.promotion_service = PromotionService()

    @require_authentication
    def get(self, request):
        """Get all promotions"""
        try:
            promotions = self.promotion_service.get_all_promotions()
            return Response({
                "success": True,
                "promotions": promotions
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting promotions: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_admin
    def post(self, request):
        """Create new promotion"""
        try:
            promotion_data = request.data
            new_promotion = self.promotion_service.create_promotion(
                promotion_data,
                request.current_user
            )
            return Response({
                "success": True,
                "promotion": new_promotion
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating promotion: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PromotionDetailView(APIView):
    """View for individual promotion operations"""
    def __init__(self):
        self.promotion_service = PromotionService()

    @require_authentication
    def get(self, request, promotion_id):
        """Get promotion by ID"""
        try:
            promotion = self.promotion_service.get_promotion_by_id(promotion_id)
            if promotion:
                return Response({
                    "success": True,
                    "promotion": promotion
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting promotion {promotion_id}: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_admin
    def put(self, request, promotion_id):
        """Update promotion"""
        try:
            promotion_data = request.data
            updated_promotion = self.promotion_service.update_promotion(
                promotion_id,
                promotion_data,
                request.current_user
            )
            if updated_promotion:
                return Response({
                    "success": True,
                    "promotion": updated_promotion
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating promotion {promotion_id}: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @require_admin
    def delete(self, request, promotion_id):
        """Delete promotion"""
        try:
            deleted = self.promotion_service.delete_promotion(
                promotion_id,
                request.current_user
            )
            if deleted:
                return Response({
                    "success": True,
                    "message": "Promotion deleted successfully"
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting promotion {promotion_id}: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PromotionQRView(APIView):
    """View for promotion QR code management"""
    def __init__(self):
        self.promotion_service = PromotionService()

    @require_authentication
    def get(self, request, promotion_id):
        """Get promotion QR code"""
        try:
            promotion = self.promotion_service.get_promotion_by_id(promotion_id)
            if promotion:
                return Response({
                    "promotion_id": promotion.get('promotion_id', ''),
                    "promotion_name": promotion.get('promotion_name', ''),
                    "qr_code": promotion.get('qr_code', ''),
                    "discount_type": promotion.get('discount_type', ''),
                    "discount_value": promotion.get('discount_value', 0)
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting QR code for promotion {promotion_id}: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_admin
    def post(self, request, promotion_id):
        """Regenerate promotion QR code"""
        try:
            updated_promotion = self.promotion_service.regenerate_qr_code(
                promotion_id,
                request.current_user
            )
            if updated_promotion:
                return Response({
                    "success": True,
                    "message": "QR code regenerated successfully",
                    "qr_code": updated_promotion.get('qr_code', '')
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error regenerating QR code for promotion {promotion_id}: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PromotionQRScanView(APIView):
    """View for scanning promotion QR codes (POS integration)"""
    def __init__(self):
        self.promotion_service = PromotionService()

    @require_authentication
    def post(self, request):
        """Scan promotion QR code and return promotion details"""
        try:
            qr_code = request.data.get('qr_code', '').strip()
            if not qr_code:
                return Response(
                    {"error": "QR code is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            promotion = self.promotion_service.get_promotion_by_qr_code(qr_code)
            if promotion:
                return Response({
                    "promotion_id": promotion.get('promotion_id', ''),
                    "promotion_name": promotion.get('promotion_name', ''),
                    "discount_type": promotion.get('discount_type', ''),
                    "discount_value": promotion.get('discount_value', 0),
                    "applicable_products": promotion.get('applicable_products', []),
                    "start_date": promotion.get('start_date'),
                    "end_date": promotion.get('end_date'),
                    "status": promotion.get('status', 'active')
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Invalid QR code or promotion not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error scanning promotion QR code: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ActivePromotionsView(APIView):
    """View for getting active promotions"""
    def __init__(self):
        self.promotion_service = PromotionService()

    def get(self, request):
        """Get all active promotions"""
        try:
            active_promotions = self.promotion_service.get_active_promotions()
            return Response({
                "success": True,
                "promotions": active_promotions
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting active promotions: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PromotionApplyView(APIView):
    """View for applying promotions at checkout"""
    def __init__(self):
        self.promotion_service = PromotionService()

    @require_authentication
    def post(self, request):
        """Apply promotion code to cart"""
        try:
            promo_code = request.data.get('promo_code', '').strip()
            cart_items = request.data.get('cart_items', [])
            
            if not promo_code:
                return Response(
                    {"error": "Promo code is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not cart_items:
                return Response(
                    {"error": "Cart items are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get promotion by QR code or code
            promotion = self.promotion_service.get_promotion_by_qr_code(promo_code)
            if not promotion:
                return Response(
                    {"error": "Invalid promo code"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if promotion is active
            if promotion.get('status') != 'active':
                return Response(
                    {"error": "Promotion is not active"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Calculate discount
            discount = self.promotion_service.calculate_discount(promotion, cart_items)
            
            return Response({
                "success": True,
                "promotion": {
                    "id": promotion.get('_id'),
                    "name": promotion.get('promotion_name'),
                    "discount_type": promotion.get('discount_type'),
                    "discount_value": promotion.get('discount_value')
                },
                "discount": discount,
                "message": f"Promotion '{promotion.get('promotion_name')}' applied successfully!"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error applying promotion: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
