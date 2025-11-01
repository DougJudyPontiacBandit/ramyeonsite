# Order History Database Synchronization

## Overview
This document describes the implementation that ensures order history on the customer website reflects real-time data from the MongoDB database, including order IDs and order status updates made from the POS system.

## What Was Implemented

### 1. Backend Changes

#### Enhanced Order History API (`backend/app/kpi_views/online_transaction_views.py`)
- ✅ **Status History Included**: Added `status_history` to the order history response
- ✅ **Formatted Timestamps**: All timestamps are properly formatted as ISO strings
- ✅ **Complete Order Data**: Returns all order details including:
  - Order ID (from MongoDB `_id` field)
  - Current order status
  - Status history with timestamps
  - Status display information (label, icon, progress, color)
  - Customer details
  - Items ordered
  - Payment information
  - Delivery information

#### Order Status Support (`backend/app/kpi_views/order_status_views.py`)
- ✅ **Multiple Status Names**: Added support for alternative status names:
  - `processing` (alternative to `preparing`)
  - `on_the_way` (alternative to `out_for_delivery`)
- ✅ **Status Display Info**: Enhanced status information with:
  - User-friendly labels
  - Progress percentages
  - Icons for visual feedback
  - Color coding

### 2. Frontend Changes

#### Order History Component (`frontend/src/components/OrderHistory.vue`)
- ✅ **Database-First Loading**: Fetches orders from MongoDB database first
- ✅ **Correct Order ID Display**: Shows the actual MongoDB `_id` (e.g., `ONLINE-000059`)
- ✅ **Real-Time Status**: Displays current order status from database
- ✅ **Status History Mapping**: Maps and passes status history to the tracker
- ✅ **Auto-Refresh**: Automatically refreshes order status every 60 seconds
- ✅ **Fallback Support**: Falls back to localStorage if database is unavailable

#### Order Status Tracker Component (`frontend/src/components/OrderStatusTracker.vue`)
- ✅ **Status History Display**: Shows complete order timeline with timestamps
- ✅ **Progress Bar**: Visual progress indicator based on order status
- ✅ **Alternative Status Names**: Supports both standard and alternative status codes
- ✅ **Auto-Refresh**: Can automatically refresh status at configurable intervals
- ✅ **Manual Refresh**: Provides refresh button for on-demand updates
- ✅ **Status Icons**: Visual indicators for each status stage

## Database Order Structure

### MongoDB Document Example
```json
{
  "_id": "ONLINE-000059",
  "customer_id": "CUST-00015",
  "customer_name": "Customer",
  "customer_email": "customer@gmail.com",
  "order_status": "completed",
  "status": "completed",
  "status_history": [
    {
      "status": "pending",
      "timestamp": "2025-10-30T10:03:44.664Z"
    },
    {
      "status": "processing",
      "timestamp": "2025-10-31T10:40:44.624Z"
    },
    {
      "status": "on_the_way",
      "timestamp": "2025-10-31T10:40:59.630Z"
    },
    {
      "status": "completed",
      "timestamp": "2025-10-31T10:41:25.126Z"
    }
  ],
  "items": [...],
  "subtotal": 195.0,
  "total_amount": 240.0,
  "payment_status": "paid",
  "payment_method": "gcash",
  "delivery_type": "delivery",
  "delivery_address": "Sample St",
  "created_at": "2025-10-30T10:03:44.664Z",
  "updated_at": "2025-10-31T10:41:25.126Z"
}
```

## How It Works

### 1. Order Display Flow
```
Customer Opens Order History
         ↓
Frontend calls: GET /api/v1/online/orders/history/
         ↓
Backend queries: MongoDB online_transactions collection
         ↓
Backend filters by: customer_id (from JWT token)
         ↓
Backend returns: Complete order list with status history
         ↓
Frontend displays: Orders with real order IDs and current status
```

### 2. Status Update Flow (POS → Website)
```
POS Staff updates order status
         ↓
Backend updates: MongoDB online_transactions document
         ↓
Backend adds to: status_history array
         ↓
Customer website: Auto-refreshes every 60 seconds
         ↓
Frontend calls: GET /api/v1/online/orders/{order_id}/status/
         ↓
Frontend displays: Updated status with new progress
```

## Status Codes Supported

| Status Code | Label | Progress | Icon | Color |
|------------|-------|----------|------|-------|
| `pending` | Order Pending | 10% | 🕐 | Yellow |
| `confirmed` | Order Confirmed | 20% | ✅ | Blue |
| `preparing` | Preparing Order | 40% | 📦 | Blue |
| `processing` | Processing Order | 40% | ⚙️ | Blue |
| `cooking` | Cooking | 60% | 👨‍🍳 | Orange |
| `ready` | Ready for Pickup/Delivery | 80% | ✨ | Green |
| `out_for_delivery` | Out for Delivery | 90% | 🚚 | Blue |
| `on_the_way` | On the Way | 90% | 🚚 | Blue |
| `delivered` | Delivered | 95% | 📦 | Green |
| `completed` | Completed | 100% | 🎉 | Green |
| `cancelled` | Cancelled | 0% | ❌ | Red |

## Testing Instructions

### 1. Verify Order ID Display
1. Log in to the customer website as `customer@gmail.com`
2. Navigate to "Order History"
3. **Expected**: Order ID should show as `ONLINE-000059` (from database)
4. **Not**: `ORDER-1760706184377` (timestamp-based localStorage ID)

### 2. Verify Order Status Display
1. Check the order status in Order History
2. **Expected**: Status should match database status (e.g., "Completed" with 100% progress)
3. **Not**: Old cached status (e.g., "Order Confirmed" at 20%)

### 3. Verify Status History
1. Click "View Details" on any order
2. Check the "Order Timeline" section
3. **Expected**: Should show all status changes with timestamps:
   - Order Pending (Oct 30, 2025)
   - Processing Order (Oct 31, 2025)
   - On the Way (Oct 31, 2025)
   - Completed (Oct 31, 2025)

### 4. Verify Real-Time Sync
1. Keep Order History page open
2. From POS system, update an order status
3. **Expected**: Within 60 seconds, the website should show the new status
4. **Alternative**: Click "Refresh Status" button for immediate update

### 5. Test Database Connection
Open browser console and check for logs:
```
✅ Fetched orders from database: 1 orders
📊 Sample order: {id: "ONLINE-000059", status: "completed", ...}
```

If you see:
```
⚠️ No token found, using localStorage fallback
```
This means the user is not logged in or token is expired.

## API Endpoints Used

### Get Order History
```
GET /api/v1/online/orders/history/
Authorization: Bearer {access_token}
Query Parameters:
  - limit: Number of orders to return (default: 50)
  - offset: Pagination offset (default: 0)

Response:
{
  "success": true,
  "count": 1,
  "total": 1,
  "results": [
    {
      "order_id": "ONLINE-000059",
      "order_status": "completed",
      "status_history": [...],
      "status_info": {...},
      ...
    }
  ]
}
```

### Get Order Status
```
GET /api/v1/online/orders/{order_id}/status/
Authorization: Bearer {access_token}

Response:
{
  "success": true,
  "data": {
    "order_id": "ONLINE-000059",
    "current_status": "completed",
    "status_info": {
      "label": "Completed",
      "icon": "🎉",
      "progress": 100,
      "color": "green"
    },
    "status_history": [...]
  }
}
```

### Update Order Status (POS Only)
```
POST /api/v1/online/orders/{order_id}/update-status/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "processing",
  "notes": "Started preparing order"
}

Response:
{
  "success": true,
  "message": "Order status updated successfully",
  "data": {
    "order_id": "ONLINE-000059",
    "new_status": "processing"
  }
}
```

## Authentication Requirements

- **Customer Login**: Required to view order history
- **JWT Token**: Must be stored in localStorage as `access_token`
- **Customer ID**: Extracted from JWT token to filter orders
- **Security**: Orders are filtered by customer_id to ensure customers only see their own orders

## Troubleshooting

### Problem: Orders not showing from database
**Symptoms**: Console shows "No token found" or localStorage fallback
**Solution**:
1. Verify customer is logged in
2. Check localStorage for `access_token`
3. If token exists, verify it's not expired
4. Try logging out and logging back in

### Problem: Order ID shows timestamp format
**Symptoms**: Order ID like `ORDER-1760706184377` instead of `ONLINE-000059`
**Solution**:
1. Orders are coming from localStorage, not database
2. Follow troubleshooting steps above to fix database connection
3. Clear localStorage and refresh page after fixing authentication

### Problem: Status not updating
**Symptoms**: Order status doesn't change after POS update
**Solution**:
1. Wait 60 seconds for auto-refresh
2. Click "Refresh Status" button manually
3. Check browser console for API errors
4. Verify MongoDB connection is working

### Problem: Status history not showing
**Symptoms**: Timeline is empty in order details modal
**Solution**:
1. Verify order has `status_history` array in MongoDB
2. Check if `showHistory` prop is set to `true`
3. Ensure `initialStatusHistory` is being passed to tracker component

## Files Modified

### Backend
- `backend/app/kpi_views/online_transaction_views.py` - Added status_history to response
- `backend/app/kpi_views/order_status_views.py` - Added alternative status codes

### Frontend
- `frontend/src/components/OrderHistory.vue` - Enhanced order mapping and display
- `frontend/src/components/OrderStatusTracker.vue` - Added status history support

## Database Schema

### Collection: `online_transactions`
**Required Fields for Order History:**
- `_id` (string): Order ID (e.g., "ONLINE-000059")
- `customer_id` (string): Customer ID for filtering
- `order_status` (string): Current order status
- `status_history` (array): Array of status change objects
- `created_at` (datetime): Order creation timestamp
- `updated_at` (datetime): Last update timestamp
- `items` (array): Ordered items
- `total_amount` (float): Order total
- `payment_status` (string): Payment status
- `delivery_type` (string): "delivery" or "pickup"

## Performance Considerations

1. **Auto-Refresh Interval**: Set to 60 seconds to balance real-time updates with API load
2. **Pagination**: Order history supports pagination (50 orders per page by default)
3. **Caching**: Status history is cached in component to avoid redundant fetches
4. **Fallback**: localStorage fallback ensures order history works offline

## Future Enhancements

- [ ] WebSocket support for real-time status updates
- [ ] Push notifications when order status changes
- [ ] Order filtering by date range and status
- [ ] Export order history to PDF
- [ ] Order tracking with delivery location

---

**Last Updated**: October 31, 2025  
**Status**: ✅ Implemented and Ready for Testing


