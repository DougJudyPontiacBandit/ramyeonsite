# 🔍 Diagnose Order History 404 Error

## Issue Summary
- **Error**: 404 Not Found when fetching `/api/v1/online/orders/history/`
- **Symptom**: Orders don't show in Order History even though they exist in database
- **Order ID Issue**: Shows "ORDER-176070618437" instead of "ONLINE-000060"

---

## Step 1: Check if You're Logged In

Open Browser Console (F12) and run:

```javascript
// Check authentication status
const token = localStorage.getItem('access_token');
console.log('Token exists:', !!token);
console.log('Token value:', token ? token.substring(0, 20) + '...' : 'NO TOKEN');

// Try to decode token (copy to https://jwt.io)
if (token) {
  console.log('Copy this token and paste at https://jwt.io to decode:');
  console.log(token);
}
```

**Expected**: You should see a token. If not, **you need to log in first!**

---

## Step 2: Check Backend is Running

In browser console:

```javascript
// Test if backend is reachable
fetch('https://pann-pos.onrender.com/api/v1/health/')
  .then(r => r.json())
  .then(d => console.log('✅ Backend is running:', d))
  .catch(e => console.error('❌ Backend is DOWN:', e));
```

**Expected**: Should show backend status. If error, **backend is not running!**

---

## Step 3: Check Your Customer ID

In browser console:

```javascript
// Check user profile
fetch('https://pann-pos.onrender.com/api/v1/auth/customer/me/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(d => {
  console.log('✅ Your Profile:', d);
  console.log('Customer ID:', d.customer?.customer_id);
  console.log('Email:', d.customer?.email);
})
.catch(e => console.error('❌ Error:', e));
```

**Expected**: Should show your customer info. If 401 error, **token is expired - log in again!**

---

## Step 4: Manually Test Orders Endpoint

In browser console:

```javascript
// Test orders endpoint directly
fetch('https://pann-pos.onrender.com/api/v1/online/orders/history/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
.then(r => r.json())
.then(d => {
  console.log('✅ Orders Response:', d);
  console.log('Number of orders:', d.total);
  console.log('First order ID:', d.results?.[0]?.order_id);
})
.catch(e => console.error('❌ Error fetching orders:', e));
```

**Expected Results**:
- **Success**: Shows your orders with correct IDs (ONLINE-000001, etc.)
- **401 Unauthorized**: Token expired → Log in again
- **404 Not Found**: Backend endpoint issue
- **403 Forbidden**: Customer ID mismatch

---

## Step 5: Check MongoDB Customer ID Matches

**In Django Shell (Backend Terminal)**:

```python
from backend.app.database import db_manager
import jwt

# Decode your JWT token (replace with your actual token)
token = "YOUR_TOKEN_HERE"
decoded = jwt.decode(token, options={"verify_signature": False})
print("JWT user_id:", decoded.get('user_id'))

# Check MongoDB
db = db_manager.get_database()
customers = list(db.customers.find())
print("\nCustomers in database:")
for c in customers:
    print(f"  - ID: {c['_id']}, Email: {c.get('email')}")

# Check orders
orders = list(db.online_transactions.find())
print(f"\nOrders in database: {len(orders)}")
for o in orders[:5]:
    print(f"  - Order ID: {o['_id']}, Customer ID: {o.get('customer_id')}")
```

**Expected**: JWT `user_id` should match `customer_id` in orders

---

## Common Issues & Solutions

### Issue #1: "No orders found" but they exist in database

**Cause**: JWT token's `user_id` doesn't match order's `customer_id`

**Solution**:
1. Check what `customer_id` is in your orders
2. Check what `user_id` is in your JWT token
3. They must match exactly!

**Fix in Django Shell**:
```python
from backend.app.database import db_manager

db = db_manager.get_database()

# Find your orders (replace with your email)
orders = list(db.online_transactions.find({'customer_email': 'your@email.com'}))
print(f"Found {len(orders)} orders")

# Check customer_id in first order
if orders:
    print("Order customer_id:", orders[0].get('customer_id'))

# Find your customer record
customer = db.customers.find_one({'email': 'your@email.com'})
if customer:
    print("Customer _id:", customer['_id'])
    print("Match:", customer['_id'] == orders[0].get('customer_id'))
```

---

### Issue #2: 404 Error

**Possible Causes**:
1. Backend not running
2. Wrong API URL
3. CORS issue

**Solution**:
```bash
# Check backend is running
curl https://pann-pos.onrender.com/api/v1/health/

# Check orders endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://pann-pos.onrender.com/api/v1/online/orders/history/
```

---

### Issue #3: Wrong Order IDs (ORDER-xxx instead of ONLINE-xxx)

**Cause**: Frontend is using localStorage orders instead of database orders

**Solution**:
1. Clear localStorage orders:
```javascript
localStorage.removeItem('ramyeon_orders');
console.log('Cleared old orders');
```

2. Refresh the page
3. Orders should now come from database with correct IDs

---

## Testing Checklist

Run through these checks:

- [ ] Backend is running and reachable
- [ ] You are logged in (token exists)
- [ ] Token is valid (not expired)
- [ ] JWT token contains `user_id`
- [ ] Customer exists in `customers` collection
- [ ] Customer `_id` matches JWT `user_id`
- [ ] Orders exist in `online_transactions` collection
- [ ] Order `customer_id` matches your `customer._id`
- [ ] API endpoint returns orders (not 404)

---

## Quick Fix Commands

**1. Clear localStorage and reload**:
```javascript
localStorage.clear();
window.location.reload();
// Then log in again
```

**2. Test with curl**:
```bash
# Get auth token first
curl -X POST https://pann-pos.onrender.com/api/v1/auth/customer/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'

# Use token to fetch orders
curl https://pann-pos.onrender.com/api/v1/online/orders/history/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## After Running Diagnostics

**Report back with**:
1. Browser console output from Step 4
2. Whether backend is running (Step 2)
3. Your JWT user_id vs MongoDB customer_id (Step 5)
4. Any error messages

This will help identify the exact issue!

---

## Expected Working Flow

```
1. Customer logs in → Receives JWT token with user_id
2. Token stored in localStorage
3. Customer places order → Backend uses JWT user_id as customer_id
4. Order saved with: customer_id = JWT.user_id
5. Customer opens Order History → Sends JWT token
6. Backend fetches: online_transactions.find({customer_id: JWT.user_id})
7. ✅ Orders appear with correct IDs (ONLINE-000XXX)
```

If any step fails, you'll see 404 or no orders!

