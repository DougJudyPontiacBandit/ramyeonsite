# 🚀 API Quick Reference Card

## Base URL
```
http://localhost:8000/api/
```

---

## 🔐 Authentication

### Register
```bash
POST /api/auth/register/
{
  "username": "user123",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Login
```bash
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Get Profile
```bash
GET /api/auth/profile/
Authorization: Bearer <token>
```

---

## 🎫 User QR Code & Points

### Get My QR Code
```bash
GET /api/qrcode/
Authorization: Bearer <token>

Response: {
  "qr_code": "A1B2C3D4E5F6...",
  "points": 1250
}
```

### Get Points History
```bash
GET /api/points/history/
Authorization: Bearer <token>
```

---

## 🛒 Shopping

### Get Products
```bash
GET /api/products/
GET /api/products/?category=1
GET /api/products/?featured=true
GET /api/products/?search=ramen
```

### Cart Operations
```bash
GET /api/cart/my_cart/

POST /api/cart/add_item/
{
  "product_id": 1,
  "quantity": 2
}

POST /api/cart/update_item/
{
  "item_id": 1,
  "quantity": 3
}

POST /api/cart/remove_item/
{
  "item_id": 1
}

POST /api/cart/clear/
```

### Create Order
```bash
POST /api/orders/
{
  "delivery_type": "delivery",
  "delivery_address": "123 Main St",
  "payment_method": "cash",
  "items": [
    {
      "product": 1,
      "quantity": 2,
      "unit_price": "150.00",
      "total_price": "300.00"
    }
  ]
}
```

---

## 🎉 Promotions & Rewards

### Get Active Promotions
```bash
GET /api/promotions/
```

### Get Loyalty Rewards
```bash
GET /api/loyalty-rewards/
```

### Redeem Reward
```bash
POST /api/loyalty-rewards/{id}/redeem/
Authorization: Bearer <token>
```

### Get My Rewards
```bash
GET /api/user-rewards/available/
Authorization: Bearer <token>
```

---

## 🏪 POS (Cashier) Endpoints

### Scan User QR Code
```bash
POST /api/pos/scan-user/
{
  "qr_code": "USER_QR_CODE"
}
```

### Scan Promotion QR Code
```bash
POST /api/pos/scan-promotion/
{
  "qr_code": "PROMO_QR_CODE"
}
```

### Redeem Promotion
```bash
POST /api/pos/redeem-promotion/
{
  "user_qr_code": "USER_QR",
  "promotion_qr_code": "PROMO_QR",
  "cashier_name": "Jane Smith",
  "order_id": 123
}
```

### Process Order Points
```bash
POST /api/pos/process-order-points/
{
  "user_qr_code": "USER_QR",
  "order_total": 500.00,
  "order_id": 123
}
```

### Award Points Manually
```bash
POST /api/pos/award-points/
{
  "user_qr_code": "USER_QR",
  "points": 100,
  "description": "Birthday bonus",
  "cashier_name": "Jane Smith"
}
```

### POS Dashboard
```bash
GET /api/pos/dashboard/
```

### Quick User Lookup
```bash
GET /api/pos/user/{qr_code}/
```

### Quick Promotion Lookup
```bash
GET /api/pos/promotion/{qr_code}/
```

---

## 📊 Points & Transactions

### Get Points Transactions
```bash
GET /api/points-transactions/
Authorization: Bearer <token>
```

### Get Promotion Redemptions
```bash
GET /api/promotion-redemptions/
Authorization: Bearer <token>
```

---

## 🎟️ Vouchers

### List Vouchers
```bash
GET /api/vouchers/
```

### Claim Voucher
```bash
POST /api/vouchers/{id}/claim/
Authorization: Bearer <token>
```

### My Vouchers
```bash
GET /api/user-vouchers/
GET /api/user-vouchers/available/
Authorization: Bearer <token>
```

---

## 📧 Other Endpoints

### Subscribe Newsletter
```bash
POST /api/newsletter/subscribe/
{
  "email": "user@example.com"
}
```

### Contact Form
```bash
POST /api/contact/
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I have a question..."
}
```

---

## 📝 Response Format

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed information"
}
```

---

## 🔢 Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal server error |

---

## 💡 Common Workflows

### Customer Checkout Flow:
1. User scans their QR code at cashier
2. Cashier scans user QR → `POST /api/pos/scan-user/`
3. Cashier processes order → `POST /api/orders/`
4. System awards points → `POST /api/pos/process-order-points/`
5. If promotion, scan promotion QR → `POST /api/pos/redeem-promotion/`

### Promotion Redemption:
1. Cashier scans promotion QR → `POST /api/pos/scan-promotion/`
2. Cashier scans user QR → `POST /api/pos/scan-user/`
3. Redeem promotion → `POST /api/pos/redeem-promotion/`
4. User gets discount + bonus points

### Points Redemption:
1. User views rewards → `GET /api/loyalty-rewards/`
2. User redeems reward → `POST /api/loyalty-rewards/{id}/redeem/`
3. User views claimed rewards → `GET /api/user-rewards/available/`
4. Cashier marks as used → `POST /api/user-rewards/{id}/use/`

---

## 🧪 Testing with curl

### Test User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!@#",
    "password2": "Test123!@#",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Test QR Code Scan
```bash
curl -X POST http://localhost:8000/api/pos/scan-user/ \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6"
  }'
```

---

## 📱 Frontend Package Recommendations

```bash
# Vue.js QR Code packages
npm install qrcode.vue3          # Display QR codes
npm install vue3-qrcode-reader   # Scan QR codes

# React QR Code packages
npm install react-qr-code        # Display QR codes
npm install react-qr-reader      # Scan QR codes
```

---

**Print this card and keep it handy! 📌**
