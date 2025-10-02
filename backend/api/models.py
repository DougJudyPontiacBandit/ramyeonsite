from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid
import hashlib


class User(AbstractUser):
    """Custom user model for the ramyeon application"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qr_code = models.CharField(max_length=200, unique=True, blank=True, null=True, help_text="Unique QR code for user identification")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate unique QR code for user if not exists
        if not self.qr_code:
            unique_string = f"USER-{self.username}-{uuid.uuid4().hex[:8]}"
            self.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        db_table = 'users'


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    """Products/Menu items"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']


class Voucher(models.Model):
    """Vouchers/Coupons"""
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=20,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')],
        default='percentage'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    usage_limit = models.IntegerField(default=0, help_text="0 means unlimited")
    usage_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    qr_code = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

    class Meta:
        db_table = 'vouchers'
        ordering = ['-created_at']


class UserVoucher(models.Model):
    """User's vouchers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vouchers')
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    obtained_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.voucher.code}"

    class Meta:
        db_table = 'user_vouchers'
        unique_together = ['user', 'voucher']


class Promotion(models.Model):
    """Promotions and deals"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    qr_code = models.CharField(max_length=200, unique=True, blank=True, null=True, help_text="Unique QR code for promotion")
    points_reward = models.IntegerField(default=0, help_text="Bonus points awarded when promotion is scanned")
    usage_limit_per_user = models.IntegerField(default=1, help_text="How many times a user can use this promotion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate unique QR code for promotion if not exists
        if not self.qr_code:
            unique_string = f"PROMO-{self.title}-{uuid.uuid4().hex[:8]}"
            self.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'promotions'
        ordering = ['-created_at']


class Cart(models.Model):
    """Shopping cart"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        db_table = 'carts'


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product']


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    DELIVERY_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='delivery')
    delivery_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    special_instructions = models.TextField(blank=True, null=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    voucher_used = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = 'order_items'


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'newsletter_subscriptions'
        ordering = ['-subscribed_at']


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

    class Meta:
        db_table = 'contact_messages'
        ordering = ['-created_at']


class PointsTransaction(models.Model):
    """Track all points transactions for users"""
    TRANSACTION_TYPES = [
        ('earned', 'Points Earned'),
        ('redeemed', 'Points Redeemed'),
        ('expired', 'Points Expired'),
        ('adjusted', 'Admin Adjustment'),
        ('bonus', 'Bonus Points'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    points = models.IntegerField()
    balance_after = models.IntegerField(help_text="User's point balance after this transaction")
    description = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='points_transactions')
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.points} points"

    class Meta:
        db_table = 'points_transactions'
        ordering = ['-created_at']


class LoyaltyReward(models.Model):
    """Rewards that users can redeem with their points"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='rewards/', blank=True, null=True)
    points_required = models.IntegerField(validators=[MinValueValidator(1)])
    discount_type = models.CharField(
        max_length=20,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount'), ('free_item', 'Free Item')],
        default='percentage'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, help_text="Product given for free")
    stock_quantity = models.IntegerField(default=0, help_text="Available quantity, 0 = unlimited")
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.points_required} points"

    class Meta:
        db_table = 'loyalty_rewards'
        ordering = ['points_required']


class UserReward(models.Model):
    """Track rewards claimed by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claimed_rewards')
    reward = models.ForeignKey(LoyaltyReward, on_delete=models.CASCADE)
    points_spent = models.IntegerField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    claimed_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"

    class Meta:
        db_table = 'user_rewards'
        ordering = ['-claimed_at']


class PromotionRedemption(models.Model):
    """Track when users redeem promotions via QR code"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promotion_redemptions')
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='redemptions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    points_awarded = models.IntegerField(default=0)
    scanned_by = models.CharField(max_length=200, help_text="Cashier who scanned the QR code")
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.promotion.title}"

    class Meta:
        db_table = 'promotion_redemptions'
        ordering = ['-redeemed_at']
