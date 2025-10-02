"""
POS (Point of Sale) Views for Cashier Operations
These endpoints are designed for cashier use to scan QR codes and process transactions
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from .models import (
    User, Promotion, PromotionRedemption, PointsTransaction,
    LoyaltyReward, UserReward, Order
)
from .serializers import (
    UserProfileSerializer, PromotionSerializer,
    PromotionRedemptionSerializer, PointsTransactionSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def scan_user_qr(request):
    """
    Scan user QR code to retrieve user information
    Used by cashiers to identify customers at checkout
    
    POST /api/pos/scan-user/
    Body: {"qr_code": "USER_QR_CODE_HERE"}
    """
    qr_code = request.data.get('qr_code')
    
    if not qr_code:
        return Response(
            {'error': 'QR code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(qr_code=qr_code)
        return Response({
            'success': True,
            'user': UserProfileSerializer(user).data,
            'message': f'Customer {user.get_full_name() or user.username} identified successfully'
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid QR code. User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def scan_promotion_qr(request):
    """
    Scan promotion QR code to retrieve promotion details
    Used by cashiers to apply promotions at checkout
    
    POST /api/pos/scan-promotion/
    Body: {"qr_code": "PROMO_QR_CODE_HERE"}
    """
    qr_code = request.data.get('qr_code')
    
    if not qr_code:
        return Response(
            {'error': 'QR code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        promotion = Promotion.objects.get(qr_code=qr_code, is_active=True)
        
        # Check if promotion is valid (date range)
        now = timezone.now()
        if promotion.valid_from > now or promotion.valid_until < now:
            return Response(
                {'error': 'This promotion has expired or is not yet active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'success': True,
            'promotion': PromotionSerializer(promotion).data,
            'message': f'Promotion "{promotion.title}" scanned successfully'
        }, status=status.HTTP_200_OK)
    except Promotion.DoesNotExist:
        return Response(
            {'error': 'Invalid promotion QR code'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def redeem_promotion(request):
    """
    Redeem a promotion for a user via QR code scan
    Cashier scans both user QR and promotion QR
    
    POST /api/pos/redeem-promotion/
    Body: {
        "user_qr_code": "USER_QR_CODE",
        "promotion_qr_code": "PROMO_QR_CODE",
        "cashier_name": "John Doe",
        "order_id": 123  // Optional
    }
    """
    user_qr = request.data.get('user_qr_code')
    promo_qr = request.data.get('promotion_qr_code')
    cashier_name = request.data.get('cashier_name', 'Unknown Cashier')
    order_id = request.data.get('order_id')
    
    if not user_qr or not promo_qr:
        return Response(
            {'error': 'Both user QR code and promotion QR code are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(qr_code=user_qr)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid user QR code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        promotion = Promotion.objects.get(qr_code=promo_qr, is_active=True)
    except Promotion.DoesNotExist:
        return Response(
            {'error': 'Invalid promotion QR code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if promotion is valid (date range)
    now = timezone.now()
    if promotion.valid_from > now or promotion.valid_until < now:
        return Response(
            {'error': 'This promotion has expired or is not yet active'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check usage limit per user
    redemption_count = PromotionRedemption.objects.filter(
        user=user,
        promotion=promotion
    ).count()
    
    if redemption_count >= promotion.usage_limit_per_user:
        return Response(
            {'error': f'User has already redeemed this promotion the maximum number of times ({promotion.usage_limit_per_user})'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create redemption record and award points
    with transaction.atomic():
        order = None
        if order_id:
            try:
                order = Order.objects.get(id=order_id, user=user)
            except Order.DoesNotExist:
                pass
        
        redemption = PromotionRedemption.objects.create(
            user=user,
            promotion=promotion,
            order=order,
            points_awarded=promotion.points_reward,
            scanned_by=cashier_name
        )
        
        # Award points if promotion has points reward
        if promotion.points_reward > 0:
            user.points += promotion.points_reward
            user.save()
            
            # Create points transaction record
            PointsTransaction.objects.create(
                user=user,
                transaction_type='bonus',
                points=promotion.points_reward,
                balance_after=user.points,
                description=f'Promotion bonus: {promotion.title}',
                promotion=promotion,
                order=order
            )
        
        return Response({
            'success': True,
            'redemption': PromotionRedemptionSerializer(redemption).data,
            'points_awarded': promotion.points_reward,
            'new_balance': user.points,
            'message': f'Promotion redeemed successfully! {promotion.points_reward} points awarded.'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def award_points_manual(request):
    """
    Manually award points to a user (for cashier use)
    
    POST /api/pos/award-points/
    Body: {
        "user_qr_code": "USER_QR_CODE",
        "points": 100,
        "description": "Birthday bonus",
        "cashier_name": "John Doe"
    }
    """
    user_qr = request.data.get('user_qr_code')
    points = request.data.get('points', 0)
    description = request.data.get('description', 'Manual points award')
    cashier_name = request.data.get('cashier_name', 'Unknown Cashier')
    
    if not user_qr:
        return Response(
            {'error': 'User QR code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not isinstance(points, int) or points <= 0:
        return Response(
            {'error': 'Points must be a positive integer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(qr_code=user_qr)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid user QR code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    with transaction.atomic():
        user.points += points
        user.save()
        
        transaction_record = PointsTransaction.objects.create(
            user=user,
            transaction_type='bonus',
            points=points,
            balance_after=user.points,
            description=f'{description} (by {cashier_name})'
        )
        
        return Response({
            'success': True,
            'transaction': PointsTransactionSerializer(transaction_record).data,
            'new_balance': user.points,
            'message': f'{points} points awarded successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def process_order_points(request):
    """
    Process points for an order (called when order is completed at POS)
    
    POST /api/pos/process-order-points/
    Body: {
        "user_qr_code": "USER_QR_CODE",
        "order_total": 500.00,
        "order_id": 123  // Optional
    }
    """
    user_qr = request.data.get('user_qr_code')
    order_total = request.data.get('order_total', 0)
    order_id = request.data.get('order_id')
    
    if not user_qr:
        return Response(
            {'error': 'User QR code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        order_total = float(order_total)
        if order_total <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response(
            {'error': 'Order total must be a positive number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(qr_code=user_qr)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid user QR code'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Calculate points (1 point per 10 pesos)
    points_earned = int(order_total / 10)
    
    with transaction.atomic():
        order = None
        if order_id:
            try:
                order = Order.objects.get(id=order_id, user=user)
                order.points_earned = points_earned
                order.save()
            except Order.DoesNotExist:
                pass
        
        user.points += points_earned
        user.save()
        
        transaction_record = PointsTransaction.objects.create(
            user=user,
            transaction_type='earned',
            points=points_earned,
            balance_after=user.points,
            description=f'Purchase points: ₱{order_total:.2f}',
            order=order
        )
        
        return Response({
            'success': True,
            'transaction': PointsTransactionSerializer(transaction_record).data,
            'points_earned': points_earned,
            'new_balance': user.points,
            'message': f'{points_earned} points earned from purchase!'
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def get_user_by_qr(request, qr_code):
    """
    Get user details by QR code (GET method for quick lookup)
    
    GET /api/pos/user/{qr_code}/
    """
    try:
        user = User.objects.get(qr_code=qr_code)
        
        # Get recent transactions
        recent_transactions = PointsTransaction.objects.filter(
            user=user
        ).order_by('-created_at')[:5]
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'recent_transactions': PointsTransactionSerializer(recent_transactions, many=True).data
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # In production, use custom POS permission
def get_promotion_by_qr(request, qr_code):
    """
    Get promotion details by QR code (GET method for quick lookup)
    
    GET /api/pos/promotion/{qr_code}/
    """
    try:
        promotion = Promotion.objects.get(qr_code=qr_code)
        
        # Check if active
        now = timezone.now()
        is_valid = (
            promotion.is_active and 
            promotion.valid_from <= now <= promotion.valid_until
        )
        
        return Response({
            'promotion': PromotionSerializer(promotion).data,
            'is_valid': is_valid,
            'status_message': 'Valid' if is_valid else 'Expired or Inactive'
        }, status=status.HTTP_200_OK)
    except Promotion.DoesNotExist:
        return Response(
            {'error': 'Promotion not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def pos_dashboard(request):
    """
    Get POS dashboard statistics
    
    GET /api/pos/dashboard/
    """
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Today's statistics
    today_orders = Order.objects.filter(created_at__date=today)
    today_redemptions = PromotionRedemption.objects.filter(redeemed_at__date=today)
    
    # This week's statistics
    week_orders = Order.objects.filter(created_at__date__gte=week_ago)
    week_points_awarded = PointsTransaction.objects.filter(
        created_at__date__gte=week_ago,
        transaction_type__in=['earned', 'bonus']
    ).aggregate(total=Sum('points'))['total'] or 0
    
    return Response({
        'today': {
            'orders_count': today_orders.count(),
            'total_sales': float(today_orders.aggregate(total=Sum('total_amount'))['total'] or 0),
            'promotions_redeemed': today_redemptions.count(),
        },
        'this_week': {
            'orders_count': week_orders.count(),
            'total_sales': float(week_orders.aggregate(total=Sum('total_amount'))['total'] or 0),
            'points_awarded': week_points_awarded,
        },
        'active_promotions': Promotion.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        ).count()
    }, status=status.HTTP_200_OK)
