from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Category, Product, Voucher, UserVoucher, 
    Promotion, Cart, CartItem, Order, OrderItem,
    Newsletter, ContactMessage, PointsTransaction,
    LoyaltyReward, UserReward, PromotionRedemption
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'points', 'qr_code', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'qr_code']
    readonly_fields = ['qr_code']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'points', 'date_of_birth', 'address', 'qr_code')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured']


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'discount_type', 'discount_value', 'valid_from', 'valid_until', 'is_active']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'title']
    list_editable = ['is_active']


@admin.register(UserVoucher)
class UserVoucherAdmin(admin.ModelAdmin):
    list_display = ['user', 'voucher', 'is_used', 'obtained_at', 'used_at']
    list_filter = ['is_used', 'obtained_at']
    search_fields = ['user__username', 'voucher__code']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percentage', 'points_reward', 'qr_code', 'valid_from', 'valid_until', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_until']
    search_fields = ['title', 'description', 'qr_code']
    readonly_fields = ['qr_code']
    list_editable = ['is_active']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'subtotal', 'created_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'delivery_type', 'total_amount', 'created_at']
    list_filter = ['status', 'delivery_type', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    list_editable = ['status']
    inlines = [OrderItemInline]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'points', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(LoyaltyReward)
class LoyaltyRewardAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'discount_type', 'discount_value', 'stock_quantity', 'is_active']
    list_filter = ['is_active', 'discount_type', 'valid_from', 'valid_until']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'stock_quantity']


@admin.register(UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'reward', 'points_spent', 'is_used', 'claimed_at', 'expires_at']
    list_filter = ['is_used', 'claimed_at', 'expires_at']
    search_fields = ['user__username', 'reward__name']
    readonly_fields = ['claimed_at']


@admin.register(PromotionRedemption)
class PromotionRedemptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'promotion', 'points_awarded', 'scanned_by', 'redeemed_at']
    list_filter = ['redeemed_at']
    search_fields = ['user__username', 'promotion__title', 'scanned_by']
    readonly_fields = ['redeemed_at']
    date_hierarchy = 'redeemed_at'
