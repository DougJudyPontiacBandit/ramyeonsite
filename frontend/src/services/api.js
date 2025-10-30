// API Service for Backend Communication
import axios from 'axios';

// Base URL for API - prefer real .env keys used in project
// Allow runtime overrides for development without rebuilding:
// - URL param: ?api=https://pann-pos.onrender.com/api/v1
// - localStorage key: ramyeon_api_base_url
// - global: window.__RAMYEON_API__
const RUNTIME_API_OVERRIDE = (() => {
  try {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search).get('api');
      if (p) return p;
      const stored = localStorage.getItem('ramyeon_api_base_url');
      if (stored) return stored;
      // eslint-disable-next-line no-underscore-dangle
      if (window.__RAMYEON_API__) return window.__RAMYEON_API__;
    }
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn('[API] Runtime override parse error:', e);
  }
  return null;
})();

const API_BASE_URL =
  RUNTIME_API_OVERRIDE ||
  // Vite (import.meta.env)
  (typeof import.meta !== 'undefined' && import.meta.env && (
    import.meta.env.VITE_API_URL ||
    import.meta.env.VITE_API_BASE_URL ||
    import.meta.env.VUE_APP_API_URL
  ))
  // Vue CLI (process.env)
  || (typeof process !== 'undefined' && process.env && (
    process.env.VUE_APP_API_URL ||
    process.env.VITE_API_URL
  ))
  // Local fallback
  || 'http://localhost:8000/api/v1';

// Debug log the resolved API base URL once (helps diagnose env issues)
try {
  if (typeof window !== 'undefined') {
    // eslint-disable-next-line no-console
    console.log('[API] Resolved base URL:', API_BASE_URL);
    if (RUNTIME_API_OVERRIDE) console.log('[API] Using runtime override');
  }
} catch (e) {
  // eslint-disable-next-line no-console
  console.warn('[API] Failed to log base URL:', e);
}

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_SERVICE_TOKEN) {
      // Fallback service token for public pages hitting protected endpoints
      config.headers.Authorization = `Bearer ${import.meta.env.VITE_API_SERVICE_TOKEN}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API - Connected to /api/auth/customer/* endpoints
export const authAPI = {
  // Registration is not supported by current PANN_POS API
  register: async () => {
    throw { message: 'Registration is not supported by the current PANN_POS API' };
  },

  // Login (customer login via PANN_POS customer service)
  login: async (email, password) => {
    try {
      const response = await apiClient.post('/auth/customer/login/', { email, password });
      const { access_token, refresh_token } = response.data || {};
      if (access_token) {
        localStorage.setItem('access_token', access_token);
      }
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token);
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Login failed' };
    }
  },

  // Logout
  logout: async () => {
    try {
      // Clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('ramyeon_user_session');
    } catch (error) {
      // Still clear local storage even if there's an error
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('ramyeon_user_session');
    }
  },

  // Get current authenticated customer
  getProfile: async () => {
    try {
      const response = await apiClient.get('/auth/customer/me/');
      return response.data;
    } catch (error) {
      console.error('API Error in getProfile:', error);
      
      // Return more detailed error information
      const errorData = error.response?.data || { error: 'Network error' };
      const enhancedError = new Error(errorData.message || errorData.error || 'Failed to fetch profile');
      enhancedError.response = error.response;
      enhancedError.data = errorData;
      enhancedError.status = error.response?.status;
      
      throw enhancedError;
    }
  },

  // Password/profile updates are not supported by current PANN_POS API
  changePassword: async () => { throw { message: 'Password change is not supported by the current PANN_POS API' }; },
  updateProfile: async () => { throw { message: 'Profile update is not supported by the current PANN_POS API' }; },
};

// POS API - Connected to /api/pos/* endpoints (for cashier operations)
export const posAPI = {
  // POS QR and cashier-specific endpoints are not available in PANN_POS for the website
  scanUserQR: async () => { throw { message: 'POS QR scan is not supported by the current PANN_POS API' }; },
  scanPromotionQR: async () => { throw { message: 'POS promotion scan is not supported by the current PANN_POS API' }; },
  redeemPromotion: async () => { throw { message: 'POS promotion redemption is not supported by the current PANN_POS API' }; },
  awardPoints: async () => { throw { message: 'Manual points award is not supported by the current PANN_POS API' }; },
  processOrderPoints: async () => { throw { message: 'Order points processing is not supported by the current PANN_POS API' }; },
  getUserByQR: async () => { throw { message: 'POS user lookup by QR is not supported by the current PANN_POS API' }; },
  getPromotionByQR: async () => { throw { message: 'POS promotion lookup by QR is not supported by the current PANN_POS API' }; },
  getDashboard: async () => { throw { message: 'POS dashboard is not supported by the current PANN_POS API' }; },
};

// ============================================================================
// PLACEHOLDER APIs - These endpoints are not yet implemented in the backend
// Uncomment and use when backend endpoints are ready
// ============================================================================

// Products API - Connected to PANN_POS backend
export const productsAPI = {
  // Get all products
  getAll: async (params = {}) => {
    try {
      const response = await apiClient.get('/products/', { params });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch products:', error);
      throw error.response?.data || { message: 'Failed to fetch products' };
    }
  },

  // Get product by ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/products/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch product:', error);
      throw error.response?.data || { message: 'Failed to fetch product' };
    }
  },

  // Get products by category
  getByCategory: async (categoryId, subcategory = null, page = 1, limit = 20) => {
    try {
      const params = { page, limit };
      if (subcategory) {
        params.subcategory = subcategory;
      }
      const response = await apiClient.get(`/category/${categoryId}/subcategories/${subcategory || 'all'}/products/`, { params });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch products by category:', error);
      throw error.response?.data || { message: 'Failed to fetch products by category' };
    }
  },

  // Search products
  search: async (query) => {
    try {
      const response = await apiClient.get('/pos/search/', { params: { q: query } });
      return response.data;
    } catch (error) {
      console.error('Failed to search products:', error);
      throw error.response?.data || { message: 'Failed to search products' };
    }
  }
};

// Categories API - Connected to PANN_POS backend
export const categoriesAPI = {
  getAll: async () => {
    try {
      const response = await apiClient.get('/category/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      throw error.response?.data || { message: 'Failed to fetch categories' };
    }
  },

  // Get category by ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/category/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch category:', error);
      throw error.response?.data || { message: 'Failed to fetch category' };
    }
  },

  // Get subcategories
  getSubcategories: async (categoryId) => {
    try {
      const response = await apiClient.get(`/category/${categoryId}/subcategories/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch subcategories:', error);
      throw error.response?.data || { message: 'Failed to fetch subcategories' };
    }
  }
};

// Cart API (Currently commented out in backend)
export const cartAPI = {
  getCart: async () => {
    console.warn('Cart API not yet implemented in backend');
    return { items: [], total: 0 };
  },

  // eslint-disable-next-line no-unused-vars
  addItem: async (productId, quantity = 1) => {
    console.warn('Cart API not yet implemented in backend');
    return { message: 'Cart API not available' };
  },

  // eslint-disable-next-line no-unused-vars
  removeItem: async (itemId) => {
    console.warn('Cart API not yet implemented in backend');
    return { message: 'Cart API not available' };
  },

  clearCart: async () => {
    console.warn('Cart API not yet implemented in backend');
    return { message: 'Cart API not available' };
  },
};

// Enhanced Orders API - Connected to enhanced online transaction endpoints
export const ordersAPI = {
  // Get all orders for current user from database
  getAll: async (limit = 50, offset = 0) => {
    try {
      // Check if user is authenticated
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('⚠️ No token found, using localStorage fallback');
        const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
        return { success: true, results: orders };
      }

      // Fetch from customer order history endpoint
      const response = await apiClient.get('/online/orders/history/', {
        params: { limit, offset }
      });
      
      console.log('✅ Fetched orders from database:', response.data.count, 'orders');
      return { success: true, ...response.data };
    } catch (error) {
      console.error('❌ Error fetching orders from database:', error);
      // Fallback to localStorage only if database fails
      const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
      return { success: false, results: orders, error: error.message };
    }
  },

  // Create new order via enhanced online transaction API
  create: async (orderData) => {
    try {
      const items = Array.isArray(orderData?.items) ? orderData.items : [];
      const payload = {
        customer_id: orderData?.user?.id,
        items: items.map((item) => ({
          product_id: item.product_id || item.id || item.productId,
          quantity: item.quantity || 1,
          price: item.price || item.unit_price || 0,
          product_name: item.name || item.product_name,
        })),
        delivery_address: orderData?.delivery_address || {},
        delivery_type: orderData?.delivery_type || 'delivery',
        payment_method: (orderData?.payment_method || 'cod').toLowerCase(),
        points_to_redeem: (orderData?.loyalty_points ?? orderData?.pointsToRedeem) || 0,
        notes: orderData?.special_instructions || '',
      };
      console.log('ordersAPI.create payload:', payload);
      const response = await apiClient.post('/online/orders/create/', payload);
      return response.data;
    } catch (error) {
      const status = error?.response?.status;
      const data = error?.response?.data;
      const msg = (data && (data.message || data.error)) || error?.message || 'Failed to create order';
      console.error('Order creation API error:', { status, data });
      const err = new Error(msg);
      err.response = error?.response;
      err.data = data;
      throw err;
    }
  },

  // Get order by ID using enhanced API
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/sales/get/${id}/`);
      return response.data;
    } catch (error) {
      const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
      return orders.find(order => order.id === id) || null;
    }
  },

  // Cancel order using enhanced API
  cancel: async () => { throw { message: 'Order cancellation endpoint is not available in PANN_POS' }; },

  // Get order status with full tracking info
  getStatus: async (orderId) => {
    try {
      // Validate orderId
      if (!orderId) {
        console.error('❌ Order ID is required');
        return { success: false, error: 'Order ID is required' };
      }

      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('⚠️ No token found for order status');
        return { success: false, error: 'Not authenticated' };
      }

      const response = await apiClient.get(`/online/orders/${orderId}/status/`);
      console.log('✅ Order status fetched:', response.data);
      return { success: true, ...response.data };
    } catch (error) {
      console.error('❌ Error fetching order status:', error);
      
      // Handle specific error cases
      if (error.response) {
        if (error.response.status === 404) {
          return { success: false, error: 'Order not found' };
        } else if (error.response.status === 403) {
          return { success: false, error: 'Unauthorized access to order' };
        } else if (error.response.status === 401) {
          return { success: false, error: 'Authentication required' };
        }
        return { success: false, error: error.response.data?.message || 'Failed to fetch order status' };
      }
      
      return { success: false, error: error.message || 'Network error' };
    }
  },

  // Update order status (for POS/Admin)
  updateStatus: async (orderId, newStatus, notes = '') => {
    try {
      // Validate inputs
      if (!orderId) {
        console.error('❌ Order ID is required');
        return { success: false, error: 'Order ID is required' };
      }
      
      if (!newStatus) {
        console.error('❌ Status is required');
        return { success: false, error: 'Status is required' };
      }

      const token = localStorage.getItem('access_token');
      if (!token) {
        console.log('⚠️ No token found for order status update');
        return { success: false, error: 'Not authenticated' };
      }

      const response = await apiClient.post(`/online/orders/${orderId}/update-status/`, {
        status: newStatus,
        notes: notes || ''
      });
      console.log('✅ Order status updated:', response.data);
      return { success: true, ...response.data };
    } catch (error) {
      console.error('❌ Error updating order status:', error);
      
      // Handle specific error cases
      if (error.response) {
        if (error.response.status === 403) {
          return { success: false, error: 'Unauthorized. Only POS staff can update order status.' };
        } else if (error.response.status === 404) {
          return { success: false, error: 'Order not found' };
        } else if (error.response.status === 400) {
          return { success: false, error: error.response.data?.message || 'Invalid status' };
        } else if (error.response.status === 401) {
          return { success: false, error: 'Authentication required' };
        }
      }
      
      return { 
        success: false, 
        error: error.response?.data?.message || error.message || 'Failed to update order status'
      };
    }
  }
};

// Newsletter API (Currently commented out in backend)
export const newsletterAPI = {
  // eslint-disable-next-line no-unused-vars
  subscribe: async (email) => {
    console.warn('Newsletter API not yet implemented in backend');
    return { message: 'Newsletter subscription not available' };
  },
};

// Contact API (Currently commented out in backend)
export const contactAPI = {
  // eslint-disable-next-line no-unused-vars
  sendMessage: async (messageData) => {
    console.warn('Contact API not yet implemented in backend');
    return { message: 'Contact form not available' };
  },
};

// Enhanced Loyalty Points API - Connected to enhanced loyalty endpoints
export const loyaltyAPI = {
  // Get customer loyalty points balance (local fallback)
  getBalance: async () => {
    try {
      // Since backend doesn't have this endpoint, use local fallback
      console.log('💎 Using local loyalty balance fallback');
      return {
        success: true,
        balance: 0,
        points: 0,
        message: 'Using local fallback - backend endpoint not available'
      };
    } catch (error) {
      console.error('Error fetching loyalty balance:', error);
      return {
        success: false,
        error: error.message || 'Failed to fetch loyalty balance'
      };
    }
  },

  // Get customer loyalty points history (local fallback)
  getHistory: async (limit = 50) => {
    try {
      // Since backend doesn't have this endpoint, use local fallback
      console.log('📜 Using local loyalty history fallback (limit:', limit, ')');
      return {
        success: true,
        history: [],
        message: 'Using local fallback - backend endpoint not available'
      };
    } catch (error) {
      console.error('Error fetching loyalty history:', error);
      return {
        success: false,
        error: error.message || 'Failed to fetch loyalty history'
      };
    }
  },

  // Validate points redemption
  validateRedemption: async (pointsToRedeem, subtotal, customerId) => {
    try {
      // Fetch customer to check available points
      const response = await apiClient.get(`/customers/${customerId}/`);
      const available = response.data?.loyalty_points ?? 0;
      const valid = typeof pointsToRedeem === 'number' && pointsToRedeem > 0 && pointsToRedeem <= available;
      return { success: valid, available_points: available };
    } catch (error) {
      return { success: false, error: 'Failed to validate points redemption' };
    }
  },

  // Calculate loyalty points earned
  calculatePointsEarned: async (subtotalAfterDiscount) => {
    try {
      const subtotal = Number(subtotalAfterDiscount || 0);
      if (!Number.isFinite(subtotal) || subtotal <= 0) {
        return { success: true, data: { points_earned: 0 } };
      }
      // 20% earn rate (mirror backend service)
      const points = Math.floor(subtotal * 0.20);
      return { success: true, data: { points_earned: points } };
    } catch (e) {
      return { success: false, error: e.message || 'Failed to calculate points earned' };
    }
  },

  // Get current loyalty tier (local fallback)
  getCurrentTier: async (customerId) => {
    try {
      // Since backend doesn't have this endpoint, use local fallback
      console.log('👑 Using local loyalty tier fallback for customer:', customerId);
      return {
        success: true,
        tier: {
          name: 'Bronze',
          level: 1,
          min_points: 0,
          max_points: 999,
          benefits: ['Basic rewards']
        },
        message: 'Using local fallback - backend endpoint not available'
      };
    } catch (error) {
      console.error('Error fetching current tier:', error);
      return {
        success: false,
        error: error.message || 'Failed to fetch current tier'
      };
    }
  }
};

// Enhanced Stock Validation API - Connected to enhanced stock endpoints
export const stockAPI = {
  // Validate stock availability for order items
  validateStock: async (items) => {
    try {
      const checkout_data = (items || []).map((item) => ({
        product_id: item.product_id || item.id || item.productId,
        quantity: item.quantity || 1,
        price: item.price || item.unit_price || 0,
      }));
      const response = await apiClient.post('/pos/stock-validation/', { checkout_data });
      return response.data;
    } catch (error) {
      return { success: false, error: 'Failed to validate stock' };
    }
  },

  // Check individual product stock
  checkProductStock: async (productId, quantity) => {
    try {
      const checkout_data = [{ product_id: productId, quantity: quantity || 1, price: 0 }];
      const response = await apiClient.post('/pos/stock-validation/', { checkout_data });
      return response.data;
    } catch (error) {
      return { success: false, error: 'Failed to check product stock' };
    }
  }
};

// Enhanced Promotions API - Connected to enhanced promotion endpoints
export const promotionsAPI = {
  // Get active promotions
  getActive: async () => {
    try {
      const response = await apiClient.get('/promotions/active/');
      // Backend returns {success: true, promotions: [...]}
      return response.data;
    } catch (error) {
      console.error('Error fetching active promotions:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to fetch promotions'
      };
    }
  },

  // Apply promotion to cart
  applyPromotion: async (promotionCode, cartItems) => {
    try {
      const response = await apiClient.post('/promotions/apply/', {
        promotion_code: promotionCode,
        cart_items: cartItems
      });
      return response.data;
    } catch (error) {
      console.error('Error applying promotion:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to apply promotion'
      };
    }
  },

  // Validate promotion eligibility
  validatePromotion: async (promotionCode, cartItems) => {
    // No separate validate endpoint; reuse apply endpoint
    try {
      const response = await apiClient.post('/promotions/apply/', {
        promotion_code: promotionCode,
        cart_items: cartItems
      });
      return response.data;
    } catch (error) {
      console.error('Error validating promotion:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate promotion'
      };
    }
  }
};

export default apiClient;
