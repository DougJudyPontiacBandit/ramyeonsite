<template>
  <div class="cart-page">
    <div class="cart-container">
      <!-- Cart Header -->
      <div class="cart-header">
        <h1>Your Cart</h1>
        <p v-if="cartItems.length === 0">Your cart is empty</p>
        <p v-else>{{ cartItems.length }} item{{ cartItems.length > 1 ? 's' : '' }} in your cart</p>
      </div>

      <div class="cart-content" v-if="cartItems.length > 0">
        <!-- Cart Items -->
        <div class="cart-items">
          <div class="cart-item" v-for="item in cartItems" :key="item.id">
            <img :src="item.image" :alt="item.name" class="item-image" />
            <div class="item-details">
              <h3>{{ item.name }}</h3>
              <p class="item-description">{{ item.description }}</p>
              <div class="item-price-section">
                <div class="item-price" :class="{ 'has-discount': getItemDiscount(item) > 0 }">
                  <span v-if="getItemDiscount(item) > 0" class="original-price">₱{{ item.price }}</span>
                  <span class="current-price">₱{{ getItemDiscountedPrice(item).toFixed(2) }}</span>
                </div>
                <div v-if="getItemDiscount(item) > 0" class="item-discount-info">
                  <span class="discount-badge">{{ getItemDiscountText(item) }}</span>
                  <span class="savings">You save ₱{{ getItemDiscount(item).toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <div class="item-controls">
              <button class="quantity-btn" @click="decreaseQuantity(item.id)">-</button>
              <span class="quantity">{{ item.quantity }}</span>
              <button class="quantity-btn" @click="increaseQuantity(item.id)">+</button>
            </div>
            <div class="item-total">
              <div v-if="getItemDiscount(item) > 0" class="total-with-discount">
                <span class="original-total">₱{{ (item.price * item.quantity).toFixed(2) }}</span>
                <span class="discounted-total">₱{{ (getItemDiscountedPrice(item) * item.quantity).toFixed(2) }}</span>
              </div>
              <div v-else class="regular-total">₱{{ (item.price * item.quantity).toFixed(2) }}</div>
            </div>
            <button class="remove-btn" @click="removeItem(item.id)">×</button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="order-summary">
          <h2>Order Summary</h2>
          <div class="summary-row">
            <span>Subtotal</span>
            <span>₱{{ subtotal.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>Delivery Fee</span>
            <span>₱{{ deliveryFee.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>Service Fee</span>
            <span>₱{{ serviceFee.toFixed(2) }}</span>
          </div>
          
          <!-- Loyalty Points Section -->
          <div class="loyalty-points-section" v-if="userProfile">
            <div class="points-header">
              <div class="points-info">
                <span class="points-icon">⭐</span>
                <span class="points-label">Your Points:</span>
                <span class="points-balance">{{ userProfile.loyalty_points || 0 }}</span>
                <span class="points-value">(₱{{ ((userProfile.loyalty_points || 0) / 4).toFixed(2) }} value)</span>
              </div>
            </div>
            
            <div class="points-redemption">
              <label class="points-checkbox">
                <input 
                  type="checkbox" 
                  v-model="useLoyaltyPoints"
                  @change="onPointsToggle"
                />
                <span class="checkbox-text">Use loyalty points</span>
              </label>
              
              <div v-if="useLoyaltyPoints && (userProfile.loyalty_points || 0) >= 40" class="points-input-group">
                <input 
                  type="number" 
                  v-model="pointsToRedeem" 
                  :min="40"
                  :max="maxPointsToRedeem"
                  placeholder="Points to use (40-80 max)"
                  class="points-input"
                  @input="onPointsChange"
                />
                <span class="points-discount">= ₱{{ pointsDiscount.toFixed(2) }} off</span>
                <div class="points-rates">
                  <small>40 pts = ₱10 | 80 pts = ₱20 (max per order)</small>
                </div>
              </div>
              <div v-else-if="useLoyaltyPoints && (userProfile.loyalty_points || 0) < 40" class="points-insufficient">
                <span class="insufficient-message">⚠️ You need at least 40 points to redeem (₱10 minimum)</span>
              </div>
            </div>
          </div>

          <!-- Promotion Code Input -->
          <div class="promo-code-section">
            <div class="promo-input-group">
              <input 
                type="text" 
                v-model="promoCode" 
                placeholder="Enter promo code"
                class="promo-input"
                :disabled="appliedPromotion"
                @keyup.enter="applyPromoCode"
              />
              <button 
                v-if="!appliedPromotion"
                class="apply-promo-btn" 
                @click="applyPromoCode"
                :disabled="!promoCode || applyingPromo"
              >
                <span v-if="!applyingPromo">Apply</span>
                <span v-else class="loading-spinner-small"></span>
              </button>
              <button 
                v-else
                class="remove-promo-btn" 
                @click="removePromoCode"
              >
                Remove
              </button>
            </div>
            
            <!-- Applied Promotion Display -->
            <div v-if="appliedPromotion" class="applied-promo">
              <div class="promo-badge">
                <span class="promo-icon">🎁</span>
                <span class="promo-name">{{ appliedPromotion.name }}</span>
              </div>
              <div class="promo-discount-info">
                {{ getPromotionDescription(appliedPromotion) }}
              </div>
            </div>
            
            <!-- Promo Error Message -->
            <div v-if="promoError" class="promo-error">
              <span class="error-icon">⚠️</span>
              {{ promoError }}
            </div>
          </div>
          
          <!-- Points Discount Row (if points used) -->
          <div v-if="pointsDiscount > 0" class="summary-row points-discount-row">
            <span>Points Discount</span>
            <span class="discount-amount">-₱{{ pointsDiscount.toFixed(2) }}</span>
          </div>
          
          <!-- Promotion Discount Row (if promotion applied) -->
          <div v-if="promotionDiscount > 0" class="summary-row discount-row">
            <span>Promotion Discount</span>
            <span class="discount-amount">-₱{{ promotionDiscount.toFixed(2) }}</span>
          </div>
          
          <div class="summary-row total">
            <span>Total</span>
            <span>₱{{ finalTotal.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Delivery Options -->
        <div class="delivery-options">
          <h2>Delivery Options</h2>
          <div class="option-group">
            <label class="option-label">
              <input type="radio" v-model="deliveryType" value="delivery" />
              <div class="option-content">
                <div class="option-icon">🚚</div>
                <div class="option-text">
                  <h3>Delivery</h3>
                  <p>Get it delivered to your doorstep</p>
                  <span class="option-time">30-45 mins</span>
                </div>
              </div>
            </label>
            <label class="option-label">
              <input type="radio" v-model="deliveryType" value="pickup" />
              <div class="option-content">
                <div class="option-icon">🏪</div>
                <div class="option-text">
                  <h3>Pickup</h3>
                  <p>Pick up from our store</p>
                  <span class="option-time">15-20 mins</span>
                </div>
              </div>
            </label>
          </div>
        </div>

        <!-- Delivery Address (only show if delivery is selected) -->
        <div class="delivery-address" v-if="deliveryType === 'delivery'">
          <h2>Delivery Address</h2>
          <div class="address-input">
            <input 
              type="text" 
              v-model="deliveryAddress" 
              placeholder="Enter your delivery address"
              class="address-field"
            />
            <button class="map-btn" @click="openMap">📍 Use Map</button>
          </div>
          
          <!-- Google Map -->
          <div class="map-container" v-if="showMap">
            <p class="map-instructions">📍 Click anywhere on the map to set your delivery location</p>
            <div id="google-map" class="google-map"></div>
            <button class="close-map-btn" @click="closeMap">Close Map</button>
          </div>
        </div>

        <!-- Payment Methods -->
        <div class="payment-methods">
          <h2>Payment Method</h2>
          <div class="payment-options">
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="cash" />
              <div class="payment-content">
                <div class="payment-icon">💵</div>
                <span>Cash on Delivery</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="gcash" />
              <div class="payment-content">
                <div class="payment-icon">📱</div>
                <span>GCash</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="card" />
              <div class="payment-content">
                <div class="payment-icon">💳</div>
                <span>Credit/Debit Card</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="paymaya" />
              <div class="payment-content">
                <div class="payment-icon">🏦</div>
                <span>PayMaya</span>
              </div>
            </label>
            <label class="payment-option">
              <input type="radio" v-model="paymentMethod" value="grabpay" />
              <div class="payment-content">
                <div class="payment-icon">🎯</div>
                <span>GrabPay QR</span>
              </div>
            </label>
          </div>
        </div>

        <!-- Special Instructions -->
        <div class="special-instructions">
          <h2>Special Instructions</h2>
          <textarea 
            v-model="specialInstructions" 
            placeholder="Any special requests or instructions for your order..."
            class="instructions-field"
          ></textarea>
        </div>

        <!-- Checkout Button -->
        <div class="checkout-section">
          <button class="checkout-btn" @click="proceedToCheckout" :disabled="!canCheckout">
            <span v-if="isProcessing" class="loading-spinner"></span>
            {{ isProcessing ? 'Processing...' : `Place Order - ₱${finalTotal.toFixed(2)}` }}
          </button>
        </div>
      </div>

      <!-- Empty Cart State -->
      <div class="empty-cart" v-else>
        <div class="empty-cart-icon">🛒</div>
        <h2>Your cart is empty</h2>
        <p>Add some delicious ramyeon to get started!</p>
        <button class="browse-menu-btn" @click="$emit('setCurrentPage', 'Menu')">
          Browse Menu
        </button>
      </div>
    </div>

    <!-- Order Confirmation Modal - FORCE TO BODY LEVEL -->
    <teleport to="body">
      <transition name="modal-fade">
        <div v-if="showOrderConfirmation" class="confirmation-modal-overlay" @click="closeConfirmationModal">
        <div class="confirmation-modal" @click.stop>
          <div class="confirmation-success-icon">
            <div class="checkmark-circle">
              <div class="checkmark"></div>
            </div>
          </div>
          
          <h2 class="confirmation-title">Order Placed Successfully! 🎉</h2>
        
        <div class="confirmation-details">
          <div class="detail-row">
            <span class="detail-label">Order ID:</span>
            <span class="detail-value order-id">{{ confirmedOrder.id }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Total Amount:</span>
            <span class="detail-value total-amount">₱{{ confirmedOrder.total }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Payment Method:</span>
            <span class="detail-value">{{ confirmedOrder.paymentMethod?.toUpperCase() }}</span>
          </div>
          
          <div class="detail-row">
            <span class="detail-label">Delivery Type:</span>
            <span class="detail-value">{{ confirmedOrder.deliveryType === 'delivery' ? 'Delivery 🚚' : 'Pickup 🏪' }}</span>
          </div>
          
          <div class="detail-row estimated-time">
            <span class="detail-label">Estimated Time:</span>
            <span class="detail-value">{{ confirmedOrder.deliveryType === 'delivery' ? '30-45' : '15-20' }} minutes</span>
          </div>
          
          <!-- Loyalty Points Info -->
          <div v-if="confirmedOrder.pointsEarned > 0 || confirmedOrder.pointsUsed > 0" class="loyalty-points-summary">
            <div v-if="confirmedOrder.pointsUsed > 0" class="detail-row">
              <span class="detail-label">Points Used:</span>
              <span class="detail-value points-used">-{{ confirmedOrder.pointsUsed }} points</span>
            </div>
            <div v-if="confirmedOrder.pointsEarned > 0" class="detail-row">
              <span class="detail-label">Points Earned:</span>
              <span class="detail-value points-earned">+{{ confirmedOrder.pointsEarned }} points</span>
            </div>
          </div>
        </div>
        
        <div class="confirmation-message">
          <p>✅ Your order has been sent to our kitchen!</p>
          <p>📱 You'll receive updates on your order status.</p>
          <p v-if="confirmedOrder.pointsEarned > 0">⭐ You earned {{ confirmedOrder.pointsEarned }} loyalty points!</p>
        </div>
        
        <button class="confirmation-btn" @click="goToHome">
          Back to Home
        </button>
          </div>
        </div>
      </transition>
    </teleport>
    
    
    
  </div>
</template>

<script>
import { paymongoAPI } from '../composables/usePaymongo.js';
import { authAPI } from '../services/api.js';
import { useOnlineOrder } from '../composables/api/useOnlineOrder.js';
import { useProducts } from '../composables/api/useProducts.js';
import { usePromotions } from '../composables/api/usePromotions.js';
import { useLoyalty } from '../composables/api/useLoyalty.js';

// Toggle verbose cart logging via env: VITE_DEBUG_CART=true or VUE_APP_DEBUG_CART=true
const CART_DEBUG = (
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_DEBUG_CART === 'true') ||
  (typeof process !== 'undefined' && process.env && process.env.VUE_APP_DEBUG_CART === 'true')
);

export default {
  name: 'Cart',
  emits: ['setCurrentPage'],
  setup() {
    // Initialize composables
    const onlineOrder = useOnlineOrder();
    const products = useProducts();
    const promotions = usePromotions();
    const loyalty = useLoyalty();
    
    return {
      // Expose composable methods and state
      ...onlineOrder,
      ...products,
      ...promotions,
      ...loyalty
    };
  },
  data() {
    return {
      // Keep existing data properties for backward compatibility
      deliveryType: 'delivery',
      deliveryAddress: '',
      paymentMethod: 'cash',
      specialInstructions: '',
      showMap: false,
      isProcessing: false,
      map: null,
      marker: null,
      // Card payment details
      showCardForm: false,
      cardDetails: {
        number: '',
        exp_month: '',
        exp_year: '',
        cvc: '',
        name: ''
      },
      userProfile: null,
      // Order confirmation modal
      showOrderConfirmation: false,
      confirmedOrder: {},
      // Promotion code
      promoCode: '',
      appliedPromotion: null,
      promotionDiscount: 0,
      applyingPromo: false,
      promoError: null,
      // Loyalty points
      useLoyaltyPoints: false,
      pointsToRedeem: 0,
      pointsDiscount: 0,
      maxPointsToRedeem: 0
    }
  },
  computed: {
    // Use composable cart data
    subtotal() {
      // Calculate subtotal using discounted prices for each item
      return this.cartItems.reduce((total, item) => {
        const discountedPrice = this.getItemDiscountedPrice(item);
        return total + (discountedPrice * item.quantity);
      }, 0);
    },
    deliveryFee() {
      return this.cartShipping;
    },
    serviceFee() {
      return this.cartTax;
    },
    total() {
      return this.cartTotal;
    },
    finalTotal() {
      return this.cartTotalWithAdjustments;
    },
    canCheckout() {
      const hasItems = this.cartItems.length > 0;
      const hasPayment = this.paymentMethod !== '';
      const hasAddress = this.deliveryType === 'pickup' || (this.deliveryType === 'delivery' && this.deliveryAddress.trim() !== '');
      return hasItems && hasPayment && hasAddress && !this.isProcessing;
    }
  },
  methods: {
    // Use composable cart methods
    async increaseQuantity(itemId) {
      const item = this.cartItems.find(item => item.id === itemId);
      if (item) {
        await this.updateCartItemQuantity(item.product_id || item.id, item.quantity + 1);
      }
    },
    async decreaseQuantity(itemId) {
      const item = this.cartItems.find(item => item.id === itemId);
      if (item && item.quantity > 1) {
        await this.updateCartItemQuantity(item.product_id || item.id, item.quantity - 1);
      }
    },
    async removeItem(itemId) {
      const item = this.cartItems.find(item => item.id === itemId);
      if (item) {
        await this.removeFromCart(item.product_id || item.id);
      }
    },
    
    // Loyalty Points Methods - Use composable
    async onPointsToggle() {
      if (this.useLoyaltyPoints) {
        // Initialize with minimum points
        this.pointsToRedeem = Math.min(40, this.loyaltyBalance);
        await this.calculatePointsDiscount();
      } else {
        this.pointsToRedeem = 0;
        this.pointsDiscount = 0;
        this.removeLoyaltyPoints();
      }
    },
    
    async onPointsChange() {
      await this.calculatePointsDiscount();
    },
    
    async calculatePointsDiscount() {
      if (!this.useLoyaltyPoints || !this.pointsToRedeem) {
        this.pointsDiscount = 0;
        return;
      }
      
      try {
        // Use composable to calculate points discount
        const result = await this.calculatePointsDiscount(
          this.pointsToRedeem, 
          { id: this.userProfile?.id }, 
          this.currentTier
        );
        
        if (result.success) {
          this.pointsDiscount = result.data.discount_amount;
          
          // Calculate max points that can be used
          const maxDiscount = Math.min(20, this.subtotal * 0.20);
          this.maxPointsToRedeem = Math.min(
            this.loyaltyBalance,
            Math.floor(maxDiscount * 4),
            80
          );
          
          // Ensure points don't exceed maximum
          if (this.pointsToRedeem > this.maxPointsToRedeem) {
            this.pointsToRedeem = this.maxPointsToRedeem;
          }
          
          if (CART_DEBUG) console.log('⭐ Points calculation:', {
            pointsToRedeem: this.pointsToRedeem,
            pointsDiscount: this.pointsDiscount,
            maxPointsToRedeem: this.maxPointsToRedeem,
            subtotal: this.subtotal,
            maxPerTransaction: 80
          });
        }
      } catch (error) {
        console.error('❌ Points calculation error:', error);
        this.pointsDiscount = 0;
      }
    },
    
    async applyPromoCode() {
      if (!this.promoCode || this.promoCode.trim() === '') {
        return;
      }
      
      this.applyingPromo = true;
      this.promoError = null;
      
      try {
        if (CART_DEBUG) console.log('🎁 Applying promo code:', this.promoCode);
        
        // Use composable to apply promotion
        const result = await this.applyPromotionToCart(this.promoCode.trim());
        
        if (result.success) {
          this.appliedPromotion = result.data.promotion;
          this.promotionDiscount = result.data.discount_amount;
          this.promoError = null;
          if (CART_DEBUG) console.log('✅ Promotion applied! Discount:', this.promotionDiscount);
          
          // Show success message
          this.showSuccessNotification(`Promo code applied! You saved ₱${this.promotionDiscount.toFixed(2)}`);
        } else {
          this.promoError = result.error || 'Invalid promo code. Please check and try again.';
          console.warn('⚠️ Promotion not found or not applicable');
        }
      } catch (error) {
        console.error('❌ Error applying promo code:', error);
        this.promoError = error.message || 'Failed to apply promo code. Please try again.';
      } finally {
        this.applyingPromo = false;
      }
    },
    
    
    async removePromoCode() {
      if (CART_DEBUG) console.log('🗑️ Removing promo code');
      
      // Use composable to remove promotion
      if (this.appliedPromotion) {
        await this.removePromotionFromCart(this.appliedPromotion.id);
      }
      
      this.appliedPromotion = null;
      this.promotionDiscount = 0;
      this.promoCode = '';
      this.promoError = null;
      
      this.showSuccessNotification('Promo code removed');
    },

    // ===============================
    // Automatic promotion application
    // ===============================
    getItemDiscountForPromotion(item, promotion) {
      if (!promotion) return 0;
      if (!this.isItemEligibleForPromotion(item, promotion)) return 0;

      const originalPrice = parseFloat(item.price);
      let discountAmount = 0;

      if (promotion.type === 'percentage') {
        discountAmount = originalPrice * (promotion.discount_value / 100);
      } else if (promotion.type === 'fixed_amount') {
        discountAmount = Math.min(promotion.discount_value, originalPrice);
      }

      return Math.max(0, discountAmount);
    },

    computePromotionDiscount(promotion) {
      if (!promotion || !Array.isArray(this.cartItems) || this.cartItems.length === 0) {
        return 0;
      }
      let total = 0;
      for (const item of this.cartItems) {
        total += this.getItemDiscountForPromotion(item, promotion);
      }
      return Math.max(0, total);
    },

    async autoApplyBestPromotion() {
      try {
        // Do not override a manually applied promotion
        if (this.appliedPromotion) return;
        if (!this.activePromotions || this.activePromotions.length === 0) return;
        if (!this.cartItems || this.cartItems.length === 0) return;

        let bestPromotion = null;
        let bestDiscount = 0;

        for (const promo of this.activePromotions) {
          if (promo.status !== 'active') continue;
          const discount = this.computePromotionDiscount(promo);
          if (discount > bestDiscount) {
            bestDiscount = discount;
            bestPromotion = promo;
          }
        }

        if (bestPromotion && bestDiscount > 0) {
          this.appliedPromotion = bestPromotion;
          this.promotionDiscount = bestDiscount;
        } else {
          // No applicable promotion
          this.appliedPromotion = null;
          this.promotionDiscount = 0;
        }
      } catch (e) {
        console.error('Auto-apply promotion error:', e);
      }
    },
    
    getPromotionDescription(promotion) {
      if (!promotion) return '';
      
      if (promotion.type === 'percentage') {
        return `${promotion.discount_value}% off on eligible items`;
      } else if (promotion.type === 'fixed_amount') {
        return `₱${promotion.discount_value} off on your order`;
      } else if (promotion.type === 'buy_x_get_y') {
        const config = promotion.discount_config || {};
        return `Buy ${config.buy_quantity || 2} get ${config.get_quantity || 1} free`;
      }
      
      return promotion.description || 'Discount applied';
    },
    
    // Per-item discount calculation methods
    getItemDiscount(item) {
      if (CART_DEBUG) console.log('🔍 Checking discount for item:', item.name, 'Price:', item.price);
      if (CART_DEBUG) console.log('🎁 Available promotions:', this.activePromotions.length);
      
      // Check if item is eligible for any active promotion
      const applicablePromotion = this.getApplicablePromotionForItem(item);
      if (CART_DEBUG) console.log('✅ Applicable promotion for', item.name, ':', applicablePromotion);
      
      if (!applicablePromotion) {
        if (CART_DEBUG) console.log('❌ No applicable promotion for', item.name);
        return 0;
      }
      
      const originalPrice = parseFloat(item.price);
      let discountAmount = 0;
      
      if (applicablePromotion.type === 'percentage') {
        discountAmount = originalPrice * (applicablePromotion.discount_value / 100);
        if (CART_DEBUG) console.log('📊 Percentage discount:', applicablePromotion.discount_value + '%', 'Amount:', discountAmount);
      } else if (applicablePromotion.type === 'fixed_amount') {
        discountAmount = Math.min(applicablePromotion.discount_value, originalPrice);
        if (CART_DEBUG) console.log('💰 Fixed amount discount:', applicablePromotion.discount_value, 'Amount:', discountAmount);
      }
      
      const finalDiscount = Math.max(0, discountAmount);
      if (CART_DEBUG) console.log('🎯 Final discount for', item.name, ':', finalDiscount);
      return finalDiscount;
    },
    
    getItemDiscountedPrice(item) {
      const originalPrice = parseFloat(item.price);
      const discount = this.getItemDiscount(item);
      return Math.max(0, originalPrice - discount);
    },
    
    getItemDiscountText(item) {
      const applicablePromotion = this.getApplicablePromotionForItem(item);
      if (!applicablePromotion) return '';
      
      if (applicablePromotion.type === 'percentage') {
        return `${applicablePromotion.discount_value}% OFF`;
      } else if (applicablePromotion.type === 'fixed_amount') {
        return `₱${applicablePromotion.discount_value} OFF`;
      }
      
      return 'DISCOUNT';
    },
    
    getApplicablePromotionForItem(item) {
      if (CART_DEBUG) console.log('🔍 Checking promotions for item:', item.name);
      if (CART_DEBUG) console.log('📋 Active promotions count:', this.activePromotions.length);
      
      // Check if any active promotion applies to this item
      for (const promotion of this.activePromotions) {
        if (CART_DEBUG) console.log('🎁 Checking promotion:', promotion.name, 'Type:', promotion.type, 'Status:', promotion.status);
        const isEligible = this.isItemEligibleForPromotion(item, promotion);
        if (CART_DEBUG) console.log('✅ Is eligible for', promotion.name, ':', isEligible);
        
        if (isEligible) {
          if (CART_DEBUG) console.log('🎯 Found applicable promotion:', promotion.name);
          return promotion;
        }
      }
      if (CART_DEBUG) console.log('❌ No applicable promotion found for', item.name);
      return null;
    },
    
    isItemEligibleForPromotion(item, promotion) {
      if (CART_DEBUG) console.log('🔍 Checking eligibility for', item.name, 'with promotion', promotion.name);
      
      // Check if promotion is active
      if (promotion.status !== 'active') {
        if (CART_DEBUG) console.log('❌ Promotion not active:', promotion.status);
        return false;
      }
      
      // Check date validity
      const now = new Date();
      const startDate = new Date(promotion.start_date);
      const endDate = new Date(promotion.end_date);
      
      if (CART_DEBUG) console.log('📅 Date check - Now:', now, 'Start:', startDate, 'End:', endDate);
      
      if (now < startDate || now > endDate) {
        if (CART_DEBUG) console.log('❌ Promotion outside date range');
        return false;
      }
      
      // Check target type and IDs
      if (CART_DEBUG) console.log('🎯 Target type:', promotion.target_type, 'Target IDs:', promotion.target_ids);
      
      const targetType = (promotion.target_type || '').toLowerCase();
      if (targetType === 'all') {
        if (CART_DEBUG) console.log('✅ Promotion applies to all items');
        return true;
      } else if (targetType === 'category' || targetType === 'categories') {
        // Check if item belongs to target category
        const isCategoryMatch = promotion.target_ids && promotion.target_ids.includes(item.category_id);
        if (CART_DEBUG) console.log('📂 Category check - Item category:', item.category_id, 'Target IDs:', promotion.target_ids, 'Match:', isCategoryMatch);
        
        // If category match failed, try drinks keyword matching for drinks promotions
        if (!isCategoryMatch && promotion.name && promotion.name.toLowerCase().includes('drinks')) {
          if (CART_DEBUG) console.log('🔍 Category match failed, trying drinks keyword matching...');
          const itemName = item.name.toLowerCase();
          const itemDescription = (item.description || '').toLowerCase();
          const drinksKeywords = ['drink', 'beverage', 'juice', 'soda', 'water', 'tea', 'coffee', 'milk', '7 up', 'coke', 'pepsi', 'alaska'];
          const isDrinksMatch = drinksKeywords.some(keyword => 
            itemName.includes(keyword) || itemDescription.includes(keyword)
          );
          if (CART_DEBUG) console.log('🥤 Drinks keyword check - Keywords:', drinksKeywords, 'Item name:', itemName, 'Match:', isDrinksMatch);
          return isDrinksMatch;
        }
        
        return isCategoryMatch;
      } else if (targetType === 'product' || targetType === 'products') {
        // Check if item is in target products
        const isProductMatch = promotion.target_ids && promotion.target_ids.includes(item.product_id || item.id);
        if (CART_DEBUG) console.log('🛍️ Product check - Item ID:', item.product_id || item.id, 'Match:', isProductMatch);
        return isProductMatch;
      } else if (promotion.target_type === 'specific') {
        // Check specific criteria (e.g., drinks, ramyeon, etc.)
        const itemName = item.name.toLowerCase();
        const itemDescription = (item.description || '').toLowerCase();
        
        if (CART_DEBUG) console.log('🔍 Specific check - Item name:', itemName, 'Description:', itemDescription);
        
        // Check for drinks promotion
        if (promotion.name && promotion.name.toLowerCase().includes('drinks')) {
          const drinksKeywords = ['drink', 'beverage', 'juice', 'soda', 'water', 'tea', 'coffee', 'milk', '7 up', 'coke', 'pepsi'];
          const isDrinksMatch = drinksKeywords.some(keyword => 
            itemName.includes(keyword) || itemDescription.includes(keyword)
          );
          if (CART_DEBUG) console.log('🥤 Drinks check - Keywords:', drinksKeywords, 'Match:', isDrinksMatch);
          return isDrinksMatch;
        }
        
        // Check for ramyeon promotion
        if (promotion.name && promotion.name.toLowerCase().includes('ramyeon')) {
          const ramyeonKeywords = ['ramyeon', 'ramen', 'noodle', 'soup'];
          const isRamyeonMatch = ramyeonKeywords.some(keyword => 
            itemName.includes(keyword) || itemDescription.includes(keyword)
          );
          if (CART_DEBUG) console.log('🍜 Ramyeon check - Keywords:', ramyeonKeywords, 'Match:', isRamyeonMatch);
          return isRamyeonMatch;
        }
      }
      
      if (CART_DEBUG) console.log('❌ No matching criteria found');
      return false;
    },
    
    showSuccessNotification(message) {
      // Simple notification (you can enhance this)
      const notification = document.createElement('div');
      notification.className = 'promo-notification success';
      notification.textContent = message;
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
        z-index: 10000;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        animation: slideInRight 0.3s ease-out;
      `;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-in reverse';
        setTimeout(() => {
          if (notification.parentNode) {
            document.body.removeChild(notification);
          }
        }, 300);
      }, 3000);
    },
    
    async openMap() {
      this.showMap = true;
      
      // Load Google Maps script dynamically
      if (!window.google) {
        try {
          await this.loadGoogleMapsScript();
        } catch (error) {
          console.error('Failed to load Google Maps:', error);
          alert('Unable to load Google Maps. Please check:\n1. Internet connection\n2. API key is valid\n3. Billing is enabled in Google Cloud Console\n\nYou can manually enter your address instead.');
          this.closeMap();
          return;
        }
      }
      
      this.$nextTick(() => {
        this.initializeMap();
      });
    },
    loadGoogleMapsScript() {
      return new Promise((resolve, reject) => {
        if (window.google) {
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAmv6-w1GHQ7Z4Y7c_iOlr17iw6Z6pnmC0&libraries=places&callback=initMap';
        script.async = true;
        script.defer = true;
        
        window.initMap = () => {
          resolve();
          delete window.initMap;
        };
        
        script.onerror = () => {
          reject(new Error('Failed to load Google Maps script'));
        };
        
        document.head.appendChild(script);
      });
    },
    closeMap() {
      this.showMap = false;
    },
    initializeMap() {
      const mapElement = document.getElementById('google-map');
      if (!mapElement || !window.google) {
        console.error('Google Maps not loaded or map element not found');
        alert('Unable to load Google Maps. Please check your internet connection and try again.');
        this.closeMap();
        return;
      }

      try {
        // Default center (Philippines - you can change this to your preferred location)
        const defaultCenter = { lat: 8.1837, lng: 126.3162 }; // Bislig City, Philippines
        
        // Initialize the map
        this.map = new window.google.maps.Map(mapElement, {
          center: defaultCenter,
          zoom: 13,
          mapTypeControl: true,
          streetViewControl: false,
          fullscreenControl: false,
          mapId: 'DEMO_MAP_ID' // Required for advanced features
        });

        // Try to get user's current location
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };
              this.map.setCenter(userLocation);
              this.placeMarker(userLocation);
            },
            (error) => {
              console.log('Geolocation error:', error);
              // If geolocation fails, use default location
              this.placeMarker(defaultCenter);
            }
          );
        } else {
          // Browser doesn't support geolocation
          this.placeMarker(defaultCenter);
        }

        // Add click listener to map
        this.map.addListener('click', (event) => {
          this.placeMarker(event.latLng);
        });
      } catch (error) {
        console.error('Map initialization error:', error);
        
        // Check if it's a billing error
        if (error.message && error.message.includes('Billing')) {
          alert('⚠️ Google Maps API Error: Billing is not enabled.\n\nPlease enable billing for this API key in Google Cloud Console:\n1. Go to console.cloud.google.com\n2. Select your project\n3. Enable billing\n4. Enable Maps JavaScript API');
        } else {
          alert('Unable to initialize Google Maps. Error: ' + error.message);
        }
        this.closeMap();
      }
    },
    placeMarker(location) {
      // Remove existing marker if any
      if (this.marker) {
        this.marker.setMap(null);
      }

      // Create new marker
      this.marker = new window.google.maps.Marker({
        position: location,
        map: this.map,
        animation: window.google.maps.Animation.DROP,
        title: 'Delivery Location'
      });

      // Get address from coordinates using Geocoding
      this.getAddressFromCoordinates(location);
    },
    getAddressFromCoordinates(location) {
      const geocoder = new window.google.maps.Geocoder();
      const latLng = {
        lat: typeof location.lat === 'function' ? location.lat() : location.lat,
        lng: typeof location.lng === 'function' ? location.lng() : location.lng
      };

      geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === 'OK' && results[0]) {
          this.deliveryAddress = results[0].formatted_address;
          
          // Optionally show an info window
          if (this.marker) {
            const infoWindow = new window.google.maps.InfoWindow({
              content: `<div style="padding: 10px;">
                <strong>Selected Location:</strong><br/>
                ${results[0].formatted_address}
              </div>`
            });
            infoWindow.open(this.map, this.marker);
          }
        } else {
          console.error('Geocoder failed:', status);
          alert('Unable to get address for this location. Please try another location.');
        }
      });
    },
    async proceedToCheckout() {
      if (!this.canCheckout) return;
      
      // Client-only submission lock to prevent duplicate creates without changing backend schema
      try {
        const lockKey = 'ramyeon_order_lock';
        if (sessionStorage.getItem(lockKey) === 'locked') {
          alert('Your order is already being processed. Please wait...');
          return;
        }
        sessionStorage.setItem(lockKey, 'locked');
      } catch (e) {
        console.warn('Could not set submission lock:', e);
      }

      this.isProcessing = true;
      
      try {
        // Get user profile for payment processing
        await this.loadUserProfile();
        
        let paymentReference = null;
        let paymentStatus = 'pending';
        
        // Generate order ID
        const orderId = 'ORDER-' + Date.now();
        
        // Track payment attempt
        this.trackPaymentAttempt(orderId, 'initiated');
        
        // Prepare order data using composable
        const orderData = {
          id: orderId,
          user: this.userProfile,
          items: this.cartItems,
          total_amount: this.finalTotal,
          delivery_type: this.deliveryType,
          delivery_address: this.deliveryAddress,
          payment_method: this.paymentMethod,
          special_instructions: this.specialInstructions,
          promotions: this.appliedPromotion ? [this.appliedPromotion.id] : [],
          loyalty_points: this.useLoyaltyPoints ? this.pointsToRedeem : 0
        };
        
        // Use composable to create order (only for COD)
        let backendOrderIdFromCreate = null;
        if (this.paymentMethod === 'cod') {
          const createRes = await this.createOrder(orderData);
          if (!createRes.success) {
            throw new Error(createRes.error || 'Failed to create order');
          }
          backendOrderIdFromCreate = (createRes && (createRes.data?.order_id || createRes.order_id)) || null;
        }
        
        // Order created successfully
        
        console.log('🛒 Starting checkout:', {
          orderId,
          paymentMethod: this.paymentMethod,
          deliveryType: this.deliveryType,
          total: this.finalTotal,
          promotion: this.appliedPromotion,
          loyaltyPoints: this.useLoyaltyPoints ? this.pointsToRedeem : 0
        });
        
        // Process payment based on payment method
        if (this.paymentMethod === 'cash') {
          // Cash on delivery - no payment processing needed
          console.log('💵 Processing Cash on Delivery');
          paymentStatus = 'pending';
          paymentReference = 'COD-' + Date.now();
        } else if (this.paymentMethod === 'gcash') {
          // Process GCash payment
          try {
            console.log('💳 Processing GCash payment...');
            const gcashResult = await this.processGCashPayment(orderId);
            console.log('GCash API response:', gcashResult);
            
            if (gcashResult && gcashResult.data && gcashResult.data.attributes && gcashResult.data.attributes.redirect) {
              // Track successful initiation
              paymentReference = gcashResult.data.id;
              this.trackPaymentAttempt(orderId, 'redirected', 'gcash');
              // Store pending order before redirect
              this.storePendingOrder(orderId, this.cartItems, this.finalTotal, paymentReference, paymentStatus);
              // Redirect to GCash checkout
              console.log('✅ Redirecting to GCash:', gcashResult.data.attributes.redirect.checkout_url);
              window.location.href = gcashResult.data.attributes.redirect.checkout_url;
              return; // Exit here, payment will be confirmed via redirect
            } else {
              throw new Error('Invalid GCash payment response - no redirect URL');
            }
          } catch (error) {
            console.error('❌ GCash payment error:', error);
            this.trackPaymentAttempt(orderId, 'failed', 'gcash', error.message);
            alert('Failed to process GCash payment:\n' + error.message + '\n\nPlease try again or select a different payment method.');
            this.isProcessing = false;
            return;
          }
        } else if (this.paymentMethod === 'paymaya') {
          // Process PayMaya payment
          try {
            console.log('💳 Processing PayMaya payment...');
            const paymayaResult = await this.processPayMayaPayment(orderId);
            console.log('PayMaya API response:', paymayaResult);
            
            if (paymayaResult && paymayaResult.data && paymayaResult.data.attributes && paymayaResult.data.attributes.redirect) {
              // Track successful initiation
              paymentReference = paymayaResult.data.id;
              this.trackPaymentAttempt(orderId, 'redirected', 'paymaya');
              // Store pending order before redirect
              this.storePendingOrder(orderId, this.cartItems, this.finalTotal, paymentReference, paymentStatus);
              // Redirect to PayMaya checkout
              console.log('✅ Redirecting to PayMaya:', paymayaResult.data.attributes.redirect.checkout_url);
              window.location.href = paymayaResult.data.attributes.redirect.checkout_url;
              return; // Exit here, payment will be confirmed via redirect
            } else {
              throw new Error('Invalid PayMaya payment response - no redirect URL');
            }
          } catch (error) {
            console.error('❌ PayMaya payment error:', error);
            this.trackPaymentAttempt(orderId, 'failed', 'paymaya', error.message);
            alert('Failed to process PayMaya payment:\n' + error.message + '\n\nPlease try again or select a different payment method.');
            this.isProcessing = false;
            return;
          }
        } else if (this.paymentMethod === 'card') {
          // Process Card payment - using Payment Links API
          try {
            console.log('💳 Processing Card payment...');
            const cardResult = await this.processCardPayment(orderId);
            console.log('Card API response:', cardResult);
            
            if (cardResult && cardResult.data && cardResult.data.attributes && cardResult.data.attributes.redirect) {
              // Track successful initiation
              paymentReference = cardResult.data.id;
              this.trackPaymentAttempt(orderId, 'redirected', 'card');
              // Store pending order before redirect
              this.storePendingOrder(orderId, this.cartItems, this.finalTotal, paymentReference, paymentStatus);
              // Redirect to card payment checkout
              console.log('✅ Redirecting to Card payment:', cardResult.data.attributes.redirect.checkout_url);
              window.location.href = cardResult.data.attributes.redirect.checkout_url;
              return; // Exit here, payment will be confirmed via redirect
            } else {
              throw new Error('Invalid card payment response - no redirect URL');
            }
          } catch (error) {
            console.error('❌ Card payment error:', error);
            this.trackPaymentAttempt(orderId, 'failed', 'card', error.message);
            alert('Failed to process card payment:\n' + error.message + '\n\nPlease try again or select a different payment method.');
            this.isProcessing = false;
            return;
          }
        } else if (this.paymentMethod === 'grabpay') {
          // Process GrabPay QR payment
          try {
            console.log('💳 Processing GrabPay payment...');
            const grabpayResult = await this.processGrabPayPayment(orderId);
            console.log('GrabPay API response:', grabpayResult);
            
            if (grabpayResult && grabpayResult.data && grabpayResult.data.attributes && grabpayResult.data.attributes.redirect) {
              // Track successful initiation
              paymentReference = grabpayResult.data.id;
              this.trackPaymentAttempt(orderId, 'redirected', 'grabpay');
              // Store pending order before redirect
              this.storePendingOrder(orderId, this.cartItems, this.finalTotal, paymentReference, paymentStatus);
              // Redirect to GrabPay QR checkout
              console.log('✅ Redirecting to GrabPay:', grabpayResult.data.attributes.redirect.checkout_url);
              window.location.href = grabpayResult.data.attributes.redirect.checkout_url;
              return; // Exit here, payment will be confirmed via redirect
            } else {
              throw new Error('Invalid GrabPay payment response - no redirect URL');
            }
          } catch (error) {
            console.error('❌ GrabPay payment error:', error);
            this.trackPaymentAttempt(orderId, 'failed', 'grabpay', error.message);
            alert('Failed to process GrabPay payment:\n' + error.message + '\n\nPlease try again or select a different payment method.');
            this.isProcessing = false;
            return;
          }
        }
        
        // Create order data
        const localOrderData = {
          id: orderId,
          items: this.cartItems,
          deliveryType: this.deliveryType,
          deliveryAddress: this.deliveryAddress,
          paymentMethod: this.paymentMethod,
          specialInstructions: this.specialInstructions,
          subtotal: this.subtotal,
          deliveryFee: this.deliveryFee,
          serviceFee: this.serviceFee,
          pointsDiscount: this.pointsDiscount,
          promotionDiscount: this.promotionDiscount,
          promotion: this.appliedPromotion,
          loyaltyPoints: this.useLoyaltyPoints ? this.pointsToRedeem : 0,
          total: this.finalTotal,
          orderTime: new Date().toISOString(),
          status: paymentStatus === 'succeeded' ? 'confirmed' : 'pending',
          paymentReference: paymentReference,
          paymentStatus: paymentStatus,
          backendOrderId: backendOrderIdFromCreate
        };
        
        // Backend order was already created by createOrder(); skip duplicate calls
        
        // Handle loyalty points redemption (only for authenticated users)
        if (this.userProfile && this.userProfile.id !== 'guest' && this.useLoyaltyPoints && this.pointsToRedeem > 0) {
          try {
            console.log('⭐ Redeeming loyalty points:', this.pointsToRedeem);
            const redeemResult = await this.redeemPoints(this.pointsToRedeem, this.userProfile.id, {
              order_id: orderId,
              description: `Points redeemed for order #${orderId}`
            });
            console.log('✅ Points redeemed:', redeemResult);
          } catch (loyaltyError) {
            console.error('❌ Loyalty points redemption error:', loyaltyError);
            // Don't fail the order if points redemption fails
          }
        }
        
        // Store order in localStorage (tied to user)
        const userId = this.userProfile?.id || this.userProfile?.email || 'guest';
        const userOrdersKey = `ramyeon_orders_${userId}`;
        const orders = JSON.parse(localStorage.getItem(userOrdersKey) || '[]');
        orders.push(localOrderData);
        localStorage.setItem(userOrdersKey, JSON.stringify(orders));
        
        // Also save to global orders for backwards compatibility
        const allOrders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
        allOrders.push(localOrderData);
        localStorage.setItem('ramyeon_orders', JSON.stringify(allOrders));
        
        console.log('✅ Order saved successfully:', localOrderData.id, 'for user:', userId);
        
        // Clear cart completely
        console.log('🧹 Clearing cart - before:', this.cartItems.length);
        this.cartItems = [];
        localStorage.removeItem('ramyeon_cart');
        console.log('🧹 Cart cleared - after:', this.cartItems.length);
        console.log('🧹 LocalStorage cart:', localStorage.getItem('ramyeon_cart'));
        
        // Force update to ensure cart UI updates
        this.$forceUpdate();
        
        // Calculate points earned (20% of subtotal after discount)
        const subtotalAfterDiscount = this.subtotal - this.pointsDiscount;
        const pointsEarned = Math.floor(subtotalAfterDiscount * 0.20);
        
        // Award points to authenticated users
        if (this.userProfile && this.userProfile.id !== 'guest' && pointsEarned > 0) {
          try {
            console.log('⭐ Awarding loyalty points:', pointsEarned, 'for order:', orderId);
            const awardResult = await this.awardPoints(pointsEarned, this.userProfile.id, {
              order_id: orderId,
              description: `Points earned from order #${orderId}`
            });
            console.log('✅ Points awarded:', awardResult);
            
            // Update user profile with new points
            if (awardResult.success && awardResult.award) {
              this.userProfile.loyalty_points = awardResult.award.total_points;
              console.log('👤 Updated user points:', this.userProfile.loyalty_points);
              
              // Force UI update to show new points
              this.$forceUpdate();
            }
          } catch (loyaltyError) {
            console.error('❌ Loyalty points awarding error:', loyaltyError);
            // Don't fail the order if points awarding fails
          }
        }
        
        // Refresh user profile to show updated points
        if (this.userProfile && this.userProfile.id !== 'guest') {
          try {
            console.log('🔄 Refreshing user profile to show updated points...');
            await this.loadUserProfile();
            console.log('✅ User profile refreshed with points:', this.userProfile.loyalty_points);
          } catch (error) {
            console.error('❌ Error refreshing user profile:', error);
          }
        }
        
        // Show confirmation modal
        this.confirmedOrder = {
          id: localOrderData.backendOrderId || localOrderData.id,
          total: this.finalTotal.toFixed(2),
          paymentMethod: this.paymentMethod,
          deliveryType: this.deliveryType,
          paymentStatus: paymentStatus,
          pointsEarned: pointsEarned,
          pointsUsed: this.useLoyaltyPoints ? this.pointsToRedeem : 0
        };
        
        console.log('🎉 Showing order confirmation modal');
        console.log('Confirmed order data:', this.confirmedOrder);
        console.log('showOrderConfirmation before:', this.showOrderConfirmation);
        
        // Use nextTick to ensure DOM is updated
        this.$nextTick(() => {
          this.showOrderConfirmation = true;
          console.log('showOrderConfirmation after:', this.showOrderConfirmation);
          console.log('Modal should be visible now!');
          
          // Triple check after render
          setTimeout(() => {
            console.log('After 500ms - showOrderConfirmation:', this.showOrderConfirmation);
            const modalElement = document.querySelector('.confirmation-modal-overlay');
            console.log('Modal element exists in DOM:', !!modalElement);
            if (modalElement) {
              console.log('Modal computed style:', window.getComputedStyle(modalElement).display);
              console.log('Modal visibility:', window.getComputedStyle(modalElement).visibility);
              console.log('Modal z-index:', window.getComputedStyle(modalElement).zIndex);
            } else {
              console.error('❌ MODAL ELEMENT NOT FOUND IN DOM!');
              console.error('This means v-if="showOrderConfirmation" is not rendering');
              console.error('Current state:', {
                showOrderConfirmation: this.showOrderConfirmation,
                confirmedOrder: this.confirmedOrder
              });
            }
          }, 500);
        });
        
      } catch (error) {
        // Persist detailed error info so it isn't lost when the alert closes
        const detailed = {
          message: error?.message || 'Unknown error',
          stack: error?.stack,
          name: error?.name,
          // If an axios-style error bubbles up, capture response details
          status: error?.response?.status,
          statusText: error?.response?.statusText,
          responseData: error?.response?.data,
        };
        try {
          window.ramyeonLastError = detailed;
          localStorage.setItem('ramyeon_last_error', JSON.stringify(detailed, null, 2));
        } catch (persistErr) {
          console.warn('Failed to persist last error for diagnostics:', persistErr);
        }
        console.error('Checkout error (captured):', detailed);
        alert('There was an error processing your order. Please try again.\n\nError: ' + (detailed.message || 'Unknown error'));
      } finally {
        this.isProcessing = false;
        try { sessionStorage.removeItem('ramyeon_order_lock'); } catch (e) {
          console.warn('Could not clear submission lock:', e);
        }
      }
    },
    
    storePendingOrder(orderId, items, total, paymentReference, paymentStatus) {
      // Store order data before redirect
      const orderData = {
        id: orderId,
        items: items,
        deliveryType: this.deliveryType,
        deliveryAddress: this.deliveryAddress,
        paymentMethod: this.paymentMethod,
        specialInstructions: this.specialInstructions,
        subtotal: this.subtotal,
        deliveryFee: this.deliveryFee,
        serviceFee: this.serviceFee,
        total: total,
        orderTime: new Date().toISOString(),
        status: 'pending_payment',
        paymentReference: paymentReference,
        paymentStatus: paymentStatus,
        // Persist loyalty selection for post-return create
        pointsToRedeem: this.useLoyaltyPoints ? this.pointsToRedeem : 0,
        pointsDiscount: this.useLoyaltyPoints ? Math.min((this.pointsToRedeem / 4), 20) : 0
      };
      
      localStorage.setItem('ramyeon_pending_order', JSON.stringify(orderData));
      localStorage.removeItem('ramyeon_cart'); // Clear cart before redirect
    },
    
    checkPaymentReturn() {
      if (CART_DEBUG) {
        console.log('[Cart] Checking payment return');
        console.log('[Cart] URL:', window.location.href);
      }
      
      // For hash routing, parameters come after the hash
      // URL format: #/cart?payment=success&order=ORDER-xxx
      let paymentStatus = null;
      let orderId = null;
      
      // Try to get parameters from hash first (for hash routing)
      if (window.location.hash.includes('?')) {
        const hashParts = window.location.hash.split('?');
        if (hashParts.length > 1) {
          const urlParams = new URLSearchParams(hashParts[1]);
          paymentStatus = urlParams.get('payment');
          orderId = urlParams.get('order');
          if (CART_DEBUG) console.log('[Cart] Parsed payment params from hash');
        }
      }
      
      // Fallback to regular URL parameters
      if (!paymentStatus || !orderId) {
        const urlParams = new URLSearchParams(window.location.search);
        paymentStatus = urlParams.get('payment');
        orderId = urlParams.get('order');
        if (CART_DEBUG) console.log('[Cart] Parsed payment params from search');
      }
      
      if (CART_DEBUG) console.log('[Cart] Payment return params:', { paymentStatus, orderId });
      
      if (paymentStatus && orderId) {
        if (CART_DEBUG) console.log('[Cart] Payment return detected');
        
        // Get pending order
        const pendingOrderStr = localStorage.getItem('ramyeon_pending_order');
        if (CART_DEBUG) console.log('[Cart] Pending order exists:', !!pendingOrderStr);
        
        if (pendingOrderStr) {
          if (CART_DEBUG) console.log('[Cart] Pending order found in localStorage');
          
          try {
            const orderData = JSON.parse(pendingOrderStr);
            if (CART_DEBUG) console.log('[Cart] Parsed order data (ids only):', { id: orderData?.id, total: orderData?.total });
            
            if (paymentStatus === 'success') {
              // Payment successful
              if (CART_DEBUG) console.log('[Cart] Payment successful');
              
              orderData.paymentStatus = 'succeeded';
              orderData.status = 'confirmed';
              
              if (CART_DEBUG) console.log('[Cart] Order marked confirmed');
              
              // Track successful payment
              this.trackPaymentAttempt(orderId, 'succeeded', orderData.paymentMethod);
              
              // Load user profile first
              if (CART_DEBUG) console.log('[Cart] Loading user profile...');
              this.loadUserProfile().then(async () => {
                if (CART_DEBUG) console.log('[Cart] User profile loaded');
                
                // Award points for successful payment (20% of subtotal after discount)
                if (this.userProfile && this.userProfile.id !== 'guest') {
                  const subtotalAfterDiscount = orderData.subtotal - (orderData.pointsDiscount || 0);
                  const pointsEarned = Math.floor(subtotalAfterDiscount * 0.20);
                  
                  if (pointsEarned > 0) {
                    try {
                      if (CART_DEBUG) console.log('[Cart] Awarding loyalty points:', pointsEarned);
                      const awardResult = await this.awardPoints(pointsEarned, this.userProfile.id, {
                        order_id: orderId,
                        description: `Points earned from order #${orderId} (payment return)`
                      });
                      if (CART_DEBUG) console.log('[Cart] Points awarded');
                      
                      // Update user profile with new points
                      if (awardResult.success && awardResult.data) {
                        this.userProfile.loyalty_points = this.loyaltyBalance;
                        if (CART_DEBUG) console.log('[Cart] Updated user points after payment');
                        
                        // Force UI update to show new points
                        this.$forceUpdate();
                      }
                    } catch (loyaltyError) {
                      console.error('❌ Loyalty points awarding error on payment return:', loyaltyError);
                    }
                  }
                }
                
                // Save order (tied to user)
                const userId = this.userProfile?.id || this.userProfile?.email || 'guest';
                const userOrdersKey = `ramyeon_orders_${userId}`;
                
                if (CART_DEBUG) console.log('[Cart] Saving order to user key');
                
                const orders = JSON.parse(localStorage.getItem(userOrdersKey) || '[]');
                
                orders.push(orderData);
                localStorage.setItem(userOrdersKey, JSON.stringify(orders));
                if (CART_DEBUG) console.log('[Cart] Saved to user orders');
                
                // Also save to global orders
                const allOrders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
                allOrders.push(orderData);
                localStorage.setItem('ramyeon_orders', JSON.stringify(allOrders));
                if (CART_DEBUG) console.log('[Cart] Saved to global orders');
                
                // Send to backend only if it wasn't already created pre-redirect
                if (!orderData.backendOrderId) {
                  this.sendOrderToBackend(orderData);
                } else {
                  if (CART_DEBUG) console.log('[Cart] Skipping backend send - backendOrderId exists');
                }
                
                // Clear pending order
                localStorage.removeItem('ramyeon_pending_order');
                if (CART_DEBUG) console.log('[Cart] Cleared pending order');
                
                // Clear cart completely
                this.cartItems = [];
                localStorage.removeItem('ramyeon_cart');
                this.$forceUpdate();
                
                // Calculate points earned for display
                const subtotalAfterDiscount = orderData.subtotal - (orderData.pointsDiscount || 0);
                const pointsEarned = Math.floor(subtotalAfterDiscount * 0.20);
                
                // Refresh user profile to show updated points
                try {
                  if (CART_DEBUG) console.log('[Cart] Refreshing user profile after payment return...');
                  await this.loadUserProfile();
                  if (CART_DEBUG) console.log('[Cart] User profile refreshed');
                } catch (error) {
                  console.error('❌ Error refreshing user profile after payment:', error);
                }
                
                // Show confirmation
                this.confirmedOrder = {
                  id: orderData.id,
                  total: orderData.total.toFixed(2),
                  paymentMethod: orderData.paymentMethod,
                  deliveryType: orderData.deliveryType,
                  paymentStatus: 'succeeded',
                  pointsEarned: pointsEarned,
                  pointsUsed: orderData.pointsDiscount || 0
                };
                
                if (CART_DEBUG) console.log('[Cart] Showing confirmation modal for returned payment');
                
                // Force update and show modal
                this.$forceUpdate();
                
                // Use nextTick to ensure DOM is updated
                this.$nextTick(() => {
                  this.showOrderConfirmation = true;
                  
                  // Check after a delay
                  setTimeout(() => {
                    const modalElement = document.querySelector('.confirmation-modal-overlay');
                    
                    if (modalElement) {
                      if (CART_DEBUG) console.log('[Cart] Confirmation modal visible');
                    } else {
                      console.error('❌❌❌ MODAL NOT IN DOM!');
                      alert('Modal should show but its not in DOM. State: ' + this.showOrderConfirmation);
                    }
                  }, 500);
                });
                
                // DON'T clean URL immediately - wait for user to close modal
                // The modal close button will handle navigation
                if (CART_DEBUG) console.log('[Cart] Keeping URL with params until modal close');
              }).catch(err => {
                console.error('Error loading user profile:', err);
                // Continue anyway with guest user
                this.showOrderConfirmation = true;
              });
            } else {
              // Payment failed or cancelled
              if (CART_DEBUG) console.log('[Cart] Payment failed/cancelled');
              // Track failed/cancelled payment
              this.trackPaymentAttempt(orderId, 'cancelled', orderData.paymentMethod, 'User cancelled payment');
              
              alert('Payment was not completed. Your order was not placed. Your items have been restored to the cart.');
              
              // Restore cart
              this.cartItems = orderData.items;
              localStorage.setItem('ramyeon_cart', JSON.stringify(orderData.items));
              localStorage.removeItem('ramyeon_pending_order');
              if (CART_DEBUG) console.log('[Cart] Cart restored after failed/cancelled payment');
              
              // Don't clean URL here - payment will still try to process
              if (CART_DEBUG) console.log('[Cart] Leaving URL as is');
            }
          } catch (error) {
            console.error('❌❌❌ ERROR processing payment return:', error);
            console.error('Error details:', error.message);
            console.error('Error stack:', error.stack);
            alert('There was an error processing your payment return. Please contact support if your payment was successful.');
          }
        } else {
          if (CART_DEBUG) console.log('[Cart] No pending order found for payment return');
          alert('No pending order found! The order may not have been stored before payment redirect.');
        }
      } else {
        if (CART_DEBUG) console.log('[Cart] No payment return detected');
      }
      
    },
    
    
    async sendOrderToBackend(orderData) {
      try {
        console.log('📤 Attempting to send order to backend...');
        const response = await this.createOrder({
          user: this.userProfile,
          items: orderData.items,
          total_amount: orderData.total,
          delivery_type: orderData.deliveryType,
          delivery_address: orderData.deliveryAddress,
          payment_method: orderData.paymentMethod,
          special_instructions: orderData.specialInstructions,
          payment_reference: orderData.paymentReference,
          payment_status: orderData.paymentStatus,
          // Map stored points to backend field used for redemption
          loyalty_points: orderData.pointsToRedeem || 0
        });
        
        console.log('✅ Order sent to backend successfully:', response);
      } catch (error) {
        console.warn('⚠️ Failed to send order to backend (this is OK, order saved locally):', error.message);
        // Don't throw - order is already saved locally, backend is optional
      }
    },
    
    closeConfirmationModal() {
      console.log('🚪 Closing confirmation modal');
      this.showOrderConfirmation = false;
      
      // Clean URL when modal closes
      window.location.hash = '#/cart';  // Clean but stay on cart page
      console.log('✅ URL cleaned, staying on cart');
    },
    
    goToHome() {
      console.log('🏠 Going to home');
      this.showOrderConfirmation = false;
      
      // Navigate to home via hash
      window.location.hash = '#/';
      this.$emit('setCurrentPage', 'Home');
    },
    
    async loadUserProfile() {
      try {
        console.log('🔍 DEBUG: Attempting to load user profile...');
        
        // Check if user is logged in
        const token = localStorage.getItem('access_token');
        console.log('🔍 DEBUG: JWT Token exists:', !!token);
        
        if (!token) {
          throw new Error('No JWT token found - user not logged in');
        }
        
        // Try to get real customer profile from backend
        console.log('🔍 DEBUG: Calling authAPI.getProfile()...');
        const response = await authAPI.getProfile();
        console.log('🔍 DEBUG: API Response:', response);
        
        if (response && response.customer) {
          this.userProfile = {
            id: response.customer.customer_id,
            email: response.customer.email,
            full_name: response.customer.full_name,
            loyalty_points: response.customer.loyalty_points || 0 // Real points from database
          };
          
          console.log('✅ Real customer profile loaded:', {
            email: this.userProfile.email,
            loyalty_points: this.userProfile.loyalty_points
          });
        } else {
          console.error('❌ No customer data in response:', response);
          throw new Error('No customer data received');
        }
      } catch (error) {
        console.error('❌ Failed to load real customer profile:', error);
        
        // Enhanced error logging
        if (error.response) {
          console.error('❌ HTTP Status:', error.response.status);
          console.error('❌ Response Data:', error.response.data);
          console.error('❌ Response Headers:', error.response.headers);
        } else if (error.data) {
          console.error('❌ Error Data:', error.data);
        }
        
        console.error('❌ Error Message:', error.message || 'No error message available');
        console.error('❌ Full Error Object:', JSON.stringify(error, null, 2));
        
        // For debugging: Use a test profile with some points
        this.userProfile = {
          id: 'test-user',
          email: 'test@ramyeon.com',
          full_name: 'Test User',
          loyalty_points: 50 // Give test user some points for debugging
        };
        
        console.log('🧪 Using test profile with points for debugging:', this.userProfile.loyalty_points);
        console.log('💡 To fix: Make sure you are logged in and backend is running');
        console.log('💡 Check backend logs for detailed error information');
      }
    },
    
    async processGCashPayment(orderId) {
      try {
        const source = await paymongoAPI.processGCashPayment({
          amount: this.finalTotal, // Use final total with discount
          orderId: orderId,
          customerEmail: this.userProfile?.email || 'customer@example.com',
          customerName: this.userProfile?.full_name || 'Customer'
        });
        
        return source;
      } catch (error) {
        console.error('GCash payment error:', error);
        throw new Error('Failed to process GCash payment. Please try again.');
      }
    },
    
    async processPayMayaPayment(orderId) {
      try {
        const source = await paymongoAPI.processPayMayaPayment({
          amount: this.finalTotal, // Use final total with discount
          orderId: orderId,
          customerEmail: this.userProfile?.email || 'customer@example.com',
          customerName: this.userProfile?.full_name || 'Customer'
        });
        
        return source;
      } catch (error) {
        console.error('PayMaya payment error:', error);
        throw new Error('Failed to process PayMaya payment. Please try again.');
      }
    },
    
    async processCardPayment(orderId) {
      try {
        // Create card payment source (similar to GCash/PayMaya)
        const source = await paymongoAPI.processCardPayment({
          amount: this.finalTotal, // Use final total with discount
          orderId: orderId,
          customerEmail: this.userProfile?.email || 'customer@example.com',
          customerName: this.userProfile?.full_name || 'Customer'
        });
        
        return source;
      } catch (error) {
        console.error('Card payment error:', error);
        throw new Error('Failed to process card payment. ' + (error.message || 'Please try again.'));
      }
    },
    
    async processGrabPayPayment(orderId) {
      try {
        const source = await paymongoAPI.processGrabPayPayment({
          amount: this.finalTotal, // Use final total with discount
          orderId: orderId,
          customerEmail: this.userProfile?.email || 'customer@example.com',
          customerName: this.userProfile?.full_name || 'Customer'
        });
        
        return source;
      } catch (error) {
        console.error('GrabPay payment error:', error);
        throw new Error('Failed to process GrabPay payment. ' + (error.message || 'Please try again.'));
      }
    },
    
    // Payment history tracking
    trackPaymentAttempt(orderId, status, method = null, error = null) {
      try {
        const paymentHistory = JSON.parse(localStorage.getItem('ramyeon_payment_history') || '[]');
        
        const attempt = {
          orderId: orderId,
          method: method || this.paymentMethod,
          status: status, // 'initiated', 'redirected', 'succeeded', 'failed', 'cancelled'
          amount: this.finalTotal, // Use final total with discount
          promotionApplied: this.appliedPromotion ? this.appliedPromotion.promotion_id : null,
          discountAmount: this.promotionDiscount,
          timestamp: new Date().toISOString(),
          error: error,
          userId: this.userProfile?.id || 'guest'
        };
        
        paymentHistory.push(attempt);
        
        // Keep only last 100 payment attempts
        if (paymentHistory.length > 100) {
          paymentHistory.shift();
        }
        
        localStorage.setItem('ramyeon_payment_history', JSON.stringify(paymentHistory));
        console.log('Payment attempt tracked:', attempt);
      } catch (error) {
        console.error('Error tracking payment attempt:', error);
      }
    },
    
    
    // Setup payment diagnostics helper
    setupPaymentDiagnostics() {
      // Expose diagnostics helper in console
      window.ramyeonPaymentDiagnostics = {
        checkEnv: () => {
          console.log('🔍 PayMongo Environment Check:');
          // Check both Vue CLI and Vite environment variables
          const publicKey = (typeof process !== 'undefined' && process.env && process.env.VUE_APP_PAYMONGO_PUBLIC_KEY) || 
                           (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_PAYMONGO_PUBLIC_KEY);
          const secretKey = (typeof process !== 'undefined' && process.env && process.env.VUE_APP_PAYMONGO_SECRET_KEY) || 
                           (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_PAYMONGO_SECRET_KEY);
          const mode = (typeof process !== 'undefined' && process.env && process.env.VUE_APP_PAYMONGO_MODE) || 
                      (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_PAYMONGO_MODE) || 'test';
          
          console.log('Public Key:', publicKey ? '✅ Set' : '❌ Not Set');
          console.log('Secret Key:', secretKey ? '✅ Set' : '❌ Not Set');
          console.log('Mode:', mode);
          
          if (!secretKey) {
            console.error('❌ PayMongo keys not configured! Please set up your .env file.');
            console.log('📖 See PAYMENT_FIXES_AND_SETUP.md for instructions');
          }
        },
        
        viewHistory: () => {
          const history = JSON.parse(localStorage.getItem('ramyeon_payment_history') || '[]');
          console.log('📊 Payment History:', history);
          return history;
        },
        
        viewPendingOrder: () => {
          const pending = localStorage.getItem('ramyeon_pending_order');
          if (pending) {
            console.log('📦 Pending Order:', JSON.parse(pending));
          } else {
            console.log('No pending order');
          }
        },
        
        clearHistory: () => {
          localStorage.removeItem('ramyeon_payment_history');
          console.log('✅ Payment history cleared');
        },
        
        help: () => {
          console.log('🛠️ Ramyeon Payment Diagnostics:');
          console.log('  ramyeonPaymentDiagnostics.checkEnv() - Check PayMongo configuration');
          console.log('  ramyeonPaymentDiagnostics.viewHistory() - View payment history');
          console.log('  ramyeonPaymentDiagnostics.viewPendingOrder() - View pending order');
          console.log('  ramyeonPaymentDiagnostics.clearHistory() - Clear payment history');
          console.log('  ramyeonPaymentDiagnostics.help() - Show this help');
        },
        
        // Debug modal
        testShowModal: () => {
          const cartComponent = document.querySelector('.cart-page')?.__vueParentComponent?.ctx;
          if (cartComponent) {
            console.log('🧪 Forcing modal to show...');
            cartComponent.confirmedOrder = {
              id: 'TEST-123',
              total: '99.99',
              paymentMethod: 'test',
              deliveryType: 'delivery',
              paymentStatus: 'succeeded'
            };
            cartComponent.showOrderConfirmation = true;
            console.log('✅ Modal should be visible now');
          } else {
            console.error('❌ Could not find cart component');
          }
        },
        
        checkModalState: () => {
          const cartComponent = document.querySelector('.cart-page')?.__vueParentComponent?.ctx;
          if (cartComponent) {
            console.log('Modal State:');
            console.log('  showOrderConfirmation:', cartComponent.showOrderConfirmation);
            console.log('  confirmedOrder:', cartComponent.confirmedOrder);
            console.log('  Modal element:', document.querySelector('.confirmation-modal-overlay'));
          }
        },
        
        // Check if orders are being saved
        checkOrders: () => {
          console.log('📦 Checking saved orders...');
          
          // Check global orders
          const globalOrders = localStorage.getItem('ramyeon_orders');
          if (globalOrders) {
            const orders = JSON.parse(globalOrders);
            console.log('Global orders:', orders.length, 'orders');
            console.log(orders);
          } else {
            console.log('No global orders found');
          }
          
          // Check user-specific orders
          Object.keys(localStorage)
            .filter(key => key.startsWith('ramyeon_orders_'))
            .forEach(key => {
              const orders = JSON.parse(localStorage.getItem(key));
              console.log(`User orders (${key}):`, orders.length, 'orders');
              console.log(orders);
            });
        }
      };
      
      // Auto-check on mount
      console.log('💡 Payment diagnostics available! Type ramyeonPaymentDiagnostics.help() for options');
      console.log('💡 Test modal: ramyeonPaymentDiagnostics.testShowModal()');
    }
  },
  async mounted() {
    console.log('🔧 Cart component mounted');
    console.log('Full URL:', window.location.href);
    console.log('Hash:', window.location.hash);
    console.log('Search:', window.location.search);
    console.log('Pathname:', window.location.pathname);
    
    // Check if returning from payment (GCash, PayMaya, Card)
    // Only check if there are actual payment parameters in URL
    const hasPaymentParams = window.location.hash.includes('payment=') || window.location.search.includes('payment=');
    console.log('Hash includes payment=:', window.location.hash.includes('payment='));
    console.log('Search includes payment=:', window.location.search.includes('payment='));
    console.log('Has payment params in URL:', hasPaymentParams);
    
    if (hasPaymentParams) {
      console.log('🔍 Payment params detected in URL, checking payment return...');
      // Small delay to ensure component is fully mounted
      setTimeout(() => {
        this.checkPaymentReturn();
      }, 100);
    } else {
      if (CART_DEBUG) console.log('[Cart] No payment params in URL, skipping payment return check');
      // Clear any stale pending orders if no payment params
      const stalePendingOrder = localStorage.getItem('ramyeon_pending_order');
      if (stalePendingOrder) {
        if (CART_DEBUG) console.log('[Cart] Clearing stale pending order');
        localStorage.removeItem('ramyeon_pending_order');
      }
    }
    
    // Load user profile first
    this.loadUserProfile();
    
    // Load cart items from localStorage if available
    const savedCart = localStorage.getItem('ramyeon_cart');
    if (CART_DEBUG) console.log('[Cart] Loading cart from localStorage:', savedCart ? 'Found' : 'Empty');
    
    if (savedCart) {
      try {
        const parsedCart = JSON.parse(savedCart);
        if (CART_DEBUG) console.log('[Cart] Parsed cart items:', parsedCart.length);
        
        // Only load if it's a valid array
        if (Array.isArray(parsedCart)) {
          this.cartItems = parsedCart;
          if (CART_DEBUG) console.log('[Cart] Cart loaded:', this.cartItems.length, 'items');
        } else {
          // If invalid, clear it
          console.warn('⚠️ Invalid cart data, clearing');
          localStorage.removeItem('ramyeon_cart');
          this.cartItems = [];
        }
      } catch (error) {
        console.error('❌ Error loading cart:', error);
        localStorage.removeItem('ramyeon_cart');
        this.cartItems = [];
      }
    } else {
      console.log('ℹ️ No saved cart found');
      this.cartItems = [];
    }
    
    // Force update to ensure UI syncs
    this.$nextTick(() => {
      this.$forceUpdate();
      console.log('🔄 Forced cart UI update - displaying:', this.cartItems.length, 'items');
    });
    
    // Payment diagnostics helper
    this.setupPaymentDiagnostics();
    
    // Load active promotions regardless of login status (for per-item discounts)
    try {
      console.log('🎁 Loading active promotions for per-item discounts...');
      await this.getActivePromotions();
      console.log('✅ Active promotions loaded:', this.activePromotions.length);
      // Try auto-applying the best promotion on load
      await this.autoApplyBestPromotion();
    } catch (error) {
      console.error('❌ Error loading promotions:', error);
    }
    
    // Initialize composables with user data (only if logged in)
    if (this.userProfile) {
      try {
        await this.getLoyaltyBalance(this.userProfile.id);
        await this.getLoyaltyHistory(this.userProfile.id);
        await this.getCurrentTier(this.userProfile.id);
      } catch (error) {
        console.error('Error initializing loyalty composables:', error);
      }
    }
  },
  
  watch: {
    cartItems: {
      handler(newCart) {
        console.log('🔄 Cart items changed:', newCart.length, 'items');
        // Save cart to localStorage whenever it changes
        // Only save if cart has items
        if (newCart && newCart.length > 0) {
          localStorage.setItem('ramyeon_cart', JSON.stringify(newCart));
          console.log('💾 Saved cart to localStorage');
        } else {
          // If cart is empty, remove from localStorage
          localStorage.removeItem('ramyeon_cart');
          console.log('🧹 Removed cart from localStorage');
        }
        
        // Recalculate cart totals using composable
        this.calculateCartTotals();
        // Auto-apply best promotion when cart changes (only if none applied)
        this.autoApplyBestPromotion();
      },
      deep: true,
      immediate: false
    }
  },
  
  beforeUnmount() {
    console.log('🔧 Cart component unmounting');
    // Clean up diagnostics
    if (window.ramyeonPaymentDiagnostics) {
      delete window.ramyeonPaymentDiagnostics;
    }
  }
}
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 20px;
  font-family: 'Poppins', sans-serif;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-header {
  text-align: center;
  margin-bottom: 30px;
}

.cart-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.cart-header p {
  color: #666;
  font-size: 1.1rem;
}

.cart-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  align-items: start;
}

.cart-items {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: 15px;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.item-details h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.item-description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.item-price {
  font-weight: 600;
  color: #ff4757;
  font-size: 1.1rem;
}

.item-price-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.item-price.has-discount {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.original-price {
  text-decoration: line-through;
  color: #999;
  font-size: 0.9rem;
  font-weight: 500;
}

.current-price {
  color: #ff4757;
  font-weight: 700;
  font-size: 1.2rem;
}

.item-discount-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.discount-badge {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-block;
  width: fit-content;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.savings {
  color: #28a745;
  font-size: 0.8rem;
  font-weight: 600;
}

.total-with-discount {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 3px;
}

.original-total {
  text-decoration: line-through;
  color: #999;
  font-size: 0.9rem;
  font-weight: 500;
}

.discounted-total {
  color: #ff4757;
  font-weight: 700;
  font-size: 1.2rem;
}

.regular-total {
  font-weight: 700;
  font-size: 1.2rem;
  color: #333;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f9fa;
  border-radius: 25px;
  padding: 5px;
}

.quantity-btn {
  width: 35px;
  height: 35px;
  border: none;
  border-radius: 50%;
  background: #ff4757;
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quantity-btn:hover {
  background: #ff3742;
  transform: scale(1.1);
}

.quantity {
  font-weight: 600;
  font-size: 1.1rem;
  min-width: 30px;
  text-align: center;
}

.item-total {
  font-weight: 700;
  font-size: 1.2rem;
  color: #333;
}

.remove-btn {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 50%;
  background: #dc3545;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  background: #c82333;
  transform: scale(1.1);
}

.order-summary {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  position: sticky;
  top: 20px;
}

.order-summary h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 1rem;
}

.summary-row.total {
  border-top: 2px solid #eee;
  padding-top: 15px;
  font-weight: 700;
  font-size: 1.2rem;
  color: #ff4757;
}

.summary-row.discount-row {
  color: #28a745;
  font-weight: 600;
  font-size: 1.05rem;
}

.discount-amount {
  color: #28a745;
  font-weight: 700;
}

/* Promo Code Section */
.promo-code-section {
  margin: 20px 0;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.promo-input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.promo-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #eee;
  border-radius: 10px;
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.promo-input:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.promo-input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.apply-promo-btn,
.remove-promo-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.apply-promo-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  min-width: 90px;
}

.apply-promo-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #218838, #1aa179);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);
}

.apply-promo-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.remove-promo-btn {
  background: #dc3545;
  color: white;
}

.remove-promo-btn:hover {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.3);
}

.loading-spinner-small {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.applied-promo {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  padding: 15px;
  border-radius: 10px;
  margin-top: 10px;
  border: 2px solid #28a745;
}

.promo-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.promo-icon {
  font-size: 1.3rem;
}

.promo-name {
  font-weight: 700;
  color: #2e7d32;
  font-size: 1rem;
}

.promo-discount-info {
  color: #1b5e20;
  font-size: 0.9rem;
  font-weight: 600;
  margin-left: 30px;
}

.promo-error {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffebee;
  color: #c62828;
  padding: 10px 15px;
  border-radius: 8px;
  margin-top: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  border: 1px solid #ef5350;
}

.error-icon {
  font-size: 1.2rem;
}

/* Loyalty Points Section */
.loyalty-points-section {
  margin: 20px 0;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border-radius: 10px;
  padding: 20px;
}

.points-header {
  margin-bottom: 15px;
}

.points-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #f57c00;
}

.points-icon {
  font-size: 1.3rem;
}

.points-label {
  font-size: 1rem;
}

.points-balance {
  font-size: 1.2rem;
  font-weight: 700;
  color: #e65100;
}

.points-value {
  font-size: 0.9rem;
  color: #bf360c;
  font-weight: 500;
}

.points-redemption {
  margin-top: 15px;
}

.points-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  margin-bottom: 15px;
}

.points-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #ff9800;
}

.checkbox-text {
  font-weight: 600;
  color: #e65100;
  font-size: 1rem;
}

.points-input-group {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
}

.points-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ffb74d;
  border-radius: 10px;
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
  background: white;
}

.points-input:focus {
  outline: none;
  border-color: #ff9800;
  box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.1);
}

.points-discount {
  font-weight: 700;
  color: #e65100;
  font-size: 1rem;
  background: #fff3e0;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #ffb74d;
}

.summary-row.points-discount-row {
  color: #ff9800;
  font-weight: 600;
  font-size: 1.05rem;
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  padding: 8px 12px;
  border-radius: 8px;
  margin: 5px 0;
}

.loyalty-points-summary {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  border-radius: 10px;
  padding: 15px;
  margin-top: 15px;
  border: 2px solid #4caf50;
}

.points-used {
  color: #f44336;
  font-weight: 700;
}

.points-earned {
  color: #4caf50;
  font-weight: 700;
}

.points-insufficient {
  margin-top: 10px;
  padding: 10px 15px;
  background: #fff3e0;
  border: 1px solid #ffb74d;
  border-radius: 8px;
}

.insufficient-message {
  color: #e65100;
  font-weight: 600;
  font-size: 0.9rem;
}

.points-rates {
  margin-top: 5px;
  text-align: center;
}

.points-rates small {
  color: #f57c00;
  font-weight: 500;
  font-size: 0.8rem;
}

.delivery-options,
.payment-methods,
.special-instructions {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.delivery-options h2,
.payment-methods h2,
.special-instructions h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-label {
  display: block;
  cursor: pointer;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.option-label input[type="radio"]:checked + .option-content {
  border-color: #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.option-icon {
  font-size: 2rem;
}

.option-text h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.option-text p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.option-time {
  color: #ff4757;
  font-weight: 600;
  font-size: 0.9rem;
}

.delivery-address {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.delivery-address h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.address-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.address-field {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.3s ease;
}

.address-field:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.map-btn {
  padding: 15px 25px;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.map-btn:hover {
  background: #ff3742;
  transform: translateY(-2px);
}

.map-container {
  position: relative;
}

.map-instructions {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 15px;
  padding: 10px 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 3px solid #ff4757;
}

.google-map {
  height: 400px;
  width: 100%;
  border-radius: 15px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.close-map-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: white;
  border: none;
  padding: 10px 15px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.payment-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.payment-option {
  display: block;
  cursor: pointer;
}

.payment-content {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.payment-option input[type="radio"]:checked + .payment-content {
  border-color: #ff4757;
  background: rgba(255, 71, 87, 0.05);
}

.payment-icon {
  font-size: 1.5rem;
}

.instructions-field {
  width: 100%;
  min-height: 100px;
  padding: 15px 20px;
  border: 2px solid #eee;
  border-radius: 15px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  resize: vertical;
  transition: all 0.3s ease;
}

.instructions-field:focus {
  outline: none;
  border-color: #ff4757;
  box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.1);
}

.checkout-section {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.checkout-btn {
  width: 100%;
  padding: 20px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.checkout-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(255, 71, 87, 0.4);
}

.checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.empty-cart-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-cart h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.empty-cart p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.browse-menu-btn {
  padding: 15px 30px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.browse-menu-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 71, 87, 0.3);
}

/* Responsive Design */
@media (max-width: 992px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
  
  .order-summary {
    position: static;
  }
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
    gap: 10px;
  }
  
  .item-image {
    width: 60px;
    height: 60px;
  }
  
  .item-controls,
  .item-total,
  .remove-btn {
    grid-column: 2;
    justify-self: end;
    margin-top: 10px;
  }
  
  .payment-options {
    grid-template-columns: 1fr;
  }
  
  .address-input {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .cart-page {
    padding: 10px;
  }
  
  .cart-header h1 {
    font-size: 2rem;
  }
  
  .cart-items,
  .order-summary,
  .delivery-options,
  .payment-methods,
  .special-instructions,
  .checkout-section {
    padding: 20px;
  }
}

/* Modal Fade Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Order Confirmation Modal - GLOBAL STYLES (via teleport) */
/* Remove scoped to make this work at body level */


@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.confirmation-modal {
  background: white !important;
  border-radius: 25px;
  padding: 50px 40px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
  position: relative;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 1000000 !important;
  pointer-events: auto !important;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.confirmation-success-icon {
  margin-bottom: 30px;
}

.checkmark-circle {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #4caf50, #66bb6a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
  box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
}

@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.checkmark {
  width: 40px;
  height: 70px;
  border: solid white;
  border-width: 0 6px 6px 0;
  transform: rotate(45deg);
  animation: drawCheck 0.5s ease-out 0.5s both;
}

@keyframes drawCheck {
  from {
    height: 0;
    width: 0;
  }
  to {
    height: 70px;
    width: 40px;
  }
}

.confirmation-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 30px;
  animation: fadeInUp 0.5s ease-out 0.3s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.confirmation-details {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 25px;
  animation: fadeInUp 0.5s ease-out 0.4s both;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #dee2e6;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row.estimated-time {
  margin-top: 10px;
  padding-top: 20px;
  border-top: 2px solid #ff4757;
}

.detail-label {
  font-weight: 600;
  color: #666;
  font-size: 0.95rem;
}

.detail-value {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.detail-value.order-id {
  color: #ff4757;
  font-family: monospace;
  font-size: 0.9rem;
  background: #fff;
  padding: 5px 10px;
  border-radius: 8px;
}

.detail-value.total-amount {
  color: #4caf50;
  font-size: 1.3rem;
  font-weight: 700;
}

.confirmation-message {
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  animation: fadeInUp 0.5s ease-out 0.5s both;
}

.confirmation-message p {
  margin: 8px 0;
  color: #2e7d32;
  font-weight: 600;
  font-size: 1rem;
}

.confirmation-btn {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #ff4757, #ff3742);
  color: white;
  border: none;
  border-radius: 15px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  animation: fadeInUp 0.5s ease-out 0.6s both;
}

.confirmation-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(255, 71, 87, 0.4);
}

/* Responsive for modal */
@media (max-width: 480px) {
  .confirmation-modal {
    padding: 40px 25px;
  }
  
  .confirmation-title {
    font-size: 1.6rem;
  }
  
  .checkmark-circle {
    width: 80px;
    height: 80px;
  }
  
  .checkmark {
    width: 30px;
    height: 50px;
  }
}
</style>

<style>
/* GLOBAL Modal Styles - Not Scoped (for teleport to body) */
.confirmation-modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  background: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(10px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 2147483647 !important; /* Maximum z-index */
  animation: fadeIn 0.3s ease-out !important;
  pointer-events: auto !important;
  visibility: visible !important;
  opacity: 1 !important;
  margin: 0 !important;
  padding: 20px !important;
}

.confirmation-modal {
  background: white !important;
  border-radius: 25px !important;
  padding: 50px 40px !important;
  max-width: 500px !important;
  width: 90% !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
  text-align: center !important;
  position: relative !important;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  z-index: 2147483647 !important;
  pointer-events: auto !important;
  margin: auto !important;
}
</style>
