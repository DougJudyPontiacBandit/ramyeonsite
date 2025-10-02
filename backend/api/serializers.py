from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, Category, Product, Voucher, UserVoucher,
    Promotion, Cart, CartItem, Order, OrderItem,
    Newsletter, ContactMessage, PointsTransaction,
    LoyaltyReward, UserReward, PromotionRedemption
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 
                  'first_name', 'last_name', 'phone', 'points', 
                  'date_of_birth', 'address', 'created_at']
        read_only_fields = ['id', 'points', 'created_at']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (without password)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'points', 'date_of_birth', 'address', 'qr_code', 'created_at']
        read_only_fields = ['id', 'username', 'email', 'points', 'qr_code', 'created_at']


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')

        attrs['user'] = user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'is_active', 
                  'products_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_products_count(self, obj):
        return obj.products.filter(is_available=True).count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'category_name', 
                  'price', 'image', 'is_available', 'is_featured', 
                  'stock_quantity', 'created_at']
        read_only_fields = ['id', 'created_at']


class VoucherSerializer(serializers.ModelSerializer):
    """Serializer for Voucher model"""
    class Meta:
        model = Voucher
        fields = ['id', 'code', 'title', 'subtitle', 'description', 
                  'discount_type', 'discount_value', 'min_purchase_amount',
                  'max_discount_amount', 'valid_from', 'valid_until',
                  'usage_limit', 'usage_count', 'is_active', 'qr_code']
        read_only_fields = ['id', 'usage_count']


class UserVoucherSerializer(serializers.ModelSerializer):
    """Serializer for UserVoucher model"""
    voucher = VoucherSerializer(read_only=True)
    voucher_id = serializers.PrimaryKeyRelatedField(
        queryset=Voucher.objects.all(), 
        source='voucher', 
        write_only=True
    )

    class Meta:
        model = UserVoucher
        fields = ['id', 'voucher', 'voucher_id', 'is_used', 
                  'used_at', 'obtained_at']
        read_only_fields = ['id', 'is_used', 'used_at', 'obtained_at']


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Promotion
        fields = ['id', 'title', 'description', 'image', 'discount_percentage',
                  'product', 'product_name', 'category', 'category_name',
                  'valid_from', 'valid_until', 'is_active', 'qr_code', 
                  'points_reward', 'usage_limit_per_user', 'created_at']
        read_only_fields = ['id', 'qr_code', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'subtotal', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 
                  'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'user_email', 'order_number', 
                  'status', 'delivery_type', 'delivery_address', 
                  'payment_method', 'special_instructions', 'subtotal',
                  'delivery_fee', 'service_fee', 'discount_amount', 
                  'total_amount', 'voucher_used', 'points_earned', 
                  'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['delivery_type', 'delivery_address', 'payment_method',
                  'special_instructions', 'voucher_used', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate totals
        subtotal = sum(item['total_price'] for item in items_data)
        delivery_fee = 50 if validated_data['delivery_type'] == 'delivery' else 0
        service_fee = subtotal * 0.05
        
        # Apply voucher discount if any
        discount_amount = 0
        voucher = validated_data.get('voucher_used')
        if voucher:
            if voucher.discount_type == 'percentage':
                discount_amount = (subtotal * voucher.discount_value) / 100
                if voucher.max_discount_amount:
                    discount_amount = min(discount_amount, voucher.max_discount_amount)
            else:
                discount_amount = voucher.discount_value
        
        total_amount = subtotal + delivery_fee + service_fee - discount_amount
        
        # Generate order number
        import uuid
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate points earned (1 point per 10 pesos)
        points_earned = int(total_amount / 10)
        
        # Create order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            service_fee=service_fee,
            discount_amount=discount_amount,
            total_amount=total_amount,
            points_earned=points_earned,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Update user points and create transaction record
        user.points += points_earned
        user.save()
        
        # Create points transaction record
        PointsTransaction.objects.create(
            user=user,
            transaction_type='earned',
            points=points_earned,
            balance_after=user.points,
            description=f'Order #{order.order_number} - ₱{total_amount:.2f}',
            order=order
        )
        
        # Mark voucher as used if applicable
        if voucher:
            voucher.usage_count += 1
            voucher.save()
            
            # Create transaction for voucher usage if applicable
            if voucher.usage_count == 1:  # First use
                PointsTransaction.objects.create(
                    user=user,
                    transaction_type='adjusted',
                    points=0,
                    balance_after=user.points,
                    description=f'Applied voucher: {voucher.code}',
                    order=order
                )
        
        return order


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for Newsletter model"""
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'is_active', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'is_read', 'created_at']


class PointsTransactionSerializer(serializers.ModelSerializer):
    """Serializer for PointsTransaction model"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    promotion_title = serializers.CharField(source='promotion.title', read_only=True)

    class Meta:
        model = PointsTransaction
        fields = ['id', 'user', 'user_name', 'transaction_type', 'points', 
                  'balance_after', 'description', 'order', 'order_number',
                  'promotion', 'promotion_title', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoyaltyRewardSerializer(serializers.ModelSerializer):
    """Serializer for LoyaltyReward model"""
    free_product_name = serializers.CharField(source='free_product.name', read_only=True)

    class Meta:
        model = LoyaltyReward
        fields = ['id', 'name', 'description', 'image', 'points_required',
                  'discount_type', 'discount_value', 'free_product', 'free_product_name',
                  'stock_quantity', 'is_active', 'valid_from', 'valid_until', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRewardSerializer(serializers.ModelSerializer):
    """Serializer for UserReward model"""
    reward = LoyaltyRewardSerializer(read_only=True)
    reward_id = serializers.PrimaryKeyRelatedField(
        queryset=LoyaltyReward.objects.all(),
        source='reward',
        write_only=True
    )

    class Meta:
        model = UserReward
        fields = ['id', 'reward', 'reward_id', 'points_spent', 'is_used',
                  'used_at', 'claimed_at', 'expires_at']
        read_only_fields = ['id', 'is_used', 'used_at', 'claimed_at']


class PromotionRedemptionSerializer(serializers.ModelSerializer):
    """Serializer for PromotionRedemption model"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    promotion_title = serializers.CharField(source='promotion.title', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)

    class Meta:
        model = PromotionRedemption
        fields = ['id', 'user', 'user_name', 'promotion', 'promotion_title',
                  'order', 'order_number', 'points_awarded', 'scanned_by', 'redeemed_at']
        read_only_fields = ['id', 'redeemed_at']
