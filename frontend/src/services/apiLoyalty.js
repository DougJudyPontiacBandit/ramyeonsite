// Customer Loyalty Points API Service
import apiClient from './api.js';

/**
 * Customer Loyalty Points API - Connected to /api/customer/loyalty/* endpoints
 * Handles loyalty points management for customers
 */
export const loyaltyAPI = {
  /**
   * Get customer loyalty points balance
   * Note: customerId is not needed as it's retrieved from JWT token
   * @returns {Promise<Object>} Customer points data
   */
  getBalance: async () => {
    try {
      // Check if user is authenticated before making the request
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('ℹ️ Loyalty balance API unavailable, using fallback');
        return {
          success: true,
          data: { balance: 0 },
          fallback: true
        };
      }
      
      const response = await apiClient.get('/customer/loyalty/balance/');
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
   * Note: customerId is not needed as it's retrieved from JWT token
   * @param {number} limit - Items per page (default: 50)
   * @returns {Promise<Object>} Points transaction history
   */
  getHistory: async (limit = 50) => {
    try {
      // Check if user is authenticated before making the request
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('ℹ️ Loyalty history API unavailable, using fallback');
        return {
          success: true,
          data: { history: [], results: [] },
          fallback: true
        };
      }
      
      const response = await apiClient.get('/customer/loyalty/history/', {
        params: { limit }
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
   * Note: customerId is retrieved from JWT token, orderSubtotal not used in backend validation
   * @param {number} pointsToRedeem - Points to redeem
   * @returns {Promise<Object>} Validation result
   */
  validateRedemption: async (pointsToRedeem) => {
    try {
      const response = await apiClient.post('/customer/loyalty/validate-redemption/', {
        points_to_redeem: pointsToRedeem
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
   * Note: This endpoint is not implemented in the unified backend yet
   * @returns {Promise<Object>} Points expiration data
   */
  getExpirationInfo: async () => {
    // This endpoint doesn't exist in the unified backend yet
    // Return a placeholder response for now
    return {
      success: true,
      data: {
        message: 'Points expiration feature not implemented yet',
        expiration_date: null
      }
    };
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
   * Get loyalty tiers
   * @returns {Promise<Object>} Loyalty tiers
   */
  getTiers: async () => {
    try {
      const response = await apiClient.get('/customer/loyalty/tiers/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching loyalty tiers:', error);
      // Return default tiers if backend is unavailable
      return {
        success: true,
        data: {
          tiers: [
            { name: 'Bronze', min_points: 0, max_points: 499, multiplier: 1.0 },
            { name: 'Silver', min_points: 500, max_points: 1499, multiplier: 1.25 },
            { name: 'Gold', min_points: 1500, max_points: 2999, multiplier: 1.5 },
            { name: 'Platinum', min_points: 3000, max_points: null, multiplier: 2.0 }
          ]
        }
      };
    }
  },

  /**
   * Get current loyalty tier for customer
   * Note: customerId is retrieved from JWT token
   * @returns {Promise<Object>} Current tier
   */
  getCurrentTier: async () => {
    try {
      // Check if user is authenticated before making the request
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('ℹ️ Loyalty tier API unavailable, using fallback');
        return {
          success: true,
          data: {
            name: 'Bronze',
            min_points: 0,
            max_points: 499,
            multiplier: 1.0
          },
          fallback: true
        };
      }
      
      const response = await apiClient.get('/customer/loyalty/current-tier/');
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Error fetching current tier:', error);
      // Return default Bronze tier if backend is unavailable
      return {
        success: true,
        data: {
          name: 'Bronze',
          min_points: 0,
          max_points: 499,
          multiplier: 1.0
        },
        fallback: true
      };
    }
  },

  /**
   * Health check for loyalty service
   * @returns {Promise<Object>} Service health status
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/customer/loyalty/health/');
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
