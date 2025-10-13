// Customer Categories API Service
import apiClient from './api.js';

/**
 * Customer Categories API - Connected to /api/customer/categories/* endpoints
 * All methods are read-only and show only active categories with available products
 */
export const categoriesAPI = {
  /**
   * Get all active categories with product counts
   * Only returns categories that have products in stock
   * @returns {Promise<Object>} Response with categories array
   * 
   * @example
   * const response = await categoriesAPI.getAll();
   * console.log(response.data.categories);
   */
  getAll: async () => {
    try {
      const response = await apiClient.get('/customer/categories/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch categories' };
    }
  },

  /**
   * Get single category details with subcategories
   * Includes product counts for each subcategory
   * @param {string} categoryId - Category ID (CTGY-### format)
   * @returns {Promise<Object>} Category details with subcategories
   * 
   * @example
   * const response = await categoriesAPI.getById('CTGY-001');
   * console.log(response.data);
   */
  getById: async (categoryId) => {
    try {
      if (!categoryId || !categoryId.startsWith('CTGY-')) {
        throw { message: 'Invalid category ID format. Expected CTGY-###' };
      }
      
      const response = await apiClient.get(`/customer/categories/${categoryId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch category details' };
    }
  },

  /**
   * Get category with its available products (paginated)
   * @param {string} categoryId - Category ID (CTGY-### format)
   * @param {string|null} subcategoryName - Optional subcategory filter
   * @param {number} page - Page number (default: 1)
   * @param {number} limit - Items per page (default: 20)
   * @returns {Promise<Object>} Category info with products array and pagination
   * 
   * @example
   * // Get category with all products
   * const response = await categoriesAPI.getWithProducts('CTGY-001', null, 1, 20);
   * 
   * // Get category with products from specific subcategory
   * const response = await categoriesAPI.getWithProducts('CTGY-001', 'Instant', 1, 20);
   */
  getWithProducts: async (categoryId, subcategoryName = null, page = 1, limit = 20) => {
    try {
      if (!categoryId || !categoryId.startsWith('CTGY-')) {
        throw { message: 'Invalid category ID format. Expected CTGY-###' };
      }
      
      const params = { page, limit };
      if (subcategoryName) {
        params.subcategory_name = subcategoryName;
      }
      
      const response = await apiClient.get(`/customer/categories/${categoryId}/products/`, { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch category products' };
    }
  },

  /**
   * Get all categories with their subcategories (detailed view)
   * Useful for building navigation menus
   * @returns {Promise<Object>} Categories with nested subcategories
   * 
   * @example
   * const response = await categoriesAPI.getAllWithSubcategories();
   * // Use for building mega menu or category navigation
   */
  getAllWithSubcategories: async () => {
    try {
      const response = await apiClient.get('/customer/categories/');
      
      // Categories already include subcategories from backend
      // This method exists for semantic clarity
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch categories with subcategories' };
    }
  },

  /**
   * Get subcategories for a specific category
   * @param {string} categoryId - Category ID (CTGY-### format)
   * @returns {Promise<Array>} Array of subcategories
   * 
   * @example
   * const subcategories = await categoriesAPI.getSubcategories('CTGY-001');
   * console.log(subcategories);
   */
  getSubcategories: async (categoryId) => {
    try {
      if (!categoryId || !categoryId.startsWith('CTGY-')) {
        throw { message: 'Invalid category ID format. Expected CTGY-###' };
      }
      
      const response = await apiClient.get(`/customer/categories/${categoryId}/`);
      
      // Extract subcategories from response
      if (response.success && response.data) {
        return response.data.sub_categories || [];
      }
      
      return [];
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch subcategories' };
    }
  },

  /**
   * Get category tree for navigation
   * Returns hierarchical structure suitable for menus
   * @returns {Promise<Array>} Category tree structure
   * 
   * @example
   * const categoryTree = await categoriesAPI.getCategoryTree();
   * // Use for rendering nested navigation menus
   */
  getCategoryTree: async () => {
    try {
      const response = await apiClient.get('/customer/categories/');
      
      if (response.success && response.data) {
        // Transform flat categories into tree structure
        const categories = response.data.categories || [];
        
        return categories.map(category => ({
          id: category._id,
          name: category.category_name,
          description: category.description,
          productCount: category.product_count,
          image: category.image_url,
          subcategories: (category.sub_categories || []).map(subcat => ({
            id: subcat.subcategory_id,
            name: subcat.name,
            productCount: subcat.product_count
          }))
        }));
      }
      
      return [];
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch category tree' };
    }
  },
};

export default categoriesAPI;