// Customer Products API Service
import apiClient from './api.js';

/**
 * Customer Products API - Connected to /api/customer/products/* endpoints
 * All methods are read-only and show only active, in-stock products
 */
export const productsAPI = {
  /**
   * Get all active products with filters and pagination
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number (default: 1)
   * @param {number} params.limit - Items per page (default: 20)
   * @param {string} params.category_id - Filter by category (CTGY-###)
   * @param {string} params.subcategory_name - Filter by subcategory
   * @param {string} params.search - Search by product name or SKU
   * @param {number} params.min_price - Minimum price filter
   * @param {number} params.max_price - Maximum price filter
   * @param {string} params.sort_by - Field to sort by (default: product_name)
   * @param {string} params.sort_order - asc or desc (default: asc)
   * @returns {Promise<Object>} Response with products array and pagination info
   * 
   * @example
   * const response = await productsAPI.getAll({ 
   *   page: 1, 
   *   limit: 20, 
   *   category_id: 'CTGY-001' 
   * });
   * console.log(response.data.products);
   */
  getAll: async (params = {}) => {
    try {
      const response = await apiClient.get('/customer/products/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch products' };
    }
  },

  /**
   * Get single product details by ID
   * @param {string} productId - Product ID (PROD-##### format)
   * @returns {Promise<Object>} Product details with promotions
   * 
   * @example
   * const response = await productsAPI.getById('PROD-00001');
   * console.log(response.data);
   */
  getById: async (productId) => {
    try {
      if (!productId || !productId.startsWith('PROD-')) {
        throw { message: 'Invalid product ID format. Expected PROD-#####' };
      }
      
      const response = await apiClient.get(`/customer/products/${productId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch product details' };
    }
  },

  /**
   * Search products by name or SKU
   * @param {string} searchTerm - Search query
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Search results with matching products
   * 
   * @example
   * const response = await productsAPI.search('ramen', 1, 20);
   * console.log(response.data.products);
   */
  search: async (searchTerm, page = 1, limit = 20) => {
    try {
      if (!searchTerm || searchTerm.trim().length === 0) {
        throw { message: 'Search term is required' };
      }
      
      const response = await apiClient.get('/customer/products/search/', {
        params: { q: searchTerm.trim(), page, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to search products' };
    }
  },

  /**
   * Get products by category and optional subcategory
   * @param {string} categoryId - Category ID (CTGY-### format)
   * @param {string|null} subcategoryName - Optional subcategory filter
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Products in specified category
   * 
   * @example
   * // Get all products in category
   * const response = await productsAPI.getByCategory('CTGY-001', null, 1, 20);
   * 
   * // Get products in specific subcategory
   * const response = await productsAPI.getByCategory('CTGY-001', 'Instant', 1, 20);
   */
  getByCategory: async (categoryId, subcategoryName = null, page = 1, limit = 20) => {
    try {
      if (!categoryId || !categoryId.startsWith('CTGY-')) {
        throw { message: 'Invalid category ID format. Expected CTGY-###' };
      }
      
      const params = { page, limit };
      if (subcategoryName) {
        params.subcategory_name = subcategoryName;
      }
      
      const response = await apiClient.get(`/customer/products/category/${categoryId}/`, { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch category products' };
    }
  },

  /**
   * Get featured products for homepage
   * @param {number} limit - Number of featured products (default: 10, max: 50)
   * @returns {Promise<Object>} Featured products array
   * 
   * @example
   * const response = await productsAPI.getFeatured(10);
   * console.log(response.data.products);
   */
  getFeatured: async (limit = 10) => {
    try {
      // Validate limit
      const validLimit = Math.min(Math.max(1, limit), 50); // Between 1 and 50
      
      const response = await apiClient.get('/customer/products/featured/', {
        params: { limit: validLimit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch featured products' };
    }
  },

  /**
   * Get products with price range filter
   * @param {number} minPrice - Minimum price
   * @param {number} maxPrice - Maximum price
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Products within price range
   * 
   * @example
   * const response = await productsAPI.getByPriceRange(10, 50, 1, 20);
   */
  getByPriceRange: async (minPrice, maxPrice, page = 1, limit = 20) => {
    try {
      const params = { 
        min_price: minPrice, 
        max_price: maxPrice,
        page,
        limit
      };
      
      const response = await apiClient.get('/customer/products/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch products by price range' };
    }
  },

  /**
   * Get products sorted by price
   * @param {string} order - 'asc' for low to high, 'desc' for high to low
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Products sorted by price
   * 
   * @example
   * // Get cheapest products first
   * const response = await productsAPI.sortByPrice('asc', 1, 20);
   * 
   * // Get most expensive products first
   * const response = await productsAPI.sortByPrice('desc', 1, 20);
   */
  sortByPrice: async (order = 'asc', page = 1, limit = 20) => {
    try {
      const params = {
        sort_by: 'selling_price',
        sort_order: order,
        page,
        limit
      };
      
      const response = await apiClient.get('/customer/products/', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to sort products by price' };
    }
  },
};

export default productsAPI;