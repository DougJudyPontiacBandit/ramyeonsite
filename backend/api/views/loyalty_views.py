from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from api.services.loyalty_service import LoyaltyService
from api.utils.jwt_utils import jwt_required
import logging

logger = logging.getLogger(__name__)

loyalty_service = LoyaltyService()

@api_view(['GET'])
@jwt_required
def get_loyalty_balance(request):
    """Get customer's loyalty points balance"""
    try:
        customer_id = request.customer['customer_id']
        
        balance = loyalty_service.get_customer_points(customer_id)
        
        if not balance:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'success': True,
            'balance': balance
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Get loyalty balance error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@jwt_required
def get_loyalty_history(request):
    """Get customer's loyalty points transaction history"""
    try:
        customer_id = request.customer['customer_id']
        limit = request.GET.get('limit', 50)
        
        history = loyalty_service.get_points_history(customer_id, int(limit))
        
        return Response({
            'success': True,
            'history': history
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Get loyalty history error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@jwt_required
@csrf_exempt
def validate_points_redemption(request):
    """Validate if customer can redeem points"""
    try:
        customer_id = request.customer['customer_id']
        points_to_redeem = request.data.get('points_to_redeem')
        
        if not points_to_redeem:
            return Response(
                {'error': 'Points to redeem is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_valid, message = loyalty_service.validate_points_redemption(
            customer_id, int(points_to_redeem)
        )
        
        return Response({
            'success': is_valid,
            'message': message,
            'can_redeem': is_valid
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Validate points redemption error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@jwt_required
@csrf_exempt
def redeem_points(request):
    """Redeem customer points"""
    try:
        customer_id = request.customer['customer_id']
        points_to_redeem = request.data.get('points_to_redeem')
        order_id = request.data.get('order_id')
        
        if not points_to_redeem or not order_id:
            return Response(
                {'error': 'Points to redeem and order ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, result = loyalty_service.redeem_points(
            customer_id, int(points_to_redeem), order_id
        )
        
        if not success:
            return Response(
                {'error': result},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'success': True,
            'redemption': result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Redeem points error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@jwt_required
@csrf_exempt
def award_points(request):
    """Award points to customer after successful order"""
    try:
        customer_id = request.customer['customer_id']
        order_amount = request.data.get('order_amount')
        order_id = request.data.get('order_id')
        
        if not order_amount or not order_id:
            return Response(
                {'error': 'Order amount and order ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, result = loyalty_service.award_points(
            customer_id, float(order_amount), order_id
        )
        
        if not success:
            return Response(
                {'error': result},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'success': True,
            'award': result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Award points error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def loyalty_health_check(request):
    """Health check for loyalty service"""
    try:
        return Response({
            'status': 'healthy',
            'service': 'loyalty_points',
            'message': 'Loyalty points service is running'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Service unhealthy'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




