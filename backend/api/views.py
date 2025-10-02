from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import jwt
from django.conf import settings

from .models import (
    User, Category, Product, Voucher, UserVoucher,
    Promotion, Cart, CartItem, Order, OrderItem,
    Newsletter, ContactMessage, PointsTransaction,
    LoyaltyReward, UserReward, PromotionRedemption
)
from .serializers import (
    UserSerializer, UserProfileSerializer, LoginSerializer,
    CategorySerializer, ProductSerializer, VoucherSerializer,
    UserVoucherSerializer, PromotionSerializer, CartSerializer,
    CartItemSerializer, OrderSerializer, OrderCreateSerializer,
    NewsletterSerializer, ContactMessageSerializer,
    PointsTransactionSerializer, LoyaltyRewardSerializer,
    UserRewardSerializer, PromotionRedemptionSerializer
)


def generate_tokens(user):
    """Generate JWT access and refresh tokens"""
    access_token_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow()
    }
    
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        'iat': datetime.utcnow()
    }
    
    access_token = jwt.encode(access_token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_token_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return access_token, refresh_token


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """User registration endpoint"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create cart for user
        Cart.objects.create(user=user)
        
        # Generate tokens
        access_token, refresh_token = generate_tokens(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': UserProfileSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Generate tokens
        access_token, refresh_token = generate_tokens(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserProfileSerializer(user).data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Get user profile"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Update user profile"""
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        return queryset


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product model"""
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by featured
        is_featured = self.request.query_params.get('featured', None)
        if is_featured:
            queryset = queryset.filter(is_featured=True)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


class VoucherViewSet(viewsets.ModelViewSet):
    """ViewSet for Voucher model"""
    queryset = Voucher.objects.filter(is_active=True)
    serializer_class = VoucherSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Voucher.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        )
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def claim(self, request, pk=None):
        """Claim a voucher for the current user"""
        voucher = self.get_object()
        
        # Check if already claimed
        if UserVoucher.objects.filter(user=request.user, voucher=voucher).exists():
            return Response(
                {'error': 'Voucher already claimed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check usage limit
        if voucher.usage_limit > 0 and voucher.usage_count >= voucher.usage_limit:
            return Response(
                {'error': 'Voucher usage limit reached'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user voucher
        user_voucher = UserVoucher.objects.create(user=request.user, voucher=voucher)
        
        return Response(
            UserVoucherSerializer(user_voucher).data,
            status=status.HTTP_201_CREATED
        )


class PromotionViewSet(viewsets.ModelViewSet):
    """ViewSet for Promotion model"""
    queryset = Promotion.objects.filter(is_active=True)
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Promotion.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        )
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for Cart model"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get current user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found or unavailable'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        if product.stock_quantity < quantity:
            return Response(
                {'error': 'Insufficient stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item quantity"""
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response({'message': 'Item removed from cart'})
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order model"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order from cart"""
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Clear cart after order
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cannot cancel order in current status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        return Response(OrderSerializer(order).data)


class UserVoucherViewSet(viewsets.ModelViewSet):
    """ViewSet for UserVoucher model"""
    serializer_class = UserVoucherSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserVoucher.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available vouchers for user"""
        vouchers = UserVoucher.objects.filter(
            user=request.user,
            is_used=False,
            voucher__is_active=True,
            voucher__valid_until__gte=timezone.now()
        )
        serializer = self.get_serializer(vouchers, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def subscribe_newsletter(request):
    """Subscribe to newsletter"""
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    newsletter, created = Newsletter.objects.get_or_create(email=email)
    
    if not created and newsletter.is_active:
        return Response(
            {'message': 'Already subscribed'},
            status=status.HTTP_200_OK
        )
    
    newsletter.is_active = True
    newsletter.save()
    
    return Response(
        {'message': 'Successfully subscribed to newsletter'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_message(request):
    """Submit contact form"""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Message sent successfully'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Points and Loyalty Endpoints

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_points_history(request):
    """Get user's points transaction history"""
    transactions = PointsTransaction.objects.filter(user=request.user)
    serializer = PointsTransactionSerializer(transactions, many=True)
    return Response({
        'current_points': request.user.points,
        'transactions': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_qr_code(request):
    """Get authenticated user's QR code"""
    user = request.user
    return Response({
        'qr_code': user.qr_code,
        'username': user.username,
        'email': user.email,
        'points': user.points
    })


class LoyaltyRewardViewSet(viewsets.ModelViewSet):
    """ViewSet for Loyalty Rewards"""
    serializer_class = LoyaltyRewardSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = LoyaltyReward.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_until__gte=timezone.now()
        )
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def redeem(self, request, pk=None):
        """Redeem a loyalty reward"""
        reward = self.get_object()
        user = request.user
        
        # Check if user has enough points
        if user.points < reward.points_required:
            return Response(
                {'error': f'Insufficient points. You need {reward.points_required} points but have {user.points}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check stock
        if reward.stock_quantity > 0:
            if reward.stock_quantity < 1:
                return Response(
                    {'error': 'This reward is out of stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create reward redemption
        with transaction.atomic():
            # Deduct points
            user.points -= reward.points_required
            user.save()
            
            # Create points transaction
            PointsTransaction.objects.create(
                user=user,
                transaction_type='redeemed',
                points=-reward.points_required,
                balance_after=user.points,
                description=f'Redeemed reward: {reward.name}'
            )
            
            # Create user reward
            expires_at = timezone.now() + timedelta(days=30)  # Reward expires in 30 days
            user_reward = UserReward.objects.create(
                user=user,
                reward=reward,
                points_spent=reward.points_required,
                expires_at=expires_at
            )
            
            # Update stock
            if reward.stock_quantity > 0:
                reward.stock_quantity -= 1
                reward.save()
            
            return Response(
                UserRewardSerializer(user_reward).data,
                status=status.HTTP_201_CREATED
            )


class UserRewardViewSet(viewsets.ModelViewSet):
    """ViewSet for User Rewards"""
    serializer_class = UserRewardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserReward.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available (unused and not expired) rewards"""
        rewards = UserReward.objects.filter(
            user=request.user,
            is_used=False,
            expires_at__gte=timezone.now()
        )
        serializer = self.get_serializer(rewards, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def use(self, request, pk=None):
        """Mark a reward as used"""
        user_reward = self.get_object()
        
        if user_reward.is_used:
            return Response(
                {'error': 'This reward has already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_reward.expires_at < timezone.now():
            return Response(
                {'error': 'This reward has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_reward.is_used = True
        user_reward.used_at = timezone.now()
        user_reward.save()
        
        return Response(
            UserRewardSerializer(user_reward).data,
            status=status.HTTP_200_OK
        )


class PointsTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Points Transactions (read-only)"""
    serializer_class = PointsTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PointsTransaction.objects.filter(user=self.request.user)


class PromotionRedemptionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Promotion Redemptions (read-only)"""
    serializer_class = PromotionRedemptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PromotionRedemption.objects.filter(user=self.request.user)
