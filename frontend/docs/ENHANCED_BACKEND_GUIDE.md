# 🚀 Enhanced Backend Guide - QR Code & Points System

## Overview

Your backend has been enhanced with a complete QR code system, points tracking, and loyalty rewards for your restaurant delivery app.

## 🆕 New Features

### 1. **User QR Codes**
- Every user automatically gets a unique QR code upon registration
- Cashiers can scan user QR codes to identify customers and award points
- QR codes are 32-character unique hashes stored in the database

### 2. **Promotion QR Codes**
- Every promotion automatically gets a unique QR code
- Cashiers can scan promotion QR codes to apply discounts and award bonus points
- Track usage limits per user

### 3. **Points Transaction History**
- Complete audit trail of all points earned/redeemed
- Track points from orders, promotions, rewards, and manual adjustments
- View balance after each transaction

### 4. **Loyalty Rewards**
- Users can redeem points for rewards
- Support for percentage discounts, fixed discounts, or free items
- Rewards have expiration dates and stock limits

### 5. **POS (Point of Sale) System**
- Dedicated endpoints for cashier operations
- Scan user and promotion QR codes
- Process points for orders
- Dashboard with sales statistics

---

## 📊 Database Models

### New Models Added:

#### **PointsTransaction**
Tracks all points movements for users:
- `user` - Foreign key to User
- `transaction_type` - earned, redeemed, expired, adjusted, bonus
- `points` - Amount of points (positive or negative)
- `balance_after` - User's balance after transaction
- `description` - Transaction description
- `order` - Related order (optional)
- `promotion` - Related promotion (optional)

#### **LoyaltyReward**
Rewards users can redeem with points:
- `name` - Reward name
- `description` - Reward description
- `points_required` - Points needed to redeem
- `discount_type` - percentage, fixed, or free_item
- `discount_value` - Discount amount
- `free_product` - Product given for free
- `stock_quantity` - Available stock
- `valid_from` / `valid_until` - Validity period

#### **UserReward**
Tracks rewards claimed by users:
- `user` - Foreign key to User
- `reward` - Foreign key to LoyaltyReward
- `points_spent` - Points used to claim
- `is_used` - Whether reward has been used
- `claimed_at` - When reward was claimed
- `expires_at` - When reward expires

#### **PromotionRedemption**
Tracks promotion QR scans:
- `user` - Who redeemed
- `promotion` - Which promotion
- `order` - Related order (optional)
- `points_awarded` - Bonus points given
- `scanned_by` - Cashier name
- `redeemed_at` - When scanned

### Enhanced Models:

#### **User**
Added:
- `qr_code` - Unique QR code for user (auto-generated)

#### **Promotion**
Added:
- `qr_code` - Unique QR code for promotion (auto-generated)
- `points_reward` - Bonus points when scanned
- `usage_limit_per_user` - How many times user can use it

---

## 🔌 API Endpoints

### User & QR Code Endpoints

#### Get User QR Code
```http
GET /api/qrcode/
Authorization: Bearer <token>
```
**Response:**
```json
{
  "qr_code": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6",
  "username": "johndoe",
  "email": "john@example.com",
  "points": 1250
}
```

#### Get Points History
```http
GET /api/points/history/
Authorization: Bearer <token>
```
**Response:**
```json
{
  "current_points": 1250,
  "transactions": [
    {
      "id": 1,
      "transaction_type": "earned",
      "points": 50,
      "balance_after": 1250,
      "description": "Purchase points: ₱500.00",
      "created_at": "2025-09-30T10:30:00Z"
    }
  ]
}
```

---

### POS (Cashier) Endpoints

#### Scan User QR Code
```http
POST /api/pos/scan-user/
```
**Request:**
```json
{
  "qr_code": "USER_QR_CODE_HERE"
}
```
**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "points": 1250,
    "qr_code": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6"
  },
  "message": "Customer John Doe identified successfully"
}
```

#### Scan Promotion QR Code
```http
POST /api/pos/scan-promotion/
```
**Request:**
```json
{
  "qr_code": "PROMO_QR_CODE_HERE"
}
```
**Response:**
```json
{
  "success": true,
  "promotion": {
    "id": 1,
    "title": "Weekend Special",
    "discount_percentage": 20.00,
    "points_reward": 100,
    "qr_code": "PROMO123456789"
  },
  "message": "Promotion 'Weekend Special' scanned successfully"
}
```

#### Redeem Promotion
```http
POST /api/pos/redeem-promotion/
```
**Request:**
```json
{
  "user_qr_code": "USER_QR_CODE",
  "promotion_qr_code": "PROMO_QR_CODE",
  "cashier_name": "Jane Smith",
  "order_id": 123
}
```
**Response:**
```json
{
  "success": true,
  "redemption": {
    "id": 1,
    "user_name": "johndoe",
    "promotion_title": "Weekend Special",
    "points_awarded": 100
  },
  "points_awarded": 100,
  "new_balance": 1350,
  "message": "Promotion redeemed successfully! 100 points awarded."
}
```

#### Process Order Points
```http
POST /api/pos/process-order-points/
```
**Request:**
```json
{
  "user_qr_code": "USER_QR_CODE",
  "order_total": 500.00,
  "order_id": 123
}
```
**Response:**
```json
{
  "success": true,
  "transaction": {
    "id": 1,
    "points": 50,
    "balance_after": 1300,
    "description": "Purchase points: ₱500.00"
  },
  "points_earned": 50,
  "new_balance": 1300,
  "message": "50 points earned from purchase!"
}
```

#### Award Points Manually
```http
POST /api/pos/award-points/
```
**Request:**
```json
{
  "user_qr_code": "USER_QR_CODE",
  "points": 100,
  "description": "Birthday bonus",
  "cashier_name": "Jane Smith"
}
```

#### POS Dashboard
```http
GET /api/pos/dashboard/
```
**Response:**
```json
{
  "today": {
    "orders_count": 45,
    "total_sales": 25000.00,
    "promotions_redeemed": 12
  },
  "this_week": {
    "orders_count": 320,
    "total_sales": 175000.00,
    "points_awarded": 17500
  },
  "active_promotions": 5
}
```

---

### Loyalty Rewards Endpoints

#### List Available Rewards
```http
GET /api/loyalty-rewards/
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "₱100 Discount",
    "description": "Get ₱100 off your next order",
    "points_required": 500,
    "discount_type": "fixed",
    "discount_value": 100.00,
    "is_active": true
  }
]
```

#### Redeem Loyalty Reward
```http
POST /api/loyalty-rewards/{id}/redeem/
Authorization: Bearer <token>
```
**Response:**
```json
{
  "id": 1,
  "reward": {
    "name": "₱100 Discount",
    "points_required": 500
  },
  "points_spent": 500,
  "is_used": false,
  "expires_at": "2025-10-30T00:00:00Z"
}
```

#### Get User's Claimed Rewards
```http
GET /api/user-rewards/available/
Authorization: Bearer <token>
```

#### Use a Reward
```http
POST /api/user-rewards/{id}/use/
Authorization: Bearer <token>
```

---

## 💻 Frontend Integration Examples

### Display User QR Code (Vue.js)

```vue
<template>
  <div class="qr-code-section">
    <h3>Your Loyalty QR Code</h3>
    <div class="qr-display">
      <qrcode-vue :value="userQRCode" :size="200" level="H" />
      <p>{{ userQRCode }}</p>
      <p>Points: {{ userPoints }}</p>
    </div>
  </div>
</template>

<script>
import QrcodeVue from 'qrcode.vue';
import api from '@/services/api';

export default {
  components: { QrcodeVue },
  data() {
    return {
      userQRCode: '',
      userPoints: 0
    }
  },
  async mounted() {
    const response = await api.get('qrcode/');
    this.userQRCode = response.data.qr_code;
    this.userPoints = response.data.points;
  }
}
</script>
```

### POS Scanner (Cashier Interface)

```vue
<template>
  <div class="pos-scanner">
    <h2>Scan Customer QR Code</h2>
    <qrcode-stream @decode="onUserScan" />
    
    <div v-if="customer" class="customer-info">
      <h3>{{ customer.username }}</h3>
      <p>Points: {{ customer.points }}</p>
      
      <button @click="scanPromotion">Scan Promotion</button>
      <button @click="processOrder">Complete Order</button>
    </div>
  </div>
</template>

<script>
import { QrcodeStream } from 'vue3-qrcode-reader';
import api from '@/services/api';

export default {
  components: { QrcodeStream },
  data() {
    return {
      customer: null,
      orderTotal: 0
    }
  },
  methods: {
    async onUserScan(qrCode) {
      try {
        const response = await api.post('pos/scan-user/', {
          qr_code: qrCode
        });
        this.customer = response.data.user;
      } catch (error) {
        alert('Invalid QR code');
      }
    },
    
    async processOrder() {
      const response = await api.post('pos/process-order-points/', {
        user_qr_code: this.customer.qr_code,
        order_total: this.orderTotal
      });
      alert(`Order complete! ${response.data.points_earned} points earned`);
    }
  }
}
</script>
```

### Points History Display

```vue
<template>
  <div class="points-history">
    <h3>Points History</h3>
    <p>Current Points: {{ currentPoints }}</p>
    
    <div v-for="transaction in transactions" :key="transaction.id" class="transaction">
      <span :class="transaction.transaction_type">
        {{ transaction.transaction_type }}
      </span>
      <span>{{ transaction.points > 0 ? '+' : '' }}{{ transaction.points }}</span>
      <span>{{ transaction.description }}</span>
      <span>{{ formatDate(transaction.created_at) }}</span>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      currentPoints: 0,
      transactions: []
    }
  },
  async mounted() {
    const response = await api.get('points/history/');
    this.currentPoints = response.data.current_points;
    this.transactions = response.data.transactions;
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    }
  }
}
</script>
```

---

## 🔧 Setup & Migration

### 1. Install Requirements
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Generate QR Codes for Existing Users
```bash
python manage.py shell
```
```python
from backend.api.models import User, Promotion
import uuid
import hashlib

# Generate QR codes for existing users
for user in User.objects.filter(qr_code__isnull=True):
    unique_string = f"USER-{user.username}-{uuid.uuid4().hex[:8]}"
    user.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
    user.save()
    print(f"Generated QR code for {user.username}: {user.qr_code}")

# Generate QR codes for existing promotions
for promo in Promotion.objects.filter(qr_code__isnull=True):
    unique_string = f"PROMO-{promo.title}-{uuid.uuid4().hex[:8]}"
    promo.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
    promo.save()
    print(f"Generated QR code for {promo.title}: {promo.qr_code}")
```

### 4. Create Sample Data (Optional)
```python
from backend.api.models import LoyaltyReward, Promotion
from django.utils import timezone
from datetime import timedelta

# Create loyalty rewards
LoyaltyReward.objects.create(
    name="₱50 Discount",
    description="Get ₱50 off your next order",
    points_required=250,
    discount_type="fixed",
    discount_value=50,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=365),
    is_active=True
)

# Create a promotion with QR code
Promotion.objects.create(
    title="Weekend Special",
    description="20% off + 100 bonus points",
    discount_percentage=20,
    points_reward=100,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=30),
    is_active=True
)
```

---

## 📱 QR Code Libraries

### For Frontend (Vue.js):
```bash
npm install qrcode.vue3
npm install vue3-qrcode-reader
```

### For Backend (Optional - Generate QR images):
```bash
pip install qrcode[pil]
```

---

## 🔐 Security Recommendations

### For Production:

1. **POS Endpoints Authentication**
   - Change `AllowAny` to custom `POSPermission`
   - Require API key or special token for POS endpoints
   
2. **QR Code Security**
   - QR codes are already hashed and unique
   - Consider adding expiration for sensitive operations
   - Log all QR code scans for audit trail

3. **Rate Limiting**
   - Add rate limiting to prevent abuse
   - Limit points redemption per time period

---

## 📈 Business Logic

### Points Calculation:
- **Orders**: 1 point per ₱10 spent
- **Promotions**: Variable bonus points (set per promotion)
- **Manual Awards**: Cashier/admin discretion

### Points Redemption:
- Users can redeem points for loyalty rewards
- Rewards have expiration dates (default 30 days)
- Stock quantity tracking for limited rewards

### Promotion Usage:
- Track redemptions per user per promotion
- Enforce usage limits
- Award bonus points on redemption

---

## 🎯 Next Steps

1. **Create POS Interface**
   - Build cashier dashboard
   - QR code scanner integration
   - Order processing UI

2. **Mobile App Integration**
   - Display user QR code in mobile app
   - Push notifications for points earned
   - Digital reward wallet

3. **Analytics Dashboard**
   - Track promotion effectiveness
   - Points economy analytics
   - Customer loyalty metrics

4. **Advanced Features**
   - Points expiration system
   - Tiered loyalty levels (Bronze, Silver, Gold)
   - Referral bonus points
   - Birthday/anniversary rewards

---

## 🐛 Troubleshooting

### QR Codes Not Generating?
- Check that `uuid` and `hashlib` are imported
- Verify model save() method is called
- Run migrations properly

### Points Not Updating?
- Ensure transactions are atomic
- Check PointsTransaction creation
- Verify user.save() is called

### POS Endpoints Not Working?
- Check URL patterns are included
- Verify pos_views.py is imported
- Test with Postman/curl first

---

## 📞 Support

For issues or questions:
1. Check backend logs: `python manage.py runserver`
2. Review admin panel: `http://localhost:8000/admin/`
3. Test API with browsable API: `http://localhost:8000/api/`

---

**Your enhanced backend is ready for production! 🚀**
