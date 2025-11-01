# Troubleshooting: Order Not Showing in History

## Problem

Order `ONLINE-000060` is in the database but:
- ❌ Not showing in Order History
- ❌ Loyalty points not added to profile

## Step-by-Step Fix

### Step 1: Check Your Browser Console

**Open browser DevTools** (Press F12) → Go to **Console** tab

Look for these logs when you visit Order History:

#### ✅ GOOD Signs (Working):
```
📦 OrderHistory component mounted
👤 User profile loaded: CUST-00015 - Points: XX
📦 Loading orders from database...
✅ Fetched orders from database: 1 orders
📊 Sample order: {id: "ONLINE-000060", ...}
```

#### ❌ BAD Signs (Not Working):
```
❌ Not logged in or failed to get profile: [error]
⚠️ No token found, using localStorage fallback
⚠️ Could not fetch from database, falling back to localStorage
```

---

### Step 2: Verify You're Logged In

Run this in browser console:

```javascript
// Check login status
console.log('Token:', localStorage.getItem('access_token') ? 'EXISTS ✅' : 'MISSING ❌');

// Check profile
fetch('https://pann-pos.onrender.com/api/v1/auth/customer/me/', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
})
.then(r => r.json())
.then(data => {
  console.log('Profile:', data);
  console.log('Customer ID:', data.id);
  console.log('Loyalty Points:', data.loyalty_points);
});
```

**Expected output:**
```javascript
{
  id: "CUST-00015",
  email: "customer@gmail.com",
  loyalty_points: 32  // Should show earned points
}
```

**If you see error:** Login again with `customer@gmail.com`

---

### Step 3: Clear Old Cached Data

Run this in browser console:

```javascript
// Clear all old orders from localStorage
localStorage.removeItem('ramyeon_orders');
localStorage.removeItem('ramyeon_pending_order');
Object.keys(localStorage).forEach(key => {
  if (key.startsWith('ramyeon_orders_')) {
    localStorage.removeItem(key);
  }
});

console.log('✅ Cleared old data');

// Reload the page
location.reload();
```

---

### Step 4: Check Database Orders API

Run this in browser console:

```javascript
// Fetch orders from database
fetch('https://pann-pos.onrender.com/api/v1/online/orders/history/', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
})
.then(r => r.json())
.then(data => {
  console.log('📦 Database Response:', data);
  if (data.success && data.results) {
    console.log('✅ Found', data.count, 'orders');
    data.results.forEach(order => {
      console.log(`  - ${order.order_id}: ${order.order_status} - ₱${order.total_amount}`);
    });
  } else {
    console.error('❌ Failed:', data.message);
  }
})
.catch(err => console.error('❌ Error:', err));
```

**Expected output:**
```
✅ Found 1 orders
  - ONLINE-000060: pending - ₱210
```

**If you get 401 Unauthorized:** Your token expired, login again

---

### Step 5: Use the Refresh Button

**New Feature Added:**

1. Go to Order History page
2. Click the **"🔄 Refresh Orders"** button at the top
3. Watch browser console for logs
4. Order should appear

---

### Step 6: Check Loyalty Points in Database

Your order should have earned points. Check if they were awarded:

**Run in browser console:**
```javascript
fetch('https://pann-pos.onrender.com/api/v1/auth/customer/me/', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
})
.then(r => r.json())
.then(data => {
  console.log('Current Points:', data.loyalty_points);
  console.log('Loyalty History:');
  (data.loyalty_history || []).forEach(entry => {
    console.log(`  ${entry.date}: ${entry.points} pts - ${entry.reason}`);
  });
});
```

**Expected:**
```
Current Points: 32
Loyalty History:
  2025-10-31: 32 pts - Earned from order ONLINE-000060
```

**If points are 0:** Backend didn't award points (check backend logs)

---

## Common Issues & Solutions

### Issue 1: Token Expired
**Symptom:** Console shows 401 errors
**Fix:**
1. Logout
2. Login again with `customer@gmail.com`
3. Refresh Order History

### Issue 2: Wrong Customer Account
**Symptom:** Order exists but not showing
**Fix:**
- Order `ONLINE-000060` belongs to `CUST-00015` (`customer@gmail.com`)
- Make sure you're logged in as that customer
- Check: `localStorage.getItem('access_token')` should match this customer

### Issue 3: Old Orders from LocalStorage
**Symptom:** Seeing `ORDER-1760706184377` instead of `ONLINE-000060`
**Fix:**
1. Clear localStorage (Step 3 above)
2. Refresh page
3. Old orders will disappear, new orders from database will show

### Issue 4: Backend Not Running
**Symptom:** Network errors in console
**Fix:**
1. Check if backend is running: https://pann-pos.onrender.com/api/v1/health/
2. If down, start backend server
3. Refresh frontend

### Issue 5: MongoDB Connection Issue
**Symptom:** API returns errors about database
**Fix:**
- Check backend logs for MongoDB connection errors
- Verify MongoDB is running
- Check database credentials

---

## Quick Diagnostic Script

Copy and paste this entire script into browser console:

```javascript
(async function diagnose() {
  console.log('🔍 Running Order History Diagnostics...\n');
  
  // 1. Check Authentication
  const token = localStorage.getItem('access_token');
  console.log('1️⃣ Authentication:', token ? '✅ Token exists' : '❌ No token');
  
  if (!token) {
    console.error('❌ STOP: Please login first!');
    return;
  }
  
  // 2. Check Profile
  try {
    const profileRes = await fetch('https://pann-pos.onrender.com/api/v1/auth/customer/me/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const profile = await profileRes.json();
    
    if (profileRes.ok) {
      console.log('2️⃣ Profile:', `✅ ${profile.id} - ${profile.email}`);
      console.log('   Points:', profile.loyalty_points || 0);
    } else {
      console.error('2️⃣ Profile: ❌ Failed -', profile.message);
      console.log('   Please logout and login again');
      return;
    }
  } catch (err) {
    console.error('2️⃣ Profile: ❌ Error -', err.message);
    return;
  }
  
  // 3. Check Orders API
  try {
    const ordersRes = await fetch('https://pann-pos.onrender.com/api/v1/online/orders/history/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const orders = await ordersRes.json();
    
    if (ordersRes.ok && orders.success) {
      console.log('3️⃣ Orders API:', `✅ Found ${orders.count} orders`);
      if (orders.results && orders.results.length > 0) {
        orders.results.forEach(order => {
          console.log(`   - ${order.order_id}: ${order.order_status} - ₱${order.total_amount} - Points: ${order.loyalty_points_earned || 0}`);
        });
      } else {
        console.log('   ⚠️ No orders found in database for this customer');
      }
    } else {
      console.error('3️⃣ Orders API: ❌ Failed -', orders.message);
    }
  } catch (err) {
    console.error('3️⃣ Orders API: ❌ Error -', err.message);
  }
  
  // 4. Check LocalStorage
  const localOrders = localStorage.getItem('ramyeon_orders');
  if (localOrders) {
    const parsed = JSON.parse(localOrders);
    console.log('4️⃣ LocalStorage:', `⚠️ ${parsed.length} old orders (should be cleared)`);
  } else {
    console.log('4️⃣ LocalStorage: ✅ Clean (no old orders)');
  }
  
  console.log('\n✅ Diagnostic complete!');
})();
```

**Expected Output:**
```
🔍 Running Order History Diagnostics...

1️⃣ Authentication: ✅ Token exists
2️⃣ Profile: ✅ CUST-00015 - customer@gmail.com
   Points: 32
3️⃣ Orders API: ✅ Found 1 orders
   - ONLINE-000060: pending - ₱210 - Points: 32
4️⃣ LocalStorage: ✅ Clean (no old orders)

✅ Diagnostic complete!
```

---

## Still Not Working?

If after all these steps the order still doesn't show:

1. **Check backend logs** for errors
2. **Verify MongoDB** has the order:
   - Collection: `online_transactions`
   - Document ID: `ONLINE-000060`
   - Customer ID: `CUST-00015`

3. **Open** `debug_order_history.html` (created earlier) and run through all checks

4. **Contact support** with:
   - Browser console output
   - Backend logs
   - Diagnostic script output

---

**Last Updated:** October 31, 2025  
**Status:** ✅ Diagnostic tools added - Ready for troubleshooting


