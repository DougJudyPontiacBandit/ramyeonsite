// Enhanced Online Order API Service
// Connected to PANN_POS enhanced online transaction endpoints
import apiClient from './api.js';

/**
 * Enhanced Online Order API Service
 * Provides comprehensive online order management with FIFO stock integration,
 * loyalty points, and real-time order tracking
 */
export const onlineOrderAPI = {
  /**
   * Create a new online order with enhanced features
   * @param {Object} orderData - Complete order data
   * @returns {Promise<Object>} Created order with order_id
   */
  createOrder: async (orderData) => {
    try {
      console.log('🛒 Creating enhanced online order:', orderData);
      
      const response = await apiClient.post('/online-orders/', {
        customer_id: orderData.customerId,
        items: orderData.items,
        delivery_address: orderData.deliveryAddress,
        payment_method: orderData.paymentMethod,
        special_instructions: orderData.specialInstructions,
        payment_reference: orderData.paymentReference,
        points_to_redeem: orderData.pointsToRedeem || 0,
        delivery_type: orderData.deliveryType || 'delivery',
        notes: orderData.notes || ''
      });
      
      console.log('✅ Order created successfully:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Order creation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to create order'
      };
    }
  },

  /**
   * Get order details by ID
   * @param {string} orderId - Order ID
   * @returns {Promise<Object>} Order details
   */
  getOrder: async (orderId) => {
    try {
      const response = await apiClient.get(`/online-orders/${orderId}/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching order:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch order'
      };
    }
  },

  /**
   * Get all orders for current customer
   * @param {Object} filters - Optional filters (status, date range, etc.)
   * @returns {Promise<Object>} Customer orders
   */
  getCustomerOrders: async (filters = {}) => {
    try {
      const response = await apiClient.get('/online-orders/customer/me/', {
        params: filters
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching customer orders:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch orders'
      };
    }
  },

  /**
   * Cancel an order
   * @param {string} orderId - Order ID to cancel
   * @param {string} reason - Cancellation reason
   * @returns {Promise<Object>} Cancellation result
   */
  cancelOrder: async (orderId, reason = 'Customer cancellation') => {
    try {
      console.log(`🚫 Cancelling order ${orderId}:`, reason);
      
      const response = await apiClient.post(`/online-orders/${orderId}/cancel/`, {
        reason: reason
      });
      
      console.log('✅ Order cancelled successfully');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Order cancellation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to cancel order'
      };
    }
  },

  /**
   * Update order status (for customer actions)
   * @param {string} orderId - Order ID
   * @param {string} status - New status
   * @returns {Promise<Object>} Update result
   */
  updateOrderStatus: async (orderId, status) => {
    try {
      const response = await apiClient.post(`/online-orders/${orderId}/status/`, {
        status: status
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error updating order status:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to update order status'
      };
    }
  },

  /**
   * Validate stock availability before order creation
   * @param {Array} items - Array of items to validate
   * @returns {Promise<Object>} Stock validation result
   */
  validateStock: async (items) => {
    try {
      console.log('📦 Validating stock for items:', items);
      
      const response = await apiClient.post('/online-orders/validate-stock/', {
        items: items
      });
      
      console.log('✅ Stock validation result:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Stock validation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate stock'
      };
    }
  },

  /**
   * Validate loyalty points redemption
   * @param {number} pointsToRedeem - Points to redeem
   * @param {number} subtotal - Order subtotal
   * @returns {Promise<Object>} Points validation result
   */
  validatePointsRedemption: async (pointsToRedeem, subtotal) => {
    try {
      console.log(`⭐ Validating points redemption: ${pointsToRedeem} points for ₱${subtotal}`);
      
      const response = await apiClient.post('/online-orders/validate-points/', {
        points_to_redeem: pointsToRedeem,
        subtotal: subtotal
      });
      
      console.log('✅ Points validation result:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Points validation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate points'
      };
    }
  },

  /**
   * Calculate loyalty points earned for an order
   * @param {number} subtotalAfterDiscount - Subtotal after all discounts
   * @returns {Promise<Object>} Points calculation result
   */
  calculateLoyaltyPoints: async (subtotalAfterDiscount) => {
    try {
      console.log(`⭐ Calculating loyalty points for ₱${subtotalAfterDiscount}`);
      
      const response = await apiClient.post('/online-orders/calculate-points/', {
        subtotal_after_discount: subtotalAfterDiscount
      });
      
      console.log('✅ Points calculation result:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Points calculation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to calculate points'
      };
    }
  },

  /**
   * Calculate service fee for delivery
   * @param {number} subtotal - Order subtotal
   * @param {string} deliveryType - Delivery type (delivery/pickup)
   * @returns {Promise<Object>} Service fee calculation
   */
  calculateServiceFee: async (subtotal, deliveryType = 'delivery') => {
    try {
      console.log(`💰 Calculating service fee for ₱${subtotal} (${deliveryType})`);
      
      const response = await apiClient.post('/online-orders/calculate-fee/', {
        subtotal: subtotal,
        delivery_type: deliveryType
      });
      
      console.log('✅ Service fee calculation result:', response.data);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('❌ Service fee calculation failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to calculate service fee'
      };
    }
  },

  /**
   * Get orders by status
   * @param {string} status - Order status (pending, processing, completed, cancelled)
   * @returns {Promise<Object>} Orders with specified status
   */
  getOrdersByStatus: async (status) => {
    try {
      const response = await apiClient.get(`/online-orders/status/${status}/`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching orders by status:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch orders'
      };
    }
  },

  /**
   * Get pending orders (orders awaiting processing)
   * @returns {Promise<Object>} Pending orders
   */
  getPendingOrders: async () => {
    try {
      const response = await apiClient.get('/online-orders/pending/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching pending orders:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch pending orders'
      };
    }
  },

  /**
   * Get processing orders (orders being prepared)
   * @returns {Promise<Object>} Processing orders
   */
  getProcessingOrders: async () => {
    try {
      const response = await apiClient.get('/online-orders/processing/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching processing orders:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch processing orders'
      };
    }
  },

  /**
   * Get order summary statistics
   * @param {Object} filters - Optional filters (date range, status, etc.)
   * @returns {Promise<Object>} Order summary statistics
   */
  getOrderSummary: async (filters = {}) => {
    try {
      const response = await apiClient.get('/online-orders/summary/', {
        params: filters
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching order summary:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch order summary'
      };
    }
  },

  /**
   * Check auto-cancellation status
   * @returns {Promise<Object>} Auto-cancellation settings and status
   */
  getAutoCancellationStatus: async () => {
    try {
      const response = await apiClient.get('/online-orders/auto-cancel/status/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching auto-cancellation status:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch auto-cancellation status'
      };
    }
  }
};

export default onlineOrderAPI;

