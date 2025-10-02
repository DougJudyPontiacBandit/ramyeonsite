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

// Auth API
export const authAPI = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await apiClient.post('/auth/register/', {
        email: userData.email,
        password: userData.password,
        password2: userData.password,  // Backend expects password confirmation
        username: userData.email.split('@')[0],  // Use email prefix as username
        first_name: userData.firstName,
        last_name: userData.lastName,
        phone: userData.phone,
      });
      
      // Save tokens
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Registration failed' };
    }
  },

  // Login user
  login: async (email, password) => {
    try {
      const response = await apiClient.post('/auth/login/', {
        email,
        password,
      });
      
      // Save tokens
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Login failed' };
    }
  },

  // Logout user
  logout: async () => {
    try {
      await apiClient.post('/auth/logout/');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('ramyeon_user_session');
    } catch (error) {
      // Still clear local storage even if API call fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('ramyeon_user_session');
    }
  },

  // Get user profile
  getProfile: async () => {
    try {
      const response = await apiClient.get('/auth/profile/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch profile' };
    }
  },

  // Update user profile
  updateProfile: async (profileData) => {
    try {
      const response = await apiClient.put('/auth/profile/update/', profileData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to update profile' };
    }
  },
};

// Products API
export const productsAPI = {
  // Get all products
  getAll: async () => {
    try {
      const response = await apiClient.get('/products/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch products' };
    }
  },

  // Get product by ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/products/${id}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch product' };
    }
  },
};

// Categories API
export const categoriesAPI = {
  // Get all categories
  getAll: async () => {
    try {
      const response = await apiClient.get('/categories/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch categories' };
    }
  },
};

// Cart API
export const cartAPI = {
  // Get user cart
  getCart: async () => {
    try {
      const response = await apiClient.get('/cart/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch cart' };
    }
  },

  // Add item to cart
  addItem: async (productId, quantity = 1) => {
    try {
      const response = await apiClient.post('/cart/add_item/', {
        product_id: productId,
        quantity,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to add item to cart' };
    }
  },

  // Remove item from cart
  removeItem: async (itemId) => {
    try {
      const response = await apiClient.post('/cart/remove_item/', {
        item_id: itemId,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to remove item from cart' };
    }
  },

  // Clear cart
  clearCart: async () => {
    try {
      const response = await apiClient.post('/cart/clear/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to clear cart' };
    }
  },
};

// Orders API
export const ordersAPI = {
  // Get all user orders
  getAll: async () => {
    try {
      const response = await apiClient.get('/orders/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch orders' };
    }
  },

  // Create order
  create: async (orderData) => {
    try {
      const response = await apiClient.post('/orders/', orderData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to create order' };
    }
  },

  // Get order by ID
  getById: async (id) => {
    try {
      const response = await apiClient.get(`/orders/${id}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to fetch order' };
    }
  },
};

// Newsletter API
export const newsletterAPI = {
  subscribe: async (email) => {
    try {
      const response = await apiClient.post('/newsletter/subscribe/', { email });
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to subscribe' };
    }
  },
};

// Contact API
export const contactAPI = {
  sendMessage: async (messageData) => {
    try {
      const response = await apiClient.post('/contact/', messageData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { message: 'Failed to send message' };
    }
  },
};

export default apiClient;
