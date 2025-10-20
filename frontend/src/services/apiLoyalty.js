// Customer Loyalty Points API Service
import apiClient from './api.js';

/**
 * Customer Loyalty Points API - Connected to /api/customer/loyalty/* endpoints
 * Handles loyalty points management for customers
 */
export const loyaltyAPI = {
  /**
   * Get customer loyalty points balance
   * @param {string} customerId - Customer ID
   * @returns {Promise<Object>} Customer points data
   */
  getBalance: async (customerId) => {
    try {
      const response = await apiClient.get(`/customer/loyalty/balance/${customerId}`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching loyalty balance:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch loyalty balance'
      };
    }
  },

  /**
   * Get customer loyalty points history
   * @param {string} customerId - Customer ID
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Points transaction history
   */
  getHistory: async (customerId, page = 1, limit = 20) => {
    try {
      const response = await apiClient.get(`/customer/loyalty/history/${customerId}`, {
        params: { page, limit }
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching loyalty history:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch loyalty history'
      };
    }
  },

  /**
   * Validate points redemption
   * @param {string} customerId - Customer ID
   * @param {number} pointsToRedeem - Points to redeem
   * @param {number} orderSubtotal - Order subtotal
   * @returns {Promise<Object>} Validation result
   */
  validateRedemption: async (customerId, pointsToRedeem, orderSubtotal) => {
    try {
      const response = await apiClient.post('/customer/loyalty/validate-redemption', {
        customer_id: customerId,
        points_to_redeem: pointsToRedeem,
        order_subtotal: orderSubtotal
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error validating points redemption:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate points redemption'
      };
    }
  },

  /**
   * Calculate points discount
   * @param {number} pointsToRedeem - Points to redeem
   * @returns {number} Discount amount in pesos
   */
  calculateDiscount: (pointsToRedeem) => {
    // 4 points = ₱1 discount
    return pointsToRedeem / 4.0;
  },

  /**
   * Calculate points to earn
   * @param {number} orderAmount - Order amount after discount
   * @returns {number} Points to earn (20% of order amount)
   */
  calculatePointsEarned: (orderAmount) => {
    return Math.floor(orderAmount * 0.20);
  },

  /**
   * Get points expiration info
   * @param {string} customerId - Customer ID
   * @returns {Promise<Object>} Points expiration data
   */
  getExpirationInfo: async (customerId) => {
    try {
      const response = await apiClient.get(`/customer/loyalty/expiration/${customerId}`);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching points expiration:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch points expiration'
      };
    }
  },

  /**
   * Redeem loyalty points
   * @param {number} pointsToRedeem - Points to redeem
   * @param {string} orderId - Order ID
   * @returns {Promise<Object>} Redemption result
   */
  redeemPoints: async (pointsToRedeem, orderId) => {
    try {
      const response = await apiClient.post('/customer/loyalty/redeem/', {
        points_to_redeem: pointsToRedeem,
        order_id: orderId
      });
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error redeeming points:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to redeem points'
      };
    }
  },

  /**
   * Award loyalty points
   * @param {number} orderAmount - Order amount after discount
   * @param {string} orderId - Order ID
   * @returns {Promise<Object>} Award result
   */
  awardPoints: async (orderAmount, orderId) => {
    try {
      const response = await apiClient.post('/customer/loyalty/award/', {
        order_amount: orderAmount,
        order_id: orderId
      });
      return {
        success: true,
        award: response.data
      };
    } catch (error) {
      console.error('Error awarding points:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to award points'
      };
    }
  },

  /**
   * Health check for loyalty service
   * @returns {Promise<Object>} Service health status
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/customer/loyalty/health');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Loyalty service health check failed:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Loyalty service unavailable'
      };
    }
  }
};

export default loyaltyAPI;
