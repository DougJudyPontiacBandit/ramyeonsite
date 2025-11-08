# Order Creation Fix Guide

## Problem Summary
Orders are not being saved to the database when customers place orders through the website.

## Root Cause
The error shows a 404 on `POST https://pannag-pos.onrender.com/api/v1/online/orders/` which indicates:
1. Wrong backend URL (should be `pann-pos.onrender.com`, not `pannag-pos.onrender.com`)
2. Missing `/create/` at the end of the URL
3. Browser cache or old compiled code

## ✅ What's Already Fixed
- ✅ Backend endpoint exists at `/api/v1/online/orders/create/`
- ✅ Frontend code correctly calls `/api/v1/online/orders/create/`
- ✅ Frontend has been rebuilt with latest code (November 8, 2025)

## 🔧 Steps to Fix

### Step 1: Verify Backend URL
Check your `.env` file has the correct URL:
```bash
# In ramyeonsite-1/frontend/.env
VITE_API_URL=https://pann-pos.onrender.com/api/v1
VUE_APP_API_URL=https://pann-pos.onrender.com/api/v1
```

**NOT** `pannag-pos.onrender.com`

### Step 2: Clear Browser Cache
1. Open Chrome DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

OR

1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"

### Step 3: Restart Development Server
If you're running the development server:

```bash
# Stop the current server (Ctrl+C)
cd C:\Users\nemen\Documents\USC\2025\IT\Capstone\ramyeonsite-1\frontend
npm run serve
```

### Step 4: If Using Production Build
If you're serving the `dist/` folder:

```bash
# Rebuild (already done)
cd C:\Users\nemen\Documents\USC\2025\IT\Capstone\ramyeonsite-1\frontend
npm run build

# Then serve the dist folder with your web server
```

### Step 5: Verify API Endpoint
Open browser console and check what API URL is being used:

```javascript
// In browser console
localStorage.getItem('ramyeon_orders')
```

Check the network tab for the exact URL being called when you place an order.

## 🧪 Testing

### Test 1: Check API Base URL
1. Open your website
2. Open DevTools Console (F12)
3. You should see: `[API] Resolved base URL: https://pann-pos.onrender.com/api/v1`

### Test 2: Place a Test Order
1. Add items to cart
2. Select "Cash on Delivery" as payment method
3. Fill in delivery address
4. Click "Place Order"
5. Check the Network tab in DevTools
6. The POST request should go to: `https://pann-pos.onrender.com/api/v1/online/orders/create/`
7. Status should be `201 Created` (not 404)

### Test 3: Verify Order in Database
After placing an order, check if it appears in:
1. Order History page (customer view)
2. Backend admin panel
3. MongoDB database (online_transactions collection)

## 🔍 Backend Verification

The backend is correctly configured:
- Endpoint: `/api/v1/online/orders/create/`
- Method: `POST`
- Authentication: Required (JWT token)
- Request Body:
```json
{
  "items": [...],
  "delivery_address": {...},
  "delivery_type": "delivery",
  "payment_method": "cash",
  "points_to_redeem": 0,
  "notes": ""
}
```

## 📊 Expected Behavior
1. Customer places order
2. POST request to `/api/v1/online/orders/create/`
3. Backend saves order to MongoDB `online_transactions` collection
4. Backend returns order ID (e.g., `ONLINE-123456`)
5. Frontend shows success modal
6. Order appears in customer's order history

## ❌ Common Issues

### Issue 1: Still getting 404
- **Cause**: Browser cache
- **Fix**: Hard refresh (Ctrl + F5) or clear cache

### Issue 2: Wrong URL (pannag-pos vs pann-pos)
- **Cause**: Environment variable not loaded
- **Fix**: Restart development server, check .env file

### Issue 3: 401 Unauthorized
- **Cause**: Not logged in or token expired
- **Fix**: Log in again

### Issue 4: 400 Bad Request
- **Cause**: Missing required fields in request
- **Fix**: Check browser console for validation errors

## 📝 Files Modified
- ✅ Frontend rebuilt: `ramyeonsite-1/frontend/dist/` (November 8, 2025 5:51 AM)
- ✅ Backend endpoint verified: `backend/app/kpi_views/online_transaction_views.py`
- ✅ Frontend API client verified: `frontend/src/services/api.js`
- ✅ Order composable verified: `frontend/src/composables/api/useOnlineOrder.js`

## 🆘 Still Not Working?

If orders still don't save after following all steps:

1. **Check Backend Logs**
```bash
# SSH into your Render backend
# Check logs for errors
```

2. **Verify MongoDB Connection**
- Ensure backend can connect to MongoDB
- Check `MONGODB_URI` environment variable

3. **Test Backend Directly**
```bash
# Use Postman or curl to test the endpoint
POST https://pann-pos.onrender.com/api/v1/online/orders/create/
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "items": [{"product_id": "test", "quantity": 1, "price": 100}],
  "delivery_address": {"street": "Test St"},
  "delivery_type": "delivery",
  "payment_method": "cash"
}
```

4. **Contact Support**
- Share browser console errors
- Share network tab request/response
- Share backend logs

## ✨ Quick Fix Summary

```bash
# 1. Clear browser cache (Ctrl + Shift + Delete)
# 2. Restart dev server
cd C:\Users\nemen\Documents\USC\2025\IT\Capstone\ramyeonsite-1\frontend
npm run serve

# 3. Hard refresh browser (Ctrl + F5)
# 4. Try placing an order again
```

---
**Last Updated**: November 8, 2025  
**Status**: ✅ Code Fixed, Awaiting User Testing

