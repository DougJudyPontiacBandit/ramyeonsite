# 📡 Backend API Documentation

Complete API reference for the Ramyeon Corner backend.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Authentication Flow

1. Register or login to get tokens
2. Store the `access_token`
3. Include token in subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```

## API Endpoints

### 🔐 Authentication

#### Register User
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "points": 0
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "points": 3280
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
POST /api/auth/logout/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

#### Get Profile
```http
GET /api/auth/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "points": 3280,
  "address": "123 Main St",
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### Update Profile
```http
PUT /api/auth/profile/update/
PATCH /api/auth/profile/update/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "address": "456 New Street"
}
```

### 📦 Categories

#### List Categories
```http
GET /api/categories/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Noodle",
    "description": "Korean instant noodles",
    "image": "/media/categories/noodle.jpg",
    "is_active": true,
    "products_count": 15,
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

#### Get Category
```http
GET /api/categories/{id}/
```

### 🍜 Products

#### List Products
```http
GET /api/products/
```

**Query Parameters:**
- `category` - Filter by category ID
- `featured` - Filter featured products (true/false)
- `search` - Search by product name

**Examples:**
```http
GET /api/products/?category=1
GET /api/products/?featured=true
GET /api/products/?search=ramen
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Shin Ramyun",
    "description": "Spicy Korean instant noodles",
    "category": 1,
    "category_name": "Noodle",
    "price": "150.00",
    "image": "/media/products/shin_ramyun.jpg",
    "is_available": true,
    "is_featured": true,
    "stock_quantity": 50,
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

#### Get Product
```http
GET /api/products/{id}/
```

### 🛒 Shopping Cart

#### Get Cart
```http
GET /api/cart/my_cart/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Shin Ramyun",
        "price": "150.00"
      },
      "quantity": 2,
      "total_price": "300.00"
    }
  ],
  "total_items": 2,
  "subtotal": "300.00",
  "created_at": "2025-01-15T10:00:00Z"
}
```

#### Add Item to Cart
```http
POST /api/cart/add_item/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response:**
```json
{
  "id": 1,
  "product": {...},
  "quantity": 2,
  "total_price": "300.00"
}
```

#### Update Cart Item
```http
POST /api/cart/update_item/
```

**Request Body:**
```json
{
  "item_id": 1,
  "quantity": 3
}
```

#### Remove Cart Item
```http
POST /api/cart/remove_item/
```

**Request Body:**
```json
{
  "item_id": 1
}
```

#### Clear Cart
```http
POST /api/cart/clear/
```

### 📋 Orders

#### List Orders
```http
GET /api/orders/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "order_number": "ORD-A1B2C3D4",
    "user": 1,
    "status": "pending",
    "delivery_type": "delivery",
    "delivery_address": "123 Main St",
    "payment_method": "cash",
    "subtotal": "300.00",
    "delivery_fee": "50.00",
    "service_fee": "15.00",
    "total_amount": "365.00",
    "items": [...],
    "created_at": "2025-01-15T12:00:00Z"
  }
]
```

#### Create Order
```http
POST /api/orders/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "delivery_type": "delivery",
  "delivery_address": "123 Main St",
  "payment_method": "cash",
  "special_instructions": "Please ring doorbell",
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

#### Get Order
```http
GET /api/orders/{id}/
```

#### Cancel Order
```http
POST /api/orders/{id}/cancel/
```

### 🎟️ Vouchers

#### List Vouchers
```http
GET /api/vouchers/
```

**Response:**
```json
[
  {
    "id": 1,
    "code": "SHIN20",
    "title": "Shin Ramyun Discount",
    "subtitle": "20% OFF",
    "discount_type": "percentage",
    "discount_value": "20.00",
    "min_purchase_amount": "100.00",
    "valid_from": "2025-01-01T00:00:00Z",
    "valid_until": "2025-12-31T23:59:59Z",
    "is_active": true
  }
]
```

#### Claim Voucher
```http
POST /api/vouchers/{id}/claim/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

#### List User Vouchers
```http
GET /api/user-vouchers/
```

#### Get Available Vouchers
```http
GET /api/user-vouchers/available/
```

### 🎉 Promotions

#### List Promotions
```http
GET /api/promotions/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Weekend Special",
    "description": "50% off on all rice cakes",
    "image": "/media/promotions/weekend.jpg",
    "discount_percentage": "50.00",
    "category": 2,
    "category_name": "Rice Cake",
    "valid_from": "2025-01-20T00:00:00Z",
    "valid_until": "2025-01-21T23:59:59Z",
    "is_active": true
  }
]
```

#### Get Promotion
```http
GET /api/promotions/{id}/
```

### 📧 Newsletter

#### Subscribe
```http
POST /api/newsletter/subscribe/
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Successfully subscribed to newsletter"
}
```

### 💬 Contact

#### Submit Message
```http
POST /api/contact/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "I have a question about delivery..."
}
```

**Response:**
```json
{
  "message": "Message sent successfully"
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message description",
  "detail": "Detailed error information"
}
```

## Rate Limiting

Currently, there are no rate limits. This may be added in production.

## CORS

The API accepts requests from:
- http://localhost:8080
- http://127.0.0.1:8080

## Testing with curl

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password2": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### Get Products (with auth)
```bash
curl http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Database Collections

The API works with these MongoDB collections:

- `users` - User accounts
- `categories` - Product categories
- `products` - Menu items
- `vouchers` - Discount coupons
- `user_vouchers` - Claimed vouchers
- `promotions` - Special offers
- `carts` - Shopping carts
- `cart_items` - Cart items
- `orders` - Customer orders
- `order_items` - Order items
- `newsletter_subscriptions` - Newsletter
- `contact_messages` - Contact messages
