# ⚡ API Quick Start Guide

## 🎯 Quick Import

```javascript
import { authAPI, posAPI } from '@/services/api';
```

---

## 🔑 Authentication Endpoints

### Register New Customer
```javascript
const response = await authAPI.register({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  phone: '+1234567890',
  password: 'SecurePass123'
});
// Returns: { token, customer, message }
```

### Login
```javascript
const response = await authAPI.login('john@example.com', 'SecurePass123');
// Returns: { token, customer, message }
// Token auto-saved to localStorage
```

### Get Current Customer (Requires Auth)
```javascript
const response = await authAPI.getProfile();
// Returns: { customer: {...} }
```

### Change Password (Requires Auth)
```javascript
const response = await authAPI.changePassword('OldPass123', 'NewPass456');
// Returns: { message: '...' }
```

### Logout
```javascript
await authAPI.logout();
// Clears tokens from localStorage
```

---

## 🏪 POS Endpoints (For Cashiers)

### Scan Customer QR
```javascript
const response = await posAPI.scanUserQR('USER-QR-CODE-123');
// Returns: { success: true, user: {...}, message: '...' }
```

### Scan Promotion QR
```javascript
const response = await posAPI.scanPromotionQR('PROMO-QR-CODE-456');
// Returns: { success: true, promotion: {...}, message: '...' }
```

### Redeem Promotion
```javascript
const response = await posAPI.redeemPromotion(
  'USER-QR-CODE',
  'PROMO-QR-CODE',
  'Cashier Name',
  123  // Optional order ID
);
// Returns: { success: true, points_awarded: 100, new_balance: 500, ... }
```

### Award Points
```javascript
const response = await posAPI.awardPoints(
  'USER-QR-CODE',
  100,                // Points to award
  'Birthday bonus',   // Description
  'Cashier Name'
);
// Returns: { success: true, new_balance: 500, ... }
```

### Process Order Points
```javascript
const response = await posAPI.processOrderPoints(
  'USER-QR-CODE',
  500.00,  // Order total amount
  123      // Optional order ID
);
// Returns: { success: true, points_earned: 50, new_balance: 550, ... }
```

---

## 📊 Customer Data Structure

```javascript
{
  _id: "CUST-00001",
  email: "john@example.com",
  username: "john_doe",
  full_name: "John Doe",
  phone: "+1234567890",
  loyalty_points: 1250,
  delivery_address: {
    street: "123 Main St",
    city: "Manila",
    postal_code: "1000"
  },
  status: "active",
  date_created: "2025-10-09T10:30:00Z",
  last_updated: "2025-10-09T10:30:00Z"
}
```

---

## ⚠️ Error Handling Pattern

```javascript
try {
  const response = await authAPI.login(email, password);
  // Handle success
} catch (error) {
  // error.error contains the error message from backend
  console.error(error.error || error.message);
}
```

---

## 🔒 Authentication Flow

1. **User Registers/Logs In**
   ```javascript
   const response = await authAPI.login(email, password);
   ```

2. **Token Auto-Saved**
   ```javascript
   // Automatically saved to localStorage as 'access_token'
   ```

3. **Token Auto-Attached to Requests**
   ```javascript
   // All subsequent API calls include: Authorization: Bearer <token>
   await authAPI.getProfile();  // ✅ Token automatically included
   ```

4. **Session Management**
   ```javascript
   // Save user session
   const customer = response.customer;
   const userSession = {
     id: customer._id,
     email: customer.email,
     points: customer.loyalty_points,
     // ...
   };
   localStorage.setItem('ramyeon_user_session', JSON.stringify(userSession));
   ```

---

## 🌐 Backend URLs

| Endpoint | URL | Auth Required |
|----------|-----|---------------|
| Register | `POST /api/auth/customer/register/` | ❌ |
| Login | `POST /api/auth/customer/login/` | ❌ |
| Get Profile | `GET /api/auth/customer/me/` | ✅ |
| Change Password | `POST /api/auth/customer/password/change/` | ✅ |
| Scan User QR | `POST /api/pos/scan-user/` | ❌ |
| Scan Promotion | `POST /api/pos/scan-promotion/` | ❌ |
| Redeem Promotion | `POST /api/pos/redeem-promotion/` | ❌ |
| Award Points | `POST /api/pos/award-points/` | ❌ |
| Process Order | `POST /api/pos/process-order-points/` | ❌ |
| POS Dashboard | `GET /api/pos/dashboard/` | ❌ |

---

## ✅ Quick Test

**Test in Browser Console:**

```javascript
// 1. Import the API
const { authAPI } = await import('./src/services/api.js');

// 2. Test registration
const response = await authAPI.register({
  firstName: 'Test',
  lastName: 'User',
  email: 'test@example.com',
  phone: '+1234567890',
  password: 'TestPass123'
});
console.log('Registration:', response);

// 3. Test login
const loginResponse = await authAPI.login('test@example.com', 'TestPass123');
console.log('Login:', loginResponse);

// 4. Test get profile (requires auth)
const profile = await authAPI.getProfile();
console.log('Profile:', profile);
```

---

## 🚀 Running the Full Stack

### Terminal 1: Backend
```bash
cd backend
python manage.py runserver
# Running on http://localhost:8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run serve
# Running on http://localhost:8080
```

---

## 📝 Common Use Cases

### Use Case 1: User Sign Up Flow
```vue
<script>
import { authAPI } from '@/services/api';

export default {
  methods: {
    async signUp() {
      try {
        const response = await authAPI.register(this.formData);
        
        // Save session
        const customer = response.customer;
        localStorage.setItem('ramyeon_user_session', JSON.stringify({
          id: customer._id,
          email: customer.email,
          points: customer.loyalty_points
        }));
        
        // Redirect to home
        this.$router.push('/');
      } catch (error) {
        this.errorMessage = error.error || 'Registration failed';
      }
    }
  }
}
</script>
```

### Use Case 2: Protected Profile Page
```vue
<script>
import { authAPI } from '@/services/api';

export default {
  data() {
    return {
      customer: null
    }
  },
  async created() {
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

### Use Case 3: POS Checkout Flow
```vue
<script>
import { posAPI } from '@/services/api';

export default {
  methods: {
    async processCheckout(userQR, orderTotal) {
      try {
        // Process order and award points
        const response = await posAPI.processOrderPoints(userQR, orderTotal);
        
        alert(`Success! ${response.points_earned} points earned!`);
        console.log('New balance:', response.new_balance);
      } catch (error) {
        alert(error.error || 'Checkout failed');
      }
    }
  }
}
</script>
```

---

**Pro Tip:** Check `frontend/docs/API_INTEGRATION_GUIDE.md` for detailed documentation!

