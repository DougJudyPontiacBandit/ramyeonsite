# Backend Setup Guide

## Quick Start

### Step 1: Navigate to Backend Directory

```powershell
cd backend
```

### Step 2: Activate Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**

```cmd
.\venv\Scripts\activate.bat
```

**If you get execution policy error on PowerShell:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install PyJWT (if not already installed)

```powershell
pip install PyJWT
```

### Step 4: Create Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 6: Run Development Server

```powershell
python manage.py runserver
```

The backend will be available at: `http://localhost:8000/`

## Accessing the API

- **API Base URL:** `http://localhost:8000/api/`
- **Admin Panel:** `http://localhost:8000/admin/`
- **API Documentation:** All endpoints are listed in `README.md`

## Environment Configuration

The `.env` file in the backend directory contains all configuration:

```env
SECRET_KEY=django-insecure-ramyeon-corner-secret-key-change-in-production-2025
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
JWT_SECRET_KEY=ramyeon-jwt-secret-key-2025
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:8080
```

## Testing the API

### Test with curl:

```bash
# Health check
curl http://localhost:8000/api/

# Get categories
curl http://localhost:8000/api/categories/

# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"TestPass123!","password2":"TestPass123!","first_name":"Test","last_name":"User"}'
```

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError: No module named 'jwt'

**Solution:**
```powershell
pip install PyJWT
```

### Issue 2: Virtual environment not activated

**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue 3: Database errors

**Solution:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue 4: CORS errors from frontend

**Solution:**
Check that `CORS_ALLOWED_ORIGINS` in `.env` includes your frontend URL (default: `http://localhost:8080`)

## Next Steps

1. ✅ Backend is set up and running
2. ✅ Database is configured
3. ✅ API endpoints are ready
4. 🔄 Create superuser for admin access
5. 🔄 Test API endpoints
6. 🔄 Connect Vue.js frontend

## API Endpoints Overview

### Authentication
- POST `/api/auth/register/` - Register new user
- POST `/api/auth/login/` - Login user
- POST `/api/auth/logout/` - Logout user
- GET `/api/auth/profile/` - Get user profile
- PUT `/api/auth/profile/update/` - Update profile

### Products & Categories
- GET `/api/categories/` - List categories
- GET `/api/products/` - List products
- GET `/api/products/?category=1` - Filter by category
- GET `/api/products/?featured=true` - Get featured products

### Shopping Cart
- GET `/api/cart/my_cart/` - Get user's cart
- POST `/api/cart/add_item/` - Add item to cart
- POST `/api/cart/update_item/` - Update quantity
- POST `/api/cart/remove_item/` - Remove item
- POST `/api/cart/clear/` - Clear cart

### Orders
- GET `/api/orders/` - List user's orders
- POST `/api/orders/` - Create order
- POST `/api/orders/{id}/cancel/` - Cancel order

### Vouchers & Promotions
- GET `/api/vouchers/` - List vouchers
- POST `/api/vouchers/{id}/claim/` - Claim voucher
- GET `/api/promotions/` - List promotions

### Other
- POST `/api/newsletter/subscribe/` - Subscribe to newsletter
- POST `/api/contact/` - Send contact message
