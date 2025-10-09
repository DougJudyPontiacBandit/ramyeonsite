# 🔗 API Integration Guide

## Overview

This guide explains how the frontend is connected to the backend and how to use the API endpoints in your Vue.js components.

## 📋 Table of Contents

1. [Connection Setup](#connection-setup)
2. [Active Endpoints](#active-endpoints)
3. [Using APIs in Components](#using-apis-in-components)
4. [Response Formats](#response-formats)
5. [Error Handling](#error-handling)
6. [Testing the Connection](#testing-the-connection)

---

## 🔌 Connection Setup

### Backend Configuration

**Base URL:** `http://localhost:8000/api`

The backend is configured in `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### CORS Settings

The backend is already configured to accept requests from the frontend:

```python
# In backend/posbackend/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]
```

### JWT Authentication

All authenticated requests automatically include the JWT token:

```javascript
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

---

## ✅ Active Endpoints

### 1. Customer Authentication (`authAPI`)

These endpoints connect to `/api/auth/customer/*` in the backend.

#### **Register**
```javascript
import { authAPI } from '@/services/api';

const response = await authAPI.register({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  phone: '+1234567890',
  password: 'SecurePass123'
});

// Response: { token, customer, message }
```

#### **Login**
```javascript
const response = await authAPI.login('john@example.com', 'SecurePass123');

// Response: { token, customer, message }
// Token is automatically saved to localStorage
```

#### **Get Profile** (Requires Authentication)
```javascript
const response = await authAPI.getProfile();

// Response: { customer: { _id, email, username, full_name, phone, loyalty_points, ... } }
```

#### **Change Password** (Requires Authentication)
```javascript
const response = await authAPI.changePassword('OldPass123', 'NewPass456');

// Response: { message: 'Password changed successfully' }
```

#### **Logout**
```javascript
await authAPI.logout();
// Clears all tokens from localStorage
```

---

### 2. Point of Sale (`posAPI`)

These endpoints connect to `/api/pos/*` in the backend (for cashier operations).

#### **Scan User QR Code**
```javascript
import { posAPI } from '@/services/api';

const response = await posAPI.scanUserQR('USER-QR-CODE-123');

// Response: { success: true, user: {...}, message: '...' }
```

#### **Scan Promotion QR Code**
```javascript
const response = await posAPI.scanPromotionQR('PROMO-QR-CODE-456');

// Response: { success: true, promotion: {...}, message: '...' }
```

#### **Redeem Promotion**
```javascript
const response = await posAPI.redeemPromotion(
  'USER-QR-CODE-123',
  'PROMO-QR-CODE-456',
  'Cashier Name',
  123 // Optional order ID
);

// Response: { success: true, redemption: {...}, points_awarded: 100, new_balance: 500, message: '...' }
```

#### **Award Points Manually**
```javascript
const response = await posAPI.awardPoints(
  'USER-QR-CODE-123',
  100,
  'Birthday bonus',
  'Cashier Name'
);

// Response: { success: true, transaction: {...}, new_balance: 500, message: '...' }
```

#### **Process Order Points**
```javascript
const response = await posAPI.processOrderPoints(
  'USER-QR-CODE-123',
  500.00,  // Order total
  123      // Optional order ID
);

// Response: { success: true, transaction: {...}, points_earned: 50, new_balance: 550, message: '...' }
```

#### **Get POS Dashboard**
```javascript
const response = await posAPI.getDashboard();

// Response: { today: {...}, this_week: {...}, active_promotions: 5 }
```

---

### 3. Placeholder APIs (Not Yet Implemented)

These APIs are available in the frontend but not yet connected to the backend:

- `productsAPI` - Product management
- `categoriesAPI` - Category management  
- `cartAPI` - Shopping cart operations
- `ordersAPI` - Order management
- `newsletterAPI` - Newsletter subscriptions
- `contactAPI` - Contact form

They currently show console warnings when called. To activate them, uncomment the corresponding routes in `backend/api/urls.py`.

---

## 💻 Using APIs in Components

### Example: Login Component

```vue
<script>
import { authAPI } from '@/services/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const response = await authAPI.login(this.email, this.password);
        
        // Create user session
        const customer = response.customer;
        const userSession = {
          id: customer._id,
          email: customer.email,
          username: customer.username,
          points: customer.loyalty_points,
          // ... other fields
        };
        
        // Save to localStorage
        localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));
        
        // Redirect or emit event
        this.$emit('loginSuccess', userSession);
        
      } catch (error) {
        this.errorMessage = error.error || error.message || 'Login failed';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>
```

### Example: Protected Route/Component

```vue
<script>
import { authAPI } from '@/services/api';

export default {
  data() {
    return {
      customer: null
    }
  },
  async mounted() {
    try {
      const response = await authAPI.getProfile();
      this.customer = response.customer;
    } catch (error) {
      // Not authenticated, redirect to login
      this.$router.push('/login');
    }
  }
}
</script>
```

### Example: POS Scanner Component

```vue
<script>
import { posAPI } from '@/services/api';

export default {
  methods: {
    async scanQRCode(qrCode) {
      try {
        const response = await posAPI.scanUserQR(qrCode);
        console.log('User found:', response.user);
        // Display user info
      } catch (error) {
        alert(error.error || 'Invalid QR code');
      }
    }
  }
}
</script>
```

---

## 📦 Response Formats

### Customer Authentication Response

**Login/Register:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "customer": {
    "_id": "CUST-00001",
    "email": "john@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "loyalty_points": 0,
    "delivery_address": {},
    "status": "active",
    "date_created": "2025-10-09T10:30:00Z",
    "last_updated": "2025-10-09T10:30:00Z"
  },
  "message": "Login successful"
}
```

**Get Profile:**
```json
{
  "customer": {
    "_id": "CUST-00001",
    "email": "john@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "loyalty_points": 1250,
    "delivery_address": {
      "street": "123 Main St",
      "city": "Manila",
      "postal_code": "1000"
    },
    "status": "active"
  }
}
```

### POS Response

**Scan User QR:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "points": 1250,
    "qr_code": "USER-QR-123"
  },
  "message": "Customer John Doe identified successfully"
}
```

**Process Order Points:**
```json
{
  "success": true,
  "transaction": {
    "id": 123,
    "transaction_type": "earned",
    "points": 50,
    "balance_after": 1300,
    "description": "Purchase points: ₱500.00"
  },
  "points_earned": 50,
  "new_balance": 1300,
  "message": "50 points earned from purchase!"
}
```

---

## ⚠️ Error Handling

### Error Response Format

```json
{
  "error": "Email already exists"
}
```

### Handling Errors in Components

```javascript
try {
  const response = await authAPI.login(email, password);
  // Handle success
} catch (error) {
  // error is the parsed error response from backend
  if (error.error) {
    this.errorMessage = error.error;
  } else if (error.message) {
    this.errorMessage = error.message;
  } else {
    this.errorMessage = 'An unexpected error occurred';
  }
}
```

### Common Error Cases

1. **Authentication Required (401)**
   - Token missing or expired
   - Redirect user to login

2. **Validation Error (400)**
   - Invalid email format
   - Password too short
   - Missing required fields

3. **Not Found (404)**
   - Invalid QR code
   - User/promotion not found

4. **Server Error (500)**
   - Database connection issue
   - Unexpected backend error

---

## 🧪 Testing the Connection

### Step 1: Start the Backend

```bash
cd backend
python manage.py runserver
```

Backend should be running on `http://localhost:8000`

### Step 2: Start the Frontend

```bash
cd frontend
npm run serve
```

Frontend should be running on `http://localhost:8080`

### Step 3: Test Registration

1. Open browser to `http://localhost:8080`
2. Navigate to Sign Up
3. Fill in the form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Phone: +1234567890
   - Password: SecurePass123
4. Click "Create Account"
5. Check browser console for any errors
6. Check browser's localStorage for `access_token` and `ramyeon_user_session`

### Step 4: Test Login

1. Navigate to Login
2. Enter credentials:
   - Email: john@example.com
   - Password: SecurePass123
3. Click "Sign in"
4. Should receive success message and be logged in

### Step 5: Test Authenticated Request

1. After logging in, open browser DevTools > Console
2. Run:
```javascript
import { authAPI } from './services/api';
const profile = await authAPI.getProfile();
console.log(profile);
```

### Step 6: Check Backend Logs

Monitor the terminal where the backend is running for:
```
POST /api/auth/customer/register/ - 201 Created
POST /api/auth/customer/login/ - 200 OK
GET /api/auth/customer/me/ - 200 OK
```

---

## 🔐 Security Notes

1. **JWT Token Storage**
   - Tokens are stored in `localStorage` as `access_token`
   - Automatically included in all authenticated requests

2. **Password Security**
   - Passwords are hashed with bcrypt in the backend
   - Never stored in plain text
   - Never sent back to frontend

3. **HTTPS in Production**
   - Use HTTPS in production
   - Update `API_BASE_URL` to your production URL
   - Configure CORS properly for production domain

---

## 🚀 Next Steps

### To Enable Products, Cart, and Orders APIs:

1. **Uncomment routes in backend:**
   - Edit `backend/api/urls.py`
   - Uncomment the router.register lines for products, cart, orders

2. **Update frontend API calls:**
   - Edit `frontend/src/services/api.js`
   - Uncomment the actual API calls in productsAPI, cartAPI, ordersAPI

3. **Test the new endpoints:**
   - Follow the testing steps above

---

## 📞 Need Help?

- Backend API routes: `backend/api/urls.py`
- Frontend API service: `frontend/src/services/api.js`
- Example usage: `frontend/src/components/Login.vue` and `SignUp.vue`

---

**Last Updated:** October 9, 2025

