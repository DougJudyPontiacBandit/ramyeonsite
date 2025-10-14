// Customer Promotions API Service
import apiClient from './api.js';

/**
 * Customer Promotions API - Connected to /api/customer/promotions/* endpoints
 * All methods are read-only and show only active promotions
 */
export const promotionsAPI = {
  /**
   * Get all active promotions with filters and pagination
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number (default: 1)
   * @param {number} params.limit - Items per page (default: 20)
   * @param {string} params.type - Filter by type (percentage, fixed_amount, buy_x_get_y)
   * @param {string} params.target_type - Filter by target (all, products, categories)
   * @param {string} params.q - Search by name or description
   * @param {string} params.sort_by - Field to sort by (default: created_at)
   * @param {string} params.sort_order - asc or desc (default: desc)
   * @returns {Promise<Object>} Response with promotions array and pagination info
   *
   * @example
   * const response = await promotionsAPI.getAll({
   *   page: 1,
   *   limit: 20,
   *   type: 'percentage'
   * });
   * console.log(response.promotions);
   */
  getAll: async (params = {}) => {
    try {
      const response = await apiClient.get('/customer/promotions/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotions' };
    }
  },

  /**
   * Get single promotion details by ID
   * @param {string} promotionId - Promotion ID (PROM-#### format)
   * @returns {Promise<Object>} Promotion details with computed fields
   *
   * @example
   * const response = await promotionsAPI.getById('PROM-0001');
   * console.log(response.promotion);
   */
  getById: async (promotionId) => {
    try {
      if (!promotionId || !promotionId.startsWith('PROM-')) {
        throw { message: 'Invalid promotion ID format. Expected PROM-####' };
      }

      const response = await apiClient.get(`/customer/promotions/${promotionId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotion details' };
    }
  },

  /**
   * Get all currently active promotions
   * Only returns promotions that are active and within their valid date range
   * @returns {Promise<Object>} Response with active promotions array
   *
   * @example
   * const response = await promotionsAPI.getActive();
   * console.log(response.promotions);
   */
  getActive: async () => {
    try {
      const response = await apiClient.get('/customer/promotions/active/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch active promotions' };
    }
  },

  /**
   * Search promotions by name or description
   * @param {string} searchTerm - Search query
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Search results with matching promotions
   *
   * @example
   * const response = await promotionsAPI.search('summer sale', 1, 20);
   * console.log(response.promotions);
   */
  search: async (searchTerm, page = 1, limit = 20) => {
    try {
      if (!searchTerm || searchTerm.trim().length === 0) {
        throw { message: 'Search term is required' };
      }

      const response = await apiClient.get('/customer/promotions/search/', {
        params: { q: searchTerm.trim(), page, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to search promotions' };
    }
  },

  /**
   * Get all active promotions applicable to a specific product
   * @param {string} productId - Product ID (PROD-##### format)
   * @returns {Promise<Object>} Promotions applicable to the product
   *
   * @example
   * const response = await promotionsAPI.getByProduct('PROD-00001');
   * console.log(response.promotions);
   */
  getByProduct: async (productId) => {
    try {
      if (!productId || !productId.startsWith('PROD-')) {
        throw { message: 'Invalid product ID format. Expected PROD-#####' };
      }

      const response = await apiClient.get(`/customer/promotions/product/${productId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotions for product' };
    }
  },

  /**
   * Get all active promotions applicable to a specific category
   * @param {string} categoryId - Category ID (CTGY-### format)
   * @returns {Promise<Object>} Promotions applicable to the category
   *
   * @example
   * const response = await promotionsAPI.getByCategory('CTGY-001');
   * console.log(response.promotions);
   */
  getByCategory: async (categoryId) => {
    try {
      if (!categoryId || !categoryId.startsWith('CTGY-')) {
        throw { message: 'Invalid category ID format. Expected CTGY-###' };
      }

      const response = await apiClient.get(`/customer/promotions/category/${categoryId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotions for category' };
    }
  },

  /**
   * Calculate the best discount for an order
   * This is a preview calculation and doesn't track usage
   * @param {Object} orderData - Order information
   * @param {Array} orderData.items - Array of order items
   * @param {string} orderData.items[].product_id - Product ID
   * @param {string} orderData.items[].category_id - Category ID (optional)
   * @param {number} orderData.items[].price - Item price
   * @param {number} orderData.items[].quantity - Item quantity
   * @param {number} orderData.total_amount - Total order amount
   * @returns {Promise<Object>} Discount calculation result
   *
   * @example
   * const response = await promotionsAPI.calculateDiscount({
   *   total_amount: 100.00,
   *   items: [
   *     {
   *       product_id: 'PROD-00001',
   *       category_id: 'CTGY-001',
   *       price: 50.00,
   *       quantity: 2
   *     }
   *   ]
   * });
   * console.log(response.discount_applied);
   * console.log(response.promotion_used);
   */
  calculateDiscount: async (orderData) => {
    try {
      // Validate order data
      if (!orderData || !orderData.items || orderData.items.length === 0) {
        throw { message: 'Order must include items' };
      }

      if (!orderData.total_amount || orderData.total_amount <= 0) {
        throw { message: 'Order must include a valid total_amount' };
      }

      const response = await apiClient.post('/customer/promotions/calculate-discount/', orderData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to calculate discount' };
    }
  },

  /**
   * Health check for promotions service
   * @returns {Promise<Object>} Service health status
   *
   * @example
   * const response = await promotionsAPI.healthCheck();
   * console.log(response.status);
   */
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/customer/promotions/health/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Health check failed' };
    }
  },

  /**
   * Get promotions filtered by type
   * @param {string} type - Promotion type (percentage, fixed_amount, buy_x_get_y)
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Promotions of specified type
   *
   * @example
   * const response = await promotionsAPI.getByType('percentage', 1, 20);
   */
  getByType: async (type, page = 1, limit = 20) => {
    try {
      if (!type || !['percentage', 'fixed_amount', 'buy_x_get_y'].includes(type)) {
        throw { message: 'Invalid promotion type. Must be percentage, fixed_amount, or buy_x_get_y' };
      }

      const params = { type, page, limit };
      const response = await apiClient.get('/customer/promotions/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotions by type' };
    }
  },

  /**
   * Get promotions filtered by target type
   * @param {string} targetType - Target type (all, products, categories)
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Promotions of specified target type
   *
   * @example
   * const response = await promotionsAPI.getByTargetType('products', 1, 20);
   */
  getByTargetType: async (targetType, page = 1, limit = 20) => {
    try {
      if (!targetType || !['all', 'products', 'categories'].includes(targetType)) {
        throw { message: 'Invalid target type. Must be all, products, or categories' };
      }

      const params = { target_type: targetType, page, limit };
      const response = await apiClient.get('/customer/promotions/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch promotions by target type' };
    }
  },

  /**
   * Get promotions sorted by discount value
   * @param {string} order - 'asc' for low to high, 'desc' for high to low
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Promotions sorted by discount value
   *
   * @example
   * // Get highest discounts first
   * const response = await promotionsAPI.sortByDiscount('desc', 1, 20);
   */
  sortByDiscount: async (order = 'desc', page = 1, limit = 20) => {
    try {
      const params = {
        sort_by: 'discount_value',
        sort_order: order,
        page,
        limit
      };

      const response = await apiClient.get('/customer/promotions/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to sort promotions by discount' };
    }
  },
};

export default promotionsAPI;
