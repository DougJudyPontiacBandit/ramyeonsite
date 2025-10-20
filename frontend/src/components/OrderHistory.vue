<template>
  <div class="order-history-container">
    <div class="order-history-header">
      <h1>📦 Order History</h1>
      <p>View all your past orders</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading your orders...</p>
    </div>

    <!-- Orders List -->
    <div v-else-if="orders.length > 0" class="orders-list">
      <div v-for="order in sortedOrders" :key="order.id" class="order-card">
        <div class="order-header">
          <div class="order-info">
            <h3>{{ order.id }}</h3>
            <span class="order-date">{{ formatDate(order.orderTime) }}</span>
          </div>
          <div class="order-status" :class="'status-' + order.status">
            {{ formatStatus(order.status) }}
          </div>
        </div>

        <div class="order-items">
          <h4>Items Ordered:</h4>
          <div class="items-list">
            <div v-for="(item, index) in order.items" :key="index" class="order-item">
              <div class="item-info">
                <img :src="item.image" :alt="item.name" class="item-image" />
                <div class="item-details">
                  <p class="item-name">{{ item.name }}</p>
                  <p class="item-quantity">Qty: {{ item.quantity }}</p>
                </div>
              </div>
              <p class="item-price">₱{{ (item.price * item.quantity).toFixed(2) }}</p>
            </div>
          </div>
        </div>

        <div class="order-details">
          <div class="detail-row">
            <span>Subtotal:</span>
            <span>₱{{ order.subtotal.toFixed(2) }}</span>
          </div>
          <div class="detail-row">
            <span>Delivery Fee:</span>
            <span>₱{{ order.deliveryFee.toFixed(2) }}</span>
          </div>
          <div class="detail-row">
            <span>Service Fee:</span>
            <span>₱{{ order.serviceFee.toFixed(2) }}</span>
          </div>
          <div class="detail-row total">
            <span>Total:</span>
            <span>₱{{ order.total.toFixed(2) }}</span>
          </div>
        </div>

        <div class="order-footer">
          <div class="delivery-info">
            <p><strong>Delivery Type:</strong> {{ formatDeliveryType(order.deliveryType) }}</p>
            <p v-if="order.deliveryAddress"><strong>Address:</strong> {{ order.deliveryAddress }}</p>
          </div>
          <div class="payment-info">
            <p><strong>Payment Method:</strong> {{ formatPaymentMethod(order.paymentMethod) }}</p>
            <p><strong>Payment Status:</strong> 
              <span :class="'payment-' + order.paymentStatus">{{ formatPaymentStatus(order.paymentStatus) }}</span>
            </p>
          </div>
        </div>

        <div class="order-actions">
          <button @click="viewOrderDetails(order)" class="btn-details">View Details</button>
          <button v-if="order.status === 'pending'" @click="cancelOrder(order)" class="btn-cancel">Cancel Order</button>
          <button @click="reorder(order)" class="btn-reorder">Order Again</button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">📦</div>
      <h2>No Orders Yet</h2>
      <p>You haven't placed any orders yet. Start shopping!</p>
      <button @click="$emit('setCurrentPage', 'Menu')" class="browse-menu-btn">
        Browse Menu
      </button>
    </div>

    <!-- Order Details Modal -->
    <div v-if="selectedOrder" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Order Details</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <h3>Order Information</h3>
            <p><strong>Order ID:</strong> {{ selectedOrder.id }}</p>
            <p><strong>Date:</strong> {{ formatDate(selectedOrder.orderTime) }}</p>
            <p><strong>Status:</strong> {{ formatStatus(selectedOrder.status) }}</p>
          </div>
          <div class="detail-section">
            <h3>Items</h3>
            <div v-for="(item, index) in selectedOrder.items" :key="index" class="modal-item">
              <p>{{ item.name }} x {{ item.quantity }}</p>
              <p>₱{{ (item.price * item.quantity).toFixed(2) }}</p>
            </div>
          </div>
          <div class="detail-section">
            <h3>Delivery Information</h3>
            <p><strong>Type:</strong> {{ formatDeliveryType(selectedOrder.deliveryType) }}</p>
            <p v-if="selectedOrder.deliveryAddress"><strong>Address:</strong> {{ selectedOrder.deliveryAddress }}</p>
            <p v-if="selectedOrder.specialInstructions"><strong>Special Instructions:</strong> {{ selectedOrder.specialInstructions }}</p>
          </div>
          <div class="detail-section">
            <h3>Payment Information</h3>
            <p><strong>Method:</strong> {{ formatPaymentMethod(selectedOrder.paymentMethod) }}</p>
            <p><strong>Status:</strong> {{ formatPaymentStatus(selectedOrder.paymentStatus) }}</p>
            <p v-if="selectedOrder.paymentReference"><strong>Reference:</strong> {{ selectedOrder.paymentReference }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../services/api.js';

export default {
  name: 'OrderHistory',
  data() {
    return {
      orders: [],
      loading: false,
      selectedOrder: null,
      userProfile: null
    };
  },
  computed: {
    sortedOrders() {
      return [...this.orders].sort((a, b) => {
        return new Date(b.orderTime) - new Date(a.orderTime);
      });
    }
  },
  methods: {
    async loadOrders() {
      this.loading = true;
      try {
        // Get user profile first
        try {
          this.userProfile = await authAPI.getProfile();
        } catch (error) {
          console.log('Not logged in or failed to get profile');
        }
        
        // Load user-specific orders
        const userId = this.userProfile?.id || this.userProfile?.email || 'guest';
        const userOrdersKey = `ramyeon_orders_${userId}`;
        
        console.log('📦 Loading orders for user:', userId);
        
        const savedOrders = localStorage.getItem(userOrdersKey);
        if (savedOrders) {
          this.orders = JSON.parse(savedOrders);
          console.log('✅ Loaded', this.orders.length, 'orders for user');
        } else {
          // Fallback to global orders for backwards compatibility
          const globalOrders = localStorage.getItem('ramyeon_orders');
          if (globalOrders) {
            this.orders = JSON.parse(globalOrders);
            console.log('ℹ️ Loaded', this.orders.length, 'orders from global storage');
          } else {
            this.orders = [];
          }
        }
      } catch (error) {
        console.error('❌ Error loading orders:', error);
        this.orders = [];
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    formatStatus(status) {
      const statusMap = {
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'preparing': 'Preparing',
        'ready': 'Ready for Pickup',
        'out_for_delivery': 'Out for Delivery',
        'delivered': 'Delivered',
        'completed': 'Completed',
        'cancelled': 'Cancelled'
      };
      return statusMap[status] || status;
    },
    formatDeliveryType(type) {
      return type === 'delivery' ? 'Delivery' : 'Pick-up';
    },
    formatPaymentMethod(method) {
      const methodMap = {
        'cash': 'Cash on Delivery',
        'gcash': 'GCash',
        'paymaya': 'PayMaya',
        'card': 'Credit/Debit Card',
        'grabpay': 'GrabPay QR'
      };
      return methodMap[method] || method;
    },
    formatPaymentStatus(status) {
      const statusMap = {
        'pending': 'Pending',
        'succeeded': 'Paid',
        'failed': 'Failed',
        'refunded': 'Refunded'
      };
      return statusMap[status] || status;
    },
    viewOrderDetails(order) {
      this.selectedOrder = order;
    },
    closeModal() {
      this.selectedOrder = null;
    },
    cancelOrder(order) {
      if (confirm(`Are you sure you want to cancel order ${order.id}?`)) {
        // Update order status
        const orderIndex = this.orders.findIndex(o => o.id === order.id);
        if (orderIndex !== -1) {
          this.orders[orderIndex].status = 'cancelled';
          
          // Save to user-specific orders
          const userId = this.userProfile?.id || this.userProfile?.email || 'guest';
          const userOrdersKey = `ramyeon_orders_${userId}`;
          localStorage.setItem(userOrdersKey, JSON.stringify(this.orders));
          
          // Also update global orders
          localStorage.setItem('ramyeon_orders', JSON.stringify(this.orders));
          
          alert('Order cancelled successfully');
        }
      }
    },
    reorder(order) {
      // Add all items from this order to cart
      const cart = JSON.parse(localStorage.getItem('ramyeon_cart') || '[]');
      
      order.items.forEach(item => {
        const existingItem = cart.find(i => i.id === item.id);
        if (existingItem) {
          existingItem.quantity += item.quantity;
        } else {
          cart.push({ ...item });
        }
      });
      
      localStorage.setItem('ramyeon_cart', JSON.stringify(cart));
      alert('Items added to cart!');
      this.$emit('setCurrentPage', 'Cart');
    }
  },
  mounted() {
    console.log('📦 OrderHistory component mounted');
    this.loadOrders();
  },
  activated() {
    // Force reload when component is reactivated (keep-alive)
    console.log('📦 OrderHistory component activated - reloading orders');
    this.loadOrders();
  },
  watch: {
    // Reload orders when component becomes visible (if user navigates away and back)
    '$route'() {
      console.log('📦 Route changed in OrderHistory - reloading orders');
      this.loadOrders();
    }
  }
};
</script>

<style scoped>
.order-history-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f0 0%, #ffe6d9 100%);
}

.order-history-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 30px 20px;
  background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
  border-radius: 20px;
  color: white;
  box-shadow: 0 4px 20px rgba(255, 71, 87, 0.3);
}

.order-history-header h1 {
  margin: 0;
  font-size: 2.5em;
  font-weight: 700;
}

.order-history-header p {
  margin: 10px 0 0 0;
  opacity: 0.9;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ff4757;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.orders-list {
  display: grid;
  gap: 20px;
}

.order-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.order-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.order-info h3 {
  margin: 0;
  color: #2d3436;
  font-size: 1.3em;
}

.order-date {
  color: #636e72;
  font-size: 0.9em;
}

.order-status {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9em;
}

.status-pending {
  background: #ffeaa7;
  color: #fdcb6e;
}

.status-confirmed,
.status-preparing {
  background: #74b9ff;
  color: #0984e3;
}

.status-ready,
.status-out_for_delivery {
  background: #a29bfe;
  color: #6c5ce7;
}

.status-delivered,
.status-completed {
  background: #55efc4;
  color: #00b894;
}

.status-cancelled {
  background: #fab1a0;
  color: #e17055;
}

.order-items h4 {
  margin: 0 0 15px 0;
  color: #2d3436;
}

.items-list {
  display: grid;
  gap: 10px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 10px;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  display: flex;
  flex-direction: column;
}

.item-name {
  margin: 0;
  font-weight: 600;
  color: #2d3436;
}

.item-quantity {
  margin: 0;
  font-size: 0.9em;
  color: #636e72;
}

.item-price {
  font-weight: 700;
  color: #ff4757;
  margin: 0;
}

.order-details {
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin: 8px 0;
  font-size: 0.95em;
}

.detail-row.total {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 2px solid #dfe6e9;
  font-weight: 700;
  font-size: 1.1em;
  color: #ff4757;
}

.order-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
}

.delivery-info p,
.payment-info p {
  margin: 5px 0;
  font-size: 0.95em;
}

.payment-succeeded {
  color: #00b894;
  font-weight: 600;
}

.payment-pending {
  color: #fdcb6e;
  font-weight: 600;
}

.payment-failed {
  color: #e17055;
  font-weight: 600;
}

.order-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.order-actions button {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-details {
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  color: white;
}

.btn-details:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(9, 132, 227, 0.4);
}

.btn-cancel {
  background: linear-gradient(135deg, #fab1a0 0%, #e17055 100%);
  color: white;
}

.btn-cancel:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(225, 112, 85, 0.4);
}

.btn-reorder {
  background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
  color: white;
}

.btn-reorder:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 71, 87, 0.4);
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 5em;
  margin-bottom: 20px;
}

.empty-state h2 {
  color: #2d3436;
  margin: 0 0 10px 0;
}

.empty-state p {
  color: #636e72;
  margin: 0 0 30px 0;
}

.browse-menu-btn {
  padding: 15px 40px;
  background: linear-gradient(135deg, #ff6b35 0%, #ff4757 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.browse-menu-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(255, 71, 87, 0.4);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px;
  border-bottom: 2px solid #f0f0f0;
}

.modal-header h2 {
  margin: 0;
  color: #2d3436;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #636e72;
  padding: 5px 10px;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #ff4757;
}

.modal-body {
  padding: 25px;
}

.detail-section {
  margin-bottom: 25px;
}

.detail-section h3 {
  color: #2d3436;
  margin: 0 0 15px 0;
  font-size: 1.2em;
}

.detail-section p {
  margin: 8px 0;
  color: #636e72;
}

.modal-item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 8px 0;
}

@media (max-width: 768px) {
  .order-footer {
    grid-template-columns: 1fr;
  }

  .order-actions {
    flex-direction: column;
  }
}
</style>


