# Order History Sync Fix

## 🐛 Problem

When a customer placed a new order, it was saved to the database but **did not appear** in the Order History page (`OrderHistory.vue`). The customer had to refresh the page multiple times or the order would never show up.

## 🔍 Root Cause

There was a **mismatch** in how `customer_id` was handled between:

1. **Order Creation** (`CreateOnlineOrderView`):
   - The backend was accepting `customer_id` from the request body sent by the frontend
   - Frontend was sending `customer_id` from `orderData.user.id` which came from `response.customer.customer_id`
   - This created orders with potentially different `customer_id` values

2. **Order Retrieval** (`CustomerOrderHistoryView`):
   - The backend always used `customer_id` from the JWT token (`user_ctx.get('user_id')`)
   - This queries MongoDB: `{'customer_id': customer_id}`

**The Issue**: If `response.customer.customer_id` ≠ JWT token's `user_id`, then:
- Orders were created with one `customer_id`
- But retrieved using a different `customer_id`
- Result: **New orders don't show up!**

## ✅ Solution

### Backend Changes (`backend/app/kpi_views/online_transaction_views.py`)

**1. Force JWT Token Usage for Order Creation**
```python
# BEFORE (Line 21-25)
customer_id = request.data.get('customer_id')
# Fallback to token user id if not provided
if not customer_id:
    user_ctx = getattr(request, 'current_user', None) or {}
    customer_id = user_ctx.get('user_id')

# AFTER (Line 21-24)
# ALWAYS use customer_id from JWT token for consistency
# This ensures orders can be retrieved properly
user_ctx = getattr(request, 'current_user', None) or {}
customer_id = user_ctx.get('user_id')
```

**Why this works**: By **always** using the JWT token's `user_id` for both creating and retrieving orders, we ensure consistency.

**2. Added Debug Logging**
```python
# Order creation logging
logger.info(f"📦 Creating order for customer_id: {customer_id}")
logger.info(f"✅ Order created successfully: {order_id} for customer_id: {customer_id}")

# Order retrieval logging
logger.info(f"📦 Fetching order history for customer_id: {customer_id}")
logger.info(f"✅ Fetched {len(orders)} orders for customer_id: {customer_id} (total in DB: {total_count})")
logger.info(f"📋 Recent order IDs: {order_ids}")
```

### Frontend Changes (`frontend/src/components/OrderHistory.vue`)

**1. Enhanced Debug Logging**
```javascript
console.log('👤 User profile loaded:', {
  id: this.userProfile?.id,
  customer_id: this.userProfile?.customer?.customer_id,
  email: this.userProfile?.email,
  points: this.userProfile?.loyalty_points
});
console.log('🔑 Using JWT token from localStorage');
```

**2. Better Order Loading Feedback**
```javascript
if (this.orders.length > 0) {
  console.log('📊 Most recent order:', {
    id: this.orders[0].id,
    time: this.orders[0].orderTime,
    status: this.orders[0].status,
    items: this.orders[0].items.length
  });
} else {
  console.log('⚠️ No orders found in database');
}
```

## 🧪 Testing Instructions

### Step 1: Clear All Test Data (Fresh Start)
```javascript
// In browser console
localStorage.clear();
// Then log in again
```

### Step 2: Place a New Order
1. Log in as a customer
2. Add items to cart
3. Go to checkout
4. Complete the order (Cash on Delivery is easiest)
5. **Open Browser Console** - Look for these logs:

**Backend logs (terminal):**
```
📦 Creating order for customer_id: <CUSTOMER_ID>
✅ Order created successfully: ONLINE-000001 for customer_id: <CUSTOMER_ID>
```

**Frontend logs (browser console):**
```
✅ Order created successfully
Order ID: ONLINE-000001
```

### Step 3: Navigate to Order History
1. Click on "Order History" in the navigation
2. **Open Browser Console** - Look for these logs:

**Expected Browser Console Output:**
```
📦 OrderHistory component mounted
👤 User profile loaded: {id: "...", customer_id: "...", email: "...", points: ...}
🔑 Using JWT token from localStorage
📦 Loading orders from database...
✅ Fetched orders from database: 1
📊 Most recent order: {id: "ONLINE-000001", time: "...", status: "pending", items: 2}
```

**Expected Backend Terminal Output:**
```
📦 Fetching order history for customer_id: <CUSTOMER_ID>
✅ Fetched 1 orders for customer_id: <CUSTOMER_ID> (total in DB: 1)
📋 Recent order IDs: ['ONLINE-000001']
```

### Step 4: Verify Order Appears
- The order should **immediately appear** in the Order History page
- No refresh needed!
- Order details should be complete (items, prices, status, etc.)

## 🔧 Debugging Tips

### If Orders Still Don't Appear

**1. Check Customer ID Consistency**
```javascript
// In browser console AFTER logging in
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// Decode JWT token (use jwt.io)
// Compare the 'user_id' in the token with database customer_id
```

**2. Check MongoDB Directly**
```python
# In Django shell or Python
from backend.app.database import db_manager
db = db_manager.get_database()

# Check all orders and their customer_id
orders = list(db.online_transactions.find())
for order in orders:
    print(f"Order: {order['_id']}, Customer ID: {order.get('customer_id')}")

# Check customer records
customers = list(db.customers.find())
for customer in customers:
    print(f"Customer ID: {customer['_id']}, Email: {customer.get('email')}")
```

**3. Check JWT Token User ID**
```python
# In Django view or Python with proper imports
from rest_framework_simplejwt.tokens import AccessToken

token_str = "YOUR_ACCESS_TOKEN_HERE"
token = AccessToken(token_str)
print("Token user_id:", token.get('user_id'))
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Order appears in DB but not in UI | Frontend not calling refresh | Check browser console for errors in `ordersAPI.getAll()` |
| 403 Unauthorized | JWT token expired | Log out and log in again |
| Empty order history | Wrong customer_id in JWT | Check JWT token contents match database `customer_id` |
| Orders appear after manual refresh | Component not auto-loading | Check `mounted()` and `activated()` lifecycle hooks |

## 📊 What Changed

### Files Modified

1. **`backend/app/kpi_views/online_transaction_views.py`**
   - Line 21-30: Force JWT token usage for customer_id
   - Line 41-44: Added order creation logging
   - Line 70: Added order fetch logging
   - Line 154-159: Added order retrieval logging

2. **`frontend/src/components/OrderHistory.vue`**
   - Line 208-213: Enhanced user profile logging
   - Line 219: Added JWT token usage log
   - Line 256-265: Improved order loading feedback

### No Breaking Changes
- All existing orders will continue to work
- No database migrations needed
- No API contract changes
- Backward compatible with existing frontend code

## 🚀 Deployment

### Development
```bash
# Backend: No restart needed (if using auto-reload)
# Just save the files

# Frontend: No restart needed (if using hot reload)
# Just save the files
```

### Production
```bash
# Backend
cd backend
python manage.py collectstatic --noinput  # If needed
sudo systemctl restart gunicorn  # Or your process manager

# Frontend
cd frontend
npm run build
# Deploy dist/ folder to your web server
```

## ✅ Success Criteria

After this fix:
1. ✅ New orders immediately appear in Order History
2. ✅ No manual refresh needed
3. ✅ Consistent customer_id between creation and retrieval
4. ✅ Better debugging with enhanced logging
5. ✅ No impact on existing orders

## 📝 Notes

- This fix ensures that the `customer_id` from the JWT token is the **single source of truth**
- Frontend can still send `customer_id` but it will be **ignored** by the backend
- This prevents any mismatch between order creation and retrieval
- The JWT token `user_id` should always match the MongoDB `customers._id` field

## 🔗 Related Issues

- Issue: New orders not showing in Order History
- Related: ORDER_HISTORY_DATABASE_SYNC.md
- Related: ORDER_HISTORY_INTEGRATION_COMPLETE.md

## 📅 Date
**Fixed**: November 1, 2025

