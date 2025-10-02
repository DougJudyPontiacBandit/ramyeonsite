# 🎨 Frontend Integration Guide

Guide for integrating the Vue.js frontend with the Django backend API.

## Overview

This guide shows you how to connect your Vue.js frontend to the Django REST API backend using Axios and JWT authentication.

## Setup

### 1. Install Axios

```bash
npm install axios
```

### 2. Create API Service

Create a new file `src/services/api.js`:

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token expired, redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default {
  // Authentication
  async register(userData) {
    const response = await api.post('auth/register/', userData);
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('ramyeon_user_session', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async login(email, password) {
    const response = await api.post('auth/login/', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      localStorage.setItem('ramyeon_user_session', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  async logout() {
    try {
      await api.post('auth/logout/');
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('ramyeon_user_session');
    }
  },

  async getProfile() {
    const response = await api.get('auth/profile/');
    return response.data;
  },

  async updateProfile(profileData) {
    const response = await api.put('auth/profile/update/', profileData);
    return response.data;
  },

  // Categories
  async getCategories() {
    const response = await api.get('categories/');
    return response.data;
  },

  // Products
  async getProducts(params = {}) {
    const response = await api.get('products/', { params });
    return response.data;
  },

  async getProduct(id) {
    const response = await api.get(`products/${id}/`);
    return response.data;
  },

  // Cart
  async getCart() {
    const response = await api.get('cart/my_cart/');
    return response.data;
  },

  async addToCart(productId, quantity = 1) {
    const response = await api.post('cart/add_item/', {
      product_id: productId,
      quantity,
    });
    return response.data;
  },

  async updateCartItem(itemId, quantity) {
    const response = await api.post('cart/update_item/', {
      item_id: itemId,
      quantity,
    });
    return response.data;
  },

  async removeCartItem(itemId) {
    const response = await api.post('cart/remove_item/', { item_id: itemId });
    return response.data;
  },

  async clearCart() {
    const response = await api.post('cart/clear/');
    return response.data;
  },

  // Orders
  async getOrders() {
    const response = await api.get('orders/');
    return response.data;
  },

  async createOrder(orderData) {
    const response = await api.post('orders/', orderData);
    return response.data;
  },

  async getOrder(id) {
    const response = await api.get(`orders/${id}/`);
    return response.data;
  },

  async cancelOrder(id) {
    const response = await api.post(`orders/${id}/cancel/`);
    return response.data;
  },

  // Vouchers
  async getVouchers() {
    const response = await api.get('vouchers/');
    return response.data;
  },

  async claimVoucher(id) {
    const response = await api.post(`vouchers/${id}/claim/`);
    return response.data;
  },

  async getUserVouchers() {
    const response = await api.get('user-vouchers/');
    return response.data;
  },

  async getAvailableVouchers() {
    const response = await api.get('user-vouchers/available/');
    return response.data;
  },

  // Promotions
  async getPromotions() {
    const response = await api.get('promotions/');
    return response.data;
  },

  async getPromotion(id) {
    const response = await api.get(`promotions/${id}/`);
    return response.data;
  },

  // Newsletter
  async subscribeNewsletter(email) {
    const response = await api.post('newsletter/subscribe/', { email });
    return response.data;
  },

  // Contact
  async sendContactMessage(messageData) {
    const response = await api.post('contact/', messageData);
    return response.data;
  },
};
```

## Update Components

### Login Component

Update `src/components/Login.vue`:

```vue
<script>
import api from '@/services/api';

export default {
  data() {
    return {
      formData: {
        email: '',
        password: '',
        rememberMe: false
      },
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = '';

      try {
        const data = await api.login(this.formData.email, this.formData.password);
        
        this.successMessage = 'Login successful! Redirecting...';
        
        if (this.formData.rememberMe) {
          localStorage.setItem('ramyeon_remember_user', this.formData.email);
        }

        setTimeout(() => {
          this.$emit('loginSuccess', data.user);
        }, 1000);

      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>
```

### SignUp Component

Update `src/components/SignUp.vue`:

```vue
<script>
import api from '@/services/api';

export default {
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        password2: '',
        firstName: '',
        lastName: '',
        phone: ''
      },
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async handleSignUp() {
      if (this.formData.password !== this.formData.password2) {
        this.errorMessage = 'Passwords do not match';
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';

      try {
        const userData = {
          username: this.formData.username,
          email: this.formData.email,
          password: this.formData.password,
          password2: this.formData.password2,
          first_name: this.formData.firstName,
          last_name: this.formData.lastName,
          phone: this.formData.phone
        };

        const data = await api.register(userData);
        
        this.successMessage = 'Registration successful! Redirecting...';
        
        setTimeout(() => {
          this.$emit('signUpSuccess', data.user);
        }, 1000);

      } catch (error) {
        console.error('SignUp error:', error);
        this.errorMessage = error.response?.data?.error || 'Registration failed. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>
```

### Menu Component

Update `src/components/Menu.vue`:

```vue
<script>
import api from '@/services/api';

export default {
  data() {
    return {
      categories: [],
      products: [],
      selectedCategory: null,
      isLoading: false
    }
  },
  async mounted() {
    await this.loadCategories();
    await this.loadProducts();
  },
  methods: {
    async loadCategories() {
      try {
        this.categories = await api.getCategories();
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    },

    async loadProducts() {
      this.isLoading = true;
      try {
        const params = this.selectedCategory ? { category: this.selectedCategory } : {};
        this.products = await api.getProducts(params);
      } catch (error) {
        console.error('Error loading products:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async addToCart(product) {
      try {
        await api.addToCart(product.id, 1);
        this.$emit('addToCart', product);
        // Show success message
        alert(`${product.name} added to cart!`);
      } catch (error) {
        console.error('Error adding to cart:', error);
        alert('Please login to add items to cart');
      }
    },

    filterByCategory(categoryId) {
      this.selectedCategory = categoryId;
      this.loadProducts();
    }
  }
}
</script>
```

### Cart Component

Update `src/components/Cart.vue`:

```vue
<script>
import api from '@/services/api';

export default {
  data() {
    return {
      cart: null,
      isLoading: false
    }
  },
  async mounted() {
    await this.loadCart();
  },
  computed: {
    subtotal() {
      return this.cart?.subtotal || 0;
    },
    deliveryFee() {
      return 50; // Fixed delivery fee
    },
    total() {
      return parseFloat(this.subtotal) + this.deliveryFee;
    }
  },
  methods: {
    async loadCart() {
      this.isLoading = true;
      try {
        this.cart = await api.getCart();
      } catch (error) {
        console.error('Error loading cart:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async updateQuantity(item, newQuantity) {
      try {
        await api.updateCartItem(item.id, newQuantity);
        await this.loadCart();
      } catch (error) {
        console.error('Error updating cart:', error);
      }
    },

    async removeItem(item) {
      try {
        await api.removeCartItem(item.id);
        await this.loadCart();
      } catch (error) {
        console.error('Error removing item:', error);
      }
    },

    async checkout() {
      try {
        const orderData = {
          delivery_type: 'delivery',
          delivery_address: this.deliveryAddress,
          payment_method: 'cash',
          items: this.cart.items.map(item => ({
            product: item.product.id,
            quantity: item.quantity,
            unit_price: item.product.price,
            total_price: item.total_price
          }))
        };

        const order = await api.createOrder(orderData);
        alert(`Order placed successfully! Order number: ${order.order_number}`);
        this.$router.push('/orders');
      } catch (error) {
        console.error('Checkout error:', error);
        alert('Checkout failed. Please try again.');
      }
    }
  }
}
</script>
```

## App.vue Updates

Update the main `App.vue` to use API:

```vue
<script>
import api from '@/services/api';

export default {
  methods: {
    async handleLogout() {
      try {
        await api.logout();
        this.currentUser = null;
        this.setCurrentPage('Home');
      } catch (error) {
        console.error('Logout error:', error);
      }
    },

    async checkUserSession() {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const user = await api.getProfile();
          this.currentUser = user;
        } catch (error) {
          // Token invalid, clear storage
          localStorage.removeItem('access_token');
          localStorage.removeItem('ramyeon_user_session');
        }
      }
    }
  }
}
</script>
```

## Environment Configuration

Create `.env` in root:

```env
VUE_APP_API_URL=http://localhost:8000/api/
```

Update `api.js`:

```javascript
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/';
```

## Testing

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run serve`
3. Test registration and login
4. Browse products from API
5. Add items to cart via API
6. Create orders through API

## Common Issues

### CORS Errors
- Ensure backend CORS settings include frontend URL
- Check `CORS_ALLOWED_ORIGINS` in backend `.env`

### 401 Unauthorized
- Token expired or invalid
- Check token in localStorage
- Re-login to get new token

### Network Errors
- Backend not running
- Wrong API URL
- Firewall blocking requests

## Next Steps

1. Replace all localStorage usage with API calls
2. Add error handling and loading states
3. Implement token refresh logic
4. Add request/response interceptors
5. Create reusable composables for API calls
