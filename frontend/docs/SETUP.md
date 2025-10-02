# 🚀 Complete Setup Guide - Ramyeon Corner

This guide will walk you through setting up both the frontend and backend of the Ramyeon Corner application.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [MongoDB Atlas Configuration](#mongodb-atlas-configuration)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## ✅ Prerequisites

### For Frontend
- **Node.js** (version 14 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**

### For Backend
- **Python** 3.8+ - [Download](https://www.python.org/)
- **pip** (comes with Python)
- **Virtual environment** (venv)

### Database
- **MongoDB Atlas** account (free tier available)
- Internet connection for cloud database

## 🎨 Frontend Setup

### 1. Navigate to Project Root

```bash
cd ramyeonsite
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- Vue.js 3
- Tailwind CSS
- QR code library
- All other dependencies

### 3. Start Development Server

```bash
npm run serve
```

The frontend will be available at: **http://localhost:8080**

### 4. Build for Production (Optional)

```bash
npm run build
```

This creates optimized files in the `dist/` folder.

## 🔧 Backend Setup

### Step 1: Navigate to Backend Directory

```bash
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

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install djongo==1.3.6
pip install PyJWT
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Your `.env` file is already configured with MongoDB Atlas:

```env
MONGODB_URI=mongodb+srv://admin:***@cluster0.qumhbyz.mongodb.net/pos_system
MONGODB_DATABASE=pos_system
SECRET_KEY=django-insecure-ramyeon-corner-secret-key-change-in-production-2025
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

✅ **This is already set up!** No changes needed.

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the MongoDB collections.

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username
- Email
- Password

### Step 7: Start Development Server

```bash
python manage.py runserver
```

The backend API will be available at: **http://localhost:8000/api/**

## 🗄️ MongoDB Atlas Configuration

### Your Current Setup

- **Cluster:** cluster0.qumhbyz.mongodb.net
- **Database:** pos_system
- **Connection:** Already configured in `.env`

### Access MongoDB Atlas Dashboard

1. Go to https://cloud.mongodb.com
2. Login with your MongoDB Atlas account
3. Select your cluster (cluster0)
4. Browse collections under the `pos_system` database

### Collections Created

After running migrations, you'll have these collections:

1. `users` - User accounts
2. `categories` - Product categories
3. `products` - Menu items
4. `vouchers` - Discount coupons
5. `user_vouchers` - Claimed vouchers
6. `promotions` - Special offers
7. `carts` - Shopping carts
8. `cart_items` - Cart items
9. `orders` - Customer orders
10. `order_items` - Order items
11. `newsletter_subscriptions` - Newsletter
12. `contact_messages` - Contact messages

## 🎯 Running the Application

### Start Both Frontend and Backend

**Terminal 1 - Frontend:**
```bash
npm run serve
```

**Terminal 2 - Backend:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Access the Application

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/

## 🧪 Testing the Setup

### Test Frontend

1. Open http://localhost:8080
2. You should see the Ramyeon Corner homepage
3. Try clicking through the menu and pages

### Test Backend API

**Using Browser:**
- Visit http://localhost:8000/api/
- You should see the API root

**Using curl (PowerShell):**
```powershell
# Get all products
curl http://localhost:8000/api/products/

# Get all categories
curl http://localhost:8000/api/categories/
```

### Test Admin Panel

1. Visit http://localhost:8000/admin/
2. Login with your superuser credentials
3. You can manage:
   - Users
   - Products & Categories
   - Orders
   - Vouchers & Promotions
   - Newsletter subscriptions
   - Contact messages

## 🐛 Troubleshooting

### Frontend Issues

#### Issue: Port 8080 already in use
**Solution:**
```bash
# Find and kill the process (Windows)
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

#### Issue: Dependencies won't install
**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Backend Issues

#### Issue: "No module named 'djongo'"
**Solution:**
```bash
pip install djongo==1.3.6
```

#### Issue: "No module named 'jwt'"
**Solution:**
```bash
pip install PyJWT
```

#### Issue: Can't activate virtual environment
**Solution (Windows PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

#### Issue: MongoDB connection failed
**Solutions:**
1. Check your internet connection
2. Verify MongoDB Atlas cluster is running
3. Check credentials in `.env` file
4. Whitelist your IP in MongoDB Atlas (0.0.0.0/0 for testing)

#### Issue: Migration errors
**Solution:**
```bash
python manage.py makemigrations --empty api
python manage.py migrate --run-syncdb
```

### Database Issues

#### Issue: Can't access MongoDB Atlas
**Solutions:**
1. Verify cluster is running at https://cloud.mongodb.com
2. Check your MongoDB Atlas account
3. Verify network access settings
4. Try pinging: `ping cluster0.qumhbyz.mongodb.net`

## 📚 Next Steps

After setup is complete:

1. ✅ **Add Sample Data**
   - Login to admin panel
   - Add categories (Noodle, Rice Cake, Side Dish, Drinks)
   - Add products with images
   - Create vouchers and promotions

2. ✅ **Test User Flow**
   - Register a new user
   - Browse products
   - Add items to cart
   - Place an order
   - Check admin panel for the order

3. ✅ **Integrate Frontend with Backend**
   - Update Vue components to use API
   - Replace localStorage with API calls
   - Implement JWT authentication

## 📖 Additional Documentation

- [Backend API Documentation](./BACKEND_API.md)
- [MongoDB Guide](./MONGODB_GUIDE.md)
- [Frontend Integration Guide](./FRONTEND_GUIDE.md)
- [Backend Complete Guide](./BACKEND_COMPLETE.md)

## 🔗 Quick Links

- **Frontend Repository:** Vue.js 3 app in `/src`
- **Backend Repository:** Django app in `/backend`
- **API Documentation:** http://localhost:8000/api/ (when running)
- **MongoDB Atlas:** https://cloud.mongodb.com

## ✅ Checklist

Use this checklist to verify your setup:

### Frontend
- [ ] Node.js installed
- [ ] Dependencies installed (`npm install`)
- [ ] Dev server running (`npm run serve`)
- [ ] Can access http://localhost:8080

### Backend
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Dev server running (`python manage.py runserver`)
- [ ] Can access http://localhost:8000/api/

### Database
- [ ] MongoDB Atlas account created
- [ ] Cluster running
- [ ] Connection string in `.env`
- [ ] Collections visible in Atlas dashboard

**Once all checkboxes are complete, your setup is done! 🎉**
