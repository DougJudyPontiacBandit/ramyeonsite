import axios from 'axios'
// import mockAuth from './mockAuth.js'

// Configure axios defaults
const DEFAULT_API_BASE = 'http://localhost:8000/api/v1'
const ENV_API_BASE = (typeof process !== 'undefined' && process.env && process.env.VUE_APP_API_BASE_URL) || DEFAULT_API_BASE
axios.defaults.baseURL = ENV_API_BASE
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Check if backend is available
// let useMockAuth = false
// const checkBackendAvailability = async () => {
//   try {
//     await axios.get('/health/', { timeout: 2000 })
//     return true
//   } catch (error) {
//     console.warn('Backend not available, using mock authentication')
//     return false
//   }
// }

// Initialize backend check
// checkBackendAvailability().then(available => {
//   useMockAuth = !available
// })

// Add request interceptor for authentication
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('auth_token')
      localStorage.removeItem('ramyeon_user_session')
      // Redirect to login if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default axios

// API endpoints
export const api = {
  // Authentication
  auth: {
    login: async (credentials) => {
      // if (useMockAuth) {
      //   return await mockAuth.login(credentials)
      // }
      return axios.post('/auth/login/', credentials)
    },
    logout: async () => {
      // if (useMockAuth) {
      //   return await mockAuth.logout()
      // }
      return axios.post('/auth/logout/')
    },
    refreshToken: (token) => axios.post('/auth/refresh/', { refresh: token }),
    currentUser: async () => {
      // if (useMockAuth) {
      //   const token = localStorage.getItem('auth_token')
      //   if (!token) {
      //     throw new Error('No token found')
      //   }
      //   return await mockAuth.getCurrentUser(token)
      // }
      return axios.get('/auth/me/')
    },
    verifyToken: (token) => axios.post('/auth/verify-token/', { token }),
    register: async (data) => {
      // if (useMockAuth) {
      //   return await mockAuth.register(data)
      // }
      return axios.post('/auth/register/', data)
    }
  },

  // Products
  products: {
    list: (params) => axios.get('/products/', { params }),
    get: (id) => axios.get(`/products/${id}/`),
    create: (data) => axios.post('/products/', data),
    update: (id, data) => axios.put(`/products/${id}/`, data),
    delete: (id) => axios.delete(`/products/${id}/`),
    bySku: (sku) => axios.get(`/products/sku/${sku}/`),
    byCategory: (categoryId) => axios.get(`/products/reports/by-category/${categoryId}/`),
    lowStock: () => axios.get('/products/reports/low-stock/'),
    expiring: () => axios.get('/products/reports/expiring/')
  },

  // Categories
  categories: {
    list: () => axios.get('/category/'),
    get: (id) => axios.get(`/category/${id}/`),
    create: (data) => axios.post('/category/', data),
    update: (id, data) => axios.put(`/category/${id}/`, data),
    delete: (id) => axios.delete(`/category/${id}/`),
    subcategories: (id) => axios.get(`/category/${id}/subcategories/`),
    products: (categoryId, subcategoryName) => axios.get(`/category/${categoryId}/subcategories/${subcategoryName}/products/`)
  },

  // Users
  users: {
    list: () => axios.get('/users/'),
    get: (id) => axios.get(`/users/${id}/`),
    create: (data) => axios.post('/users/', data),
    update: (id, data) => axios.put(`/users/${id}/`, data),
    delete: (id) => axios.delete(`/users/${id}/`)
  },

  // Customers
  customers: {
    list: () => axios.get('/customers/'),
    get: (id) => axios.get(`/customers/${id}/`),
    create: (data) => axios.post('/customers/', data),
    update: (id, data) => axios.put(`/customers/${id}/`, data),
    delete: (id) => axios.delete(`/customers/${id}/`),
    qr: (id) => axios.get(`/customers/${id}/qr/`),
    qrScan: (qrCode) => axios.post('/customers/qr/scan/', { qr_code: qrCode })
  },

  // Sales/Invoices
  sales: {
    list: () => axios.get('/invoices/'),
    mine: () => axios.get('/invoices/my/'),
    get: (id) => axios.get(`/invoices/${id}/`),
    create: (data) => axios.post('/invoices/', data),
    update: (id, data) => axios.put(`/invoices/${id}/`, data),
    delete: (id) => axios.delete(`/invoices/${id}/`),
    stats: () => axios.get('/invoices/stats/')
  },

  // Promotions
  promotions: {
    list: () => axios.get('/promotions/'),
    get: (id) => axios.get(`/promotions/${id}/`),
    create: (data) => axios.post('/promotions/', data),
    update: (id, data) => axios.put(`/promotions/${id}/`, data),
    delete: (id) => axios.delete(`/promotions/${id}/`),
    active: () => axios.get('/promotions/active/'),
    apply: (data) => axios.post('/promotions/apply/', data),
    qr: (id) => axios.get(`/promotions/${id}/qr/`),
    qrScan: (qrCode) => axios.post('/promotions/qr/scan/', { qr_code: qrCode })
  },

  // POS operations
  pos: {
    catalog: () => axios.get('/pos/catalog/'),
    search: (query) => axios.get('/pos/search/', { params: { q: query } }),
    barcode: (barcode) => axios.get(`/pos/barcode/${barcode}/`),
    stockCheck: (products) => axios.post('/pos/stock-check/', { products }),
    lowStock: () => axios.get('/pos/low-stock/')
  },

  // Cart operations
  cart: {
    get: () => axios.get('/cart/'),
    addItem: (productId, quantity, price, productName) => axios.post('/cart/items/', { product_id: productId, quantity, price, product_name: productName }),
    updateItem: (productId, quantity) => axios.put('/cart/items/', { product_id: productId, quantity }),
    removeItem: (productId) => axios.delete(`/cart/items/?product_id=${productId}`),
    checkout: (promotionName = null) => axios.post('/cart/checkout/', { promotion_name: promotionName })
  }
}
