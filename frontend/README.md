# 🍜 Ramyeon Corner - Full Stack Application

A modern full-stack web application for a ramyeon (Korean instant noodle) restaurant, built with Vue.js 3 and Django REST Framework with MongoDB Atlas.

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Environment Configuration](#environment-configuration)
- [Documentation](#documentation)
- [Contributing](#contributing)

## 🎯 Overview

Ramyeon Corner is a complete restaurant management system featuring:
- **Customer-facing web app** for browsing menu, ordering, and managing vouchers
- **RESTful API backend** with authentication and order management
- **MongoDB Atlas** cloud database
- **Admin panel** for content and order management

## 🛠️ Tech Stack

### Frontend
- **Framework:** Vue.js 3
- **Styling:** Tailwind CSS
- **Build Tool:** Vue CLI
- **QR Code:** qrcode library
- **HTTP Client:** Axios (for API calls)

### Backend
- **Framework:** Django 5.2.1
- **API:** Django REST Framework 3.16.0
- **Database:** MongoDB Atlas (cloud)
- **Authentication:** JWT (JSON Web Tokens)
- **ODM:** Djongo (Django-MongoDB connector)

## 📁 Project Structure

```
ramyeonsite/
├── src/                      # Vue.js Frontend
│   ├── components/          # Vue components
│   ├── assets/              # Images, styles
│   ├── App.vue             # Root component
│   └── main.js             # Entry point
│
├── backend/                 # Django Backend
│   ├── backend/
│   │   ├── api/            # Main API app
│   │   │   ├── models.py   # Database models
│   │   │   ├── serializers.py
│   │   │   ├── views.py    # API endpoints
│   │   │   └── urls.py
│   │   ├── settings.py     # Django settings
│   │   └── urls.py         # Main URL config
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                # Environment variables
│
├── docs/                    # Documentation
│   ├── SETUP.md            # Complete setup guide
│   ├── API.md              # API documentation
│   └── MONGODB.md          # MongoDB guide
│
├── package.json            # Frontend dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

**For Frontend:**
- Node.js 14+ 
- npm or yarn

**For Backend:**
- Python 3.8+
- pip
- Virtual environment

### Frontend Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run serve
```

Visit: http://localhost:8080

### Backend Quick Start

```bash
# Navigate to backend
cd backend

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install djongo==1.3.6
pip install PyJWT

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit API: http://localhost:8000/api/  
Visit Admin: http://localhost:8000/admin/

## 💻 Frontend Setup

### Installation

1. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

2. **Start development server:**

   ```bash
   npm run serve
   ```

3. **Build for production:**

   ```bash
   npm run build
   ```

### Available Scripts

- `npm run serve` - Start dev server with hot-reload
- `npm run build` - Build for production
- `npm run lint` - Lint and fix code

## 🔧 Backend Setup

### Installation

1. **Navigate to backend:**

   ```bash
   cd backend
   ```

2. **Activate virtual environment:**

   **Windows PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   **Windows CMD:**
   ```cmd
   .\venv\Scripts\activate.bat
   ```

3. **Install MongoDB connector:**

   ```bash
   pip install djongo==1.3.6
   ```

4. **Configure environment:**

   Your `.env` file is already configured with MongoDB Atlas:
   ```env
   MONGODB_URI=mongodb+srv://admin:***@cluster0.qumhbyz.mongodb.net/pos_system
   MONGODB_DATABASE=pos_system
   ```

5. **Run database migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server:**

   ```bash
   python manage.py runserver
   ```

## ✨ Features

### Customer Features
- ✅ User registration and authentication
- ✅ Browse menu by categories
- ✅ Search products
- ✅ Shopping cart management
- ✅ Order placement (delivery/pickup)
- ✅ Voucher/coupon system
- ✅ Points rewards (1 point per ₱10)
- ✅ User profile management
- ✅ Order history
- ✅ Newsletter subscription
- ✅ Contact form

### Admin Features
- ✅ User management
- ✅ Product/category management
- ✅ Order management
- ✅ Voucher creation
- ✅ Promotion management
- ✅ Dashboard analytics
- ✅ Customer messages

### Technical Features
- ✅ JWT authentication
- ✅ RESTful API
- ✅ MongoDB cloud database
- ✅ Responsive design
- ✅ CORS enabled
- ✅ Image upload support
- ✅ QR code generation

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login (get JWT tokens) |
| POST | `/api/auth/logout/` | Logout user |
| GET | `/api/auth/profile/` | Get user profile |
| PUT | `/api/auth/profile/update/` | Update profile |

### Product Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| GET | `/api/products/` | List all products |
| GET | `/api/products/?category={id}` | Filter by category |
| GET | `/api/products/?search={query}` | Search products |
| GET | `/api/products/?featured=true` | Get featured products |

### Cart Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/my_cart/` | Get user's cart |
| POST | `/api/cart/add_item/` | Add item to cart |
| POST | `/api/cart/update_item/` | Update item quantity |
| POST | `/api/cart/remove_item/` | Remove item |
| POST | `/api/cart/clear/` | Clear cart |

### Order Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List user's orders |
| POST | `/api/orders/` | Create new order |
| GET | `/api/orders/{id}/` | Get order details |
| POST | `/api/orders/{id}/cancel/` | Cancel order |

### Voucher Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vouchers/` | List active vouchers |
| POST | `/api/vouchers/{id}/claim/` | Claim voucher |
| GET | `/api/user-vouchers/` | User's vouchers |
| GET | `/api/user-vouchers/available/` | Available vouchers |

### Promotion Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/promotions/` | List active promotions |
| GET | `/api/promotions/{id}/` | Get promotion details |

### Other Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/newsletter/subscribe/` | Subscribe to newsletter |
| POST | `/api/contact/` | Submit contact message |

## 🔑 Environment Configuration

### Frontend (.env - if needed)
```env
VUE_APP_API_URL=http://localhost:8000/api/
```

### Backend (.env)
```env
# MongoDB Atlas (Cloud Database)
MONGODB_URI=mongodb+srv://admin:***@cluster0.qumhbyz.mongodb.net/pos_system
MONGODB_DATABASE=pos_system

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend URL
FRONTEND_URL=http://localhost:8080
```

### Why 2 .env Files?

1. **`.env`** - Your actual credentials (NOT in git)
2. **`.env.example`** - Template for other developers (safe to share)

The `.env` file is in `.gitignore` to protect your credentials!

## 📚 Documentation

Detailed guides are available in the `docs/` folder:

- **[SETUP.md](./docs/SETUP.md)** - Complete setup guide
- **[BACKEND_API.md](./docs/BACKEND_API.md)** - Full API documentation
- **[MONGODB_GUIDE.md](./docs/MONGODB_GUIDE.md)** - MongoDB Atlas guide
- **[FRONTEND_GUIDE.md](./docs/FRONTEND_GUIDE.md)** - Frontend integration guide

Backend-specific documentation:
- `backend/INSTALL_INSTRUCTIONS.md` - Backend installation
- `backend/MONGODB_SETUP.md` - MongoDB setup details

## 🗄️ Database Models

### MongoDB Collections

1. **users** - User accounts with points
2. **categories** - Product categories
3. **products** - Menu items
4. **vouchers** - Discount coupons
5. **user_vouchers** - Claimed vouchers
6. **promotions** - Special offers
7. **carts** - Shopping carts
8. **cart_items** - Cart items
9. **orders** - Customer orders
10. **order_items** - Order items
11. **newsletter_subscriptions** - Newsletter
12. **contact_messages** - Contact messages

## 🔗 Access Points

### Development URLs

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **MongoDB Atlas:** https://cloud.mongodb.com

## 🛡️ Security

- ✅ JWT token authentication
- ✅ CORS protection
- ✅ Password hashing (bcrypt)
- ✅ Environment variables for secrets
- ✅ MongoDB Atlas security
- ✅ Input validation

## 🚧 Development

### Frontend Development

```bash
# Install dependencies
npm install

# Run dev server
npm run serve

# Build for production
npm run build

# Lint code
npm run lint
```

### Backend Development

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 🧪 Testing

### Test API with curl

```bash
# Get products
curl http://localhost:8000/api/products/

# Register user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123","password2":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'
```

## 🐛 Troubleshooting

### Frontend Issues

**Issue: Dependencies not installing**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Issue: Port already in use**
```bash
# Kill process on port 8080 (Windows)
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Backend Issues

**Issue: "No module named 'djongo'"**
```bash
pip install djongo==1.3.6
```

**Issue: MongoDB connection failed**
- Check internet connection
- Verify MongoDB Atlas cluster is running
- Check credentials in `.env`
- Whitelist IP in MongoDB Atlas

**Issue: Migration errors**
```bash
python manage.py makemigrations --empty api
python manage.py migrate --run-syncdb
```

## 📞 Support & Resources

- **MongoDB Atlas:** https://cloud.mongodb.com
- **Django Docs:** https://docs.djangoproject.com
- **Vue.js Docs:** https://vuejs.org
- **DRF Docs:** https://www.django-rest-framework.org

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is private and proprietary.

---

**Built with ❤️ for Ramyeon Corner**