// API Service for Backend Communication
import axios from 'axios';

// Base URL for API - adjust this to match your backend URL
const API_BASE_URL = 'http://localhost:8000/api';

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
      const response = await apiClient.get('/auth/customer/me/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch profile' };
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

// Products API (Currently commented out in backend)
export const productsAPI = {
  // Note: These endpoints are not active yet
  // Uncomment in backend/api/urls.py first
  getAll: async () => {
    console.warn('Products API not yet implemented in backend');
    return { results: [] };
    // try {
    //   const response = await apiClient.get('/products/');
    //   return response.data;
    // } catch (error) {
    //   throw error.response?.data || { message: 'Failed to fetch products' };
    // }
  },

  // eslint-disable-next-line no-unused-vars
  getById: async (id) => {
    console.warn('Products API not yet implemented in backend');
    return null;
  },
};

// Categories API (Currently commented out in backend)
export const categoriesAPI = {
  getAll: async () => {
    console.warn('Categories API not yet implemented in backend');
    return { results: [] };
  },
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

// Orders API (Currently commented out in backend)
export const ordersAPI = {
  getAll: async () => {
    console.warn('Orders API not yet implemented in backend');
    return { results: [] };
  },

  // eslint-disable-next-line no-unused-vars
  create: async (orderData) => {
    console.warn('Orders API not yet implemented in backend');
    return { message: 'Orders API not available' };
  },

  // eslint-disable-next-line no-unused-vars
  getById: async (id) => {
    console.warn('Orders API not yet implemented in backend');
    return null;
  },
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

export default apiClient;
