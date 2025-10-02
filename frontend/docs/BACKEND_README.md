# Ramyeon Corner - Backend API

Django REST API backend for the Ramyeon Corner restaurant application.

## Tech Stack

- **Framework:** Django 5.2.1
- **API:** Django REST Framework 3.16.0
- **Database:** SQLite (default) / PostgreSQL / MySQL
- **Authentication:** JWT (JSON Web Tokens)
- **CORS:** django-cors-headers

## Features

- ✅ User Authentication & Authorization (JWT)
- ✅ Product & Category Management
- ✅ Shopping Cart System
- ✅ Order Processing
- ✅ Voucher/Coupon System
- ✅ Promotions Management
- ✅ Newsletter Subscriptions
- ✅ Contact Form
- ✅ Admin Dashboard

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## Installation & Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create and activate virtual environment

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

Admin panel: `http://localhost:8000/admin/`

## API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Products & Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Get category details
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/?category={id}` - Filter by category
- `GET /api/products/?featured=true` - Get featured products
- `GET /api/products/?search={query}` - Search products

### Shopping Cart

- `GET /api/cart/my_cart/` - Get current user's cart
- `POST /api/cart/add_item/` - Add item to cart
- `POST /api/cart/update_item/` - Update cart item quantity
- `POST /api/cart/remove_item/` - Remove item from cart
- `POST /api/cart/clear/` - Clear cart

### Orders

- `GET /api/orders/` - List user's orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/{id}/cancel/` - Cancel order

### Vouchers

- `GET /api/vouchers/` - List active vouchers
- `POST /api/vouchers/{id}/claim/` - Claim voucher
- `GET /api/user-vouchers/` - List user's vouchers
- `GET /api/user-vouchers/available/` - Get available vouchers

### Promotions

- `GET /api/promotions/` - List active promotions
- `GET /api/promotions/{id}/` - Get promotion details

### Newsletter & Contact

- `POST /api/newsletter/subscribe/` - Subscribe to newsletter
- `POST /api/contact/` - Submit contact form

## Database Models

### User
- Custom user model with points system
- Fields: username, email, phone, points, address, etc.

### Category
- Product categories
- Fields: name, description, image, is_active

### Product
- Menu items/products
- Fields: name, description, category, price, image, stock_quantity

### Voucher
- Discount vouchers/coupons
- Fields: code, discount_type, discount_value, valid dates

### Promotion
- Special promotions
- Fields: title, description, discount_percentage, valid dates

### Cart & CartItem
- Shopping cart system
- Automatic total calculation

### Order & OrderItem
- Order management
- Status tracking (pending → completed)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_ENGINE` | Database engine | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Database name | `db.sqlite3` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `http://localhost:8080` |
| `JWT_SECRET_KEY` | JWT secret | - |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `60` |

## Database Configuration

### SQLite (Default - Development)

```env
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

### PostgreSQL

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=ramyeon_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### MySQL

```env
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=ramyeon_db
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

## Running Tests

```bash
python manage.py test
```

## Production Deployment

### 1. Update settings for production

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com
```

### 2. Collect static files

```bash
python manage.py collectstatic
```

### 3. Run with Gunicorn

```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

### 4. Use a process manager (systemd, supervisor, etc.)

### 5. Set up nginx as reverse proxy

## Admin Panel

Access the admin panel at `/admin/` to manage:

- Users
- Products & Categories
- Orders
- Vouchers & Promotions
- Newsletter Subscriptions
- Contact Messages

## API Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Login Flow

1. `POST /api/auth/login/` with email and password
2. Receive `access_token` and `refresh_token`
3. Include token in subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```

## CORS Configuration

CORS is configured to allow requests from the Vue.js frontend:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]
```

## Project Structure

```
backend/
├── backend/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI application
│   ├── asgi.py              # ASGI application
│   ├── api/                 # Main API app
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # API views
│   │   ├── urls.py          # API URLs
│   │   └── admin.py         # Admin configuration
│   ├── app/                 # Additional app
│   ├── notifications/       # Notifications module
│   ├── promotions/          # Promotions module
│   └── reports/             # Reports module
├── manage.py                # Django management
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Make sure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### Issue: Database errors

**Solution:** Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: CORS errors

**Solution:** Check CORS_ALLOWED_ORIGINS in settings matches your frontend URL

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run tests and linting
5. Submit a pull request

## License

This project is private and proprietary.
