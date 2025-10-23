// API Service for Backend Communication
import axios from 'axios';

// Base URL for API - adjusted to match the unified PANN_POS backend
const API_BASE_URL = 'http://localhost:8000/api/v1';

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
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API - Connected to /api/auth/customer/* endpoints
export const authAPI = {
  // Register new customer
  register: async (userData) => {
    try {
      const response = await apiClient.post('/auth/customer/register/', {
        email: userData.email,
        password: userData.password,
        username: userData.username || userData.email.split('@')[0],
        full_name: `${userData.firstName || ''} ${userData.lastName || ''}`.trim(),
        phone: userData.phone || '',
        delivery_address: userData.delivery_address || {}
      });
      
      // Save token (backend returns 'token' not 'access_token')
      if (response.data.token) {
        localStorage.setItem('access_token', response.data.token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Registration failed' };
    }
  },

  // Login customer
  login: async (email, password) => {
    try {
      const response = await apiClient.post('/auth/customer/login/', {
        email,
        password,
      });
      
      // Save token
      if (response.data.token) {
        localStorage.setItem('access_token', response.data.token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Login failed' };
    }
  },

  // Logout customer
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

  // Get current customer profile
  getProfile: async () => {
    try {
      const response = await apiClient.get('/auth/customer/profile/');
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

  // Change customer password
  changePassword: async (oldPassword, newPassword) => {
    try {
      const response = await apiClient.post('/auth/customer/password/change/', {
        old_password: oldPassword,
        new_password: newPassword,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to change password' };
    }
  },

  // Update customer profile
  updateProfile: async (profileData) => {
    try {
      const response = await apiClient.put('/auth/customer/profile/update/', profileData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update profile' };
    }
  },
};

// POS API - Connected to /api/pos/* endpoints (for cashier operations)
export const posAPI = {
  // Scan user QR code
  scanUserQR: async (qrCode) => {
    try {
      const response = await apiClient.post('/pos/scan-user/', {
        qr_code: qrCode,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to scan user QR code' };
    }
  },

  // Scan promotion QR code
  scanPromotionQR: async (qrCode) => {
    try {
      const response = await apiClient.post('/pos/scan-promotion/', {
        qr_code: qrCode,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to scan promotion QR code' };
    }
  },

  // Redeem promotion
  redeemPromotion: async (userQrCode, promotionQrCode, cashierName, orderId = null) => {
    try {
      const response = await apiClient.post('/pos/redeem-promotion/', {
        user_qr_code: userQrCode,
        promotion_qr_code: promotionQrCode,
        cashier_name: cashierName,
        order_id: orderId,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to redeem promotion' };
    }
  },

  // Award points manually
  awardPoints: async (userQrCode, points, description, cashierName) => {
    try {
      const response = await apiClient.post('/pos/award-points/', {
        user_qr_code: userQrCode,
        points: points,
        description: description,
        cashier_name: cashierName,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to award points' };
    }
  },

  // Process order points
  processOrderPoints: async (userQrCode, orderTotal, orderId = null) => {
    try {
      const response = await apiClient.post('/pos/process-order-points/', {
        user_qr_code: userQrCode,
        order_total: orderTotal,
        order_id: orderId,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to process order points' };
    }
  },

  // Get user by QR code
  getUserByQR: async (qrCode) => {
    try {
      const response = await apiClient.get(`/pos/user/${qrCode}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get user' };
    }
  },

  // Get promotion by QR code
  getPromotionByQR: async (qrCode) => {
    try {
      const response = await apiClient.get(`/pos/promotion/${qrCode}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to get promotion' };
    }
  },

  // Get POS dashboard stats
  getDashboard: async () => {
    try {
      const response = await apiClient.get('/pos/dashboard/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch dashboard' };
    }
  },
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
  // Get all orders for current user
  getAll: async () => {
    try {
      const response = await apiClient.get('/online-orders/customer/me/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      // Fallback to localStorage if API fails
      const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
      return { results: orders };
    }
  },

  // Create new order via enhanced online transaction API
  create: async (orderData) => {
    try {
      const response = await apiClient.post('/online-orders/', {
        customer_id: orderData.customerId,
        items: orderData.items,
        delivery_address: orderData.deliveryAddress,
        payment_method: orderData.paymentMethod,
        special_instructions: orderData.specialInstructions,
        payment_reference: orderData.paymentReference,
        points_to_redeem: orderData.pointsToRedeem || 0,
        delivery_type: orderData.deliveryType || 'delivery'
      });
      
      return response.data;
    } catch (error) {
      console.error('Order creation error:', error);
      throw error.response?.data || { message: 'Failed to create order' };
    }
  },

  // Get order by ID using enhanced API
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/online-orders/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch order:', error);
      // Fallback to localStorage
      const orders = JSON.parse(localStorage.getItem('ramyeon_orders') || '[]');
      return orders.find(order => order.id === id) || null;
    }
  },

  // Cancel order using enhanced API
  cancel: async (orderId, reason = 'Customer cancellation') => {
    try {
      const response = await apiClient.post(`/online-orders/${orderId}/cancel/`, {
        reason: reason
      });
      return response.data;
    } catch (error) {
      console.error('Failed to cancel order:', error);
      throw error.response?.data || { message: 'Failed to cancel order' };
    }
  },

  // Get order status
  getStatus: async (orderId) => {
    try {
      const response = await apiClient.get(`/online-orders/${orderId}/`);
      return response.data.status;
    } catch (error) {
      console.error('Failed to get order status:', error);
      return 'unknown';
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
      const response = await apiClient.post('/online-orders/validate-points/', {
        customer_id: customerId,
        points_to_redeem: pointsToRedeem,
        subtotal: subtotal
      });
      return response.data;
    } catch (error) {
      console.error('Error validating points redemption:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate points redemption'
      };
    }
  },

  // Calculate loyalty points earned
  calculatePointsEarned: async (subtotalAfterDiscount) => {
    try {
      const response = await apiClient.post('/online-orders/calculate-points/', {
        subtotal_after_discount: subtotalAfterDiscount
      });
      return response.data;
    } catch (error) {
      console.error('Error calculating loyalty points:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to calculate loyalty points'
      };
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
      const response = await apiClient.post('/online-orders/validate-stock/', {
        items: items
      });
      return response.data;
    } catch (error) {
      console.error('Error validating stock:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to validate stock'
      };
    }
  },

  // Check individual product stock
  checkProductStock: async (productId, quantity) => {
    try {
      const response = await apiClient.post('/online-orders/validate-stock/', {
        items: [{ product_id: productId, quantity: quantity }]
      });
      return response.data;
    } catch (error) {
      console.error('Error checking product stock:', error);
      return {
        success: false,
        error: error.response?.data?.message || error.message || 'Failed to check product stock'
      };
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
    try {
      const response = await apiClient.post('/promotions/validate/', {
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
