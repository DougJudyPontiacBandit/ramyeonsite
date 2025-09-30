# Ramyeon Site - POS System Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Frontend Components](#frontend-components)
3. [Backend API](#backend-api)
4. [Database Schema](#database-schema)
5. [Authentication & Security](#authentication--security)
6. [API Documentation](#api-documentation)
7. [Deployment](#deployment)
8. [Development Guidelines](#development-guidelines)
9. [Testing](#testing)
10. [Performance Optimization](#performance-optimization)
11. [Monitoring & Logging](#monitoring--logging)
12. [Contributing](#contributing)

## Architecture Overview

### System Architecture

The Ramyeon POS system follows a microservices architecture with three main components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Customer        │    │ Backend API     │    │ Admin           │
│ Frontend        │◄──►│ (Django REST)   │◄──►│ Frontend        │
│ (Vue.js)        │    │                 │    │ (Vue.js)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Database        │
                       │ (MongoDB Atlas) │
                       └─────────────────┘
```

### Technology Stack

#### Customer Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **QRCode.js**: QR code generation
- **Anthropic AI SDK**: AI integration

#### Backend API
- **Django 5.2**: Python web framework
- **Django REST Framework**: API development toolkit
- **MongoDB**: NoSQL database
- **PyMongo**: MongoDB driver for Python
- **JWT**: JSON Web Token authentication
- **CORS**: Cross-Origin Resource Sharing

#### Admin Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vite**: Fast build tool and dev server
- **Chart.js**: Data visualization
- **Vue-ChartJS**: Vue wrapper for Chart.js

#### Database
- **MongoDB Atlas**: Cloud-hosted MongoDB
- **Local MongoDB**: Development fallback
- **Collections**: users, customers, categories, orders, promotions, reports

## Frontend Components

### Customer Frontend Structure

```
src/
├── components/          # Reusable Vue components
│   ├── App.vue         # Root component
│   ├── HelloWorld.vue  # Home page
│   ├── Menu.vue        # Menu display
│   ├── Cart.vue        # Shopping cart
│   ├── Login.vue       # Authentication
│   ├── SignUp.vue      # User registration
│   ├── Profile.vue     # User profile
│   ├── Promotions.vue  # Promotions display
│   ├── ContactUs.vue   # Contact page
│   ├── AboutUs.vue     # About page
│   ├── QRCode.vue      # QR code component
│   └── VoucherModal.vue # Voucher modal
├── assets/             # Static assets
│   ├── food/          # Food images
│   ├── Home/          # Home page assets
│   └── Nav Bar/       # Navigation assets
├── api.js             # API service layer
└── main.js            # Application entry point
```

### Key Components

#### App.vue
Main application component handling:
- Page routing and navigation
- User authentication state
- Cart management
- Dark mode toggle
- Newsletter subscription

#### Menu.vue
Menu display component featuring:
- Category-based food filtering
- Add to cart functionality
- Food item details (price, description, image)
- Responsive grid layout

#### Cart.vue
Shopping cart component with:
- Item quantity management
- Total price calculation
- Persistent storage (localStorage)
- Checkout process

#### Authentication Components
- **Login.vue**: User login form with validation
- **SignUp.vue**: User registration with email validation
- **Profile.vue**: User profile management

### Admin Frontend Structure

```
backend/frontend/src/
├── components/         # Admin components
├── views/             # Page views
├── router/            # Routing configuration
├── services/          # API services
├── stores/            # State management
└── main.js            # Application entry
```

## Backend API

### API Structure

```
backend/backend/
├── posbackend/         # Django project settings
├── app/               # Main Django app
│   ├── views.py       # API endpoints
│   ├── models.py      # Data models
│   ├── serializers.py # Data serialization
│   ├── database.py    # MongoDB connection
│   ├── middleware/    # Custom middleware
│   └── kpi_views/     # Business logic views
├── notifications/     # Notification system
├── promotions/        # Promotion management
├── reports/           # Reporting system
└── requirements.txt   # Python dependencies
```

### API Endpoints

#### Authentication Endpoints
```
POST /api/v1/auth/login/
POST /api/v1/auth/register/
POST /api/v1/auth/logout/
```

#### User Management
```
GET    /api/v1/users/           # List users
POST   /api/v1/users/           # Create user
GET    /api/v1/users/{id}/      # Get user details
PUT    /api/v1/users/{id}/      # Update user
DELETE /api/v1/users/{id}/      # Delete user
```

#### Customer Management
```
GET  /api/v1/customers/         # List customers
POST /api/v1/customers/         # Create customer
GET  /api/v1/customers/{id}/    # Get customer
PUT  /api/v1/customers/{id}/    # Update customer
```

#### Menu Management
```
GET  /api/v1/categories/        # List categories
POST /api/v1/categories/        # Create category
GET  /api/v1/categories/{id}/   # Get category
PUT  /api/v1/categories/{id}/   # Update category
```

#### Order Management
```
GET  /api/v1/orders/            # List orders
POST /api/v1/orders/            # Create order
GET  /api/v1/orders/{id}/       # Get order details
PUT  /api/v1/orders/{id}/       # Update order status
```

#### Cart Management
```
GET  /api/v1/cart/              # Get user cart
POST /api/v1/cart/add/          # Add item to cart
DELETE /api/v1/cart/{item_id}/  # Remove item from cart
```

#### Promotions
```
GET  /api/v1/promotions/        # List promotions
POST /api/v1/promotions/        # Create promotion
GET  /api/v1/promotions/{id}/   # Get promotion
PUT  /api/v1/promotions/{id}/   # Update promotion
```

#### Reports
```
GET /api/v1/reports/sales/      # Sales reports
GET /api/v1/reports/categories/ # Category reports
GET /api/v1/reports/items/      # Item reports
```

### Middleware

#### RequestLoggingMiddleware
- Logs all incoming requests
- Tracks request metadata (method, path, user)
- Performance monitoring

#### ErrorHandlingMiddleware
- Global error handling
- Standardized error responses
- Exception logging

#### JWTAuthenticationMiddleware
- JWT token validation
- User authentication
- Request user context

### Services

#### Database Service (database.py)
```python
class DatabaseManager:
    def __init__(self):
        self.client = None
        self.database = None
        self.current_db = None

    def connect_to_mongodb(self):
        # MongoDB connection logic with fallback

    def get_database(self):
        # Return appropriate database instance
```

#### Business Logic Services
- **CustomerKPI.py**: Customer analytics and KPIs
- **reportByCategoryService.py**: Category-based reporting
- **reportByItemService.py**: Item-based reporting
- **salesLogsService.py**: Sales logging and analysis

## Database Schema

### MongoDB Collections

#### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "hashed_password",
  "firstName": "John",
  "lastName": "Doe",
  "role": "customer|admin",
  "created_at": ISODate,
  "updated_at": ISODate,
  "is_active": true
}
```

#### Customers Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "phone": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "City",
    "state": "State",
    "zipCode": "12345"
  },
  "loyalty_points": 150,
  "total_orders": 25,
  "created_at": ISODate
}
```

#### Categories Collection
```json
{
  "_id": ObjectId,
  "name": "Ramyeon",
  "description": "Korean instant noodles",
  "image_url": "https://...",
  "is_active": true,
  "sort_order": 1,
  "created_at": ISODate
}
```

#### Items Collection
```json
{
  "_id": ObjectId,
  "category_id": ObjectId,
  "name": "Shin Ramyun",
  "description": "Spicy Korean noodles",
  "price": 8.99,
  "image_url": "https://...",
  "is_available": true,
  "ingredients": ["noodles", "soup base", "vegetables"],
  "created_at": ISODate
}
```

#### Orders Collection
```json
{
  "_id": ObjectId,
  "customer_id": ObjectId,
  "items": [
    {
      "item_id": ObjectId,
      "quantity": 2,
      "price": 8.99,
      "subtotal": 17.98
    }
  ],
  "total_amount": 17.98,
  "status": "pending|confirmed|preparing|ready|completed",
  "order_type": "dine-in|takeout|delivery",
  "payment_method": "cash|card",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

#### Promotions Collection
```json
{
  "_id": ObjectId,
  "title": "Weekend Special",
  "description": "20% off all ramyeon",
  "discount_type": "percentage|fixed",
  "discount_value": 20,
  "valid_from": ISODate,
  "valid_until": ISODate,
  "is_active": true,
  "applicable_items": [ObjectId],
  "created_at": ISODate
}
```

#### Session Logs Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "session_start": ISODate,
  "session_end": ISODate,
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "actions": [
    {
      "action": "login|view_menu|add_to_cart|checkout",
      "timestamp": ISODate,
      "details": {}
    }
  ]
}
```

## Authentication & Security

### JWT Authentication

#### Token Structure
```json
{
  "user_id": "user_id",
  "email": "user@example.com",
  "role": "customer|admin",
  "iat": 1640995200,
  "exp": 1641081600
}
```

#### Authentication Flow
1. User submits login credentials
2. Backend validates credentials
3. JWT token generated and returned
4. Frontend stores token in localStorage
5. Subsequent requests include token in Authorization header
6. Backend validates token on protected routes

### Security Measures

#### Password Security
- bcrypt hashing for passwords
- Minimum password requirements
- Password reset functionality

#### API Security
- CORS configuration
- Rate limiting
- Input validation and sanitization
- SQL injection prevention (MongoDB)

#### Data Protection
- Environment variables for sensitive data
- Encrypted database connections
- Secure token storage

## Deployment

### Production Environment Setup

#### Environment Variables
```env
# Django Settings
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
MONGODB_URI=mongodb+srv://prod-user:password@cluster.mongodb.net/pos_system_prod
MONGODB_DATABASE=pos_system_prod

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Integration (future)
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

#### Deployment Steps

1. **Prepare Production Build**
   ```bash
   # Customer Frontend
   npm run build

   # Admin Frontend
   cd backend/frontend
   npm run build
   ```

2. **Configure Web Server**
   - Nginx for static file serving
   - Gunicorn for Django application
   - SSL certificate configuration

3. **Database Migration**
   - Backup production database
   - Run any pending migrations
   - Update indexes if needed

4. **Deploy Services**
   - Deploy frontend to CDN/Netlify
   - Deploy backend to cloud server (Heroku, DigitalOcean, etc.)
   - Configure environment variables

### Monitoring & Maintenance

#### Health Checks
- API health endpoint: `/api/v1/health/`
- Database connection monitoring
- Service uptime monitoring

#### Backup Strategy
- Daily database backups
- Automated backup scripts
- Offsite backup storage

#### Performance Monitoring
- Response time tracking
- Database query optimization
- Frontend bundle size monitoring

## Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use Black for code formatting
- Type hints for function parameters
- Docstrings for all functions and classes

#### JavaScript/Vue (Frontend)
- ESLint configuration
- Consistent naming conventions
- Component composition over inheritance
- Proper error handling

### Git Workflow

#### Branch Naming
- `feature/feature-name`: New features
- `bugfix/bug-description`: Bug fixes
- `hotfix/critical-fix`: Critical production fixes
- `refactor/refactor-description`: Code refactoring

#### Commit Messages
```
type(scope): description

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

### Testing

#### Backend Testing
```bash
# Run Django tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report
```

#### Frontend Testing
```bash
# Run Vue tests
npm run test:unit

# Run E2E tests (if configured)
npm run test:e2e
```

### API Documentation

### API Base URL
- **Development:** `http://localhost:8000/api/v1/`
- **Production:** `https://yourdomain.com/api/v1/`

### Authentication
All API endpoints (except login/register) require authentication via JWT token.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### OpenAPI Specification
- API endpoints documented with OpenAPI 3.0
- Swagger UI for interactive documentation
- Postman collection for testing

### Request/Response Examples

#### Authentication Endpoints

**Login Request:**
```json
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Login Response:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "customer"
  }
}
```

**Register Request:**
```json
POST /api/v1/auth/register/
{
  "email": "newuser@example.com",
  "password": "password123",
  "firstName": "Jane",
  "lastName": "Smith"
}
```

**Register Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": "new_user_id",
    "email": "newuser@example.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "role": "customer"
  }
}
```

#### User Management Endpoints

**Get User Profile:**
```json
GET /api/v1/users/profile/
Authorization: Bearer <token>

Response:
{
  "id": "user_id",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "customer",
  "created_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

**Update User Profile:**
```json
PUT /api/v1/users/profile/
Authorization: Bearer <token>
{
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+1234567890"
}

Response:
{
  "success": true,
  "message": "Profile updated successfully",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+1234567890",
    "updated_at": "2024-01-01T12:00:00Z"
  }
}
```

#### Customer Management Endpoints

**Get Customer List:**
```json
GET /api/v1/customers/
Authorization: Bearer <token>

Response:
{
  "success": true,
  "customers": [
    {
      "id": "customer_id",
      "user_id": "user_id",
      "phone": "+1234567890",
      "address": {
        "street": "123 Main St",
        "city": "City",
        "state": "State",
        "zipCode": "12345"
      },
      "loyalty_points": 150,
      "total_orders": 25,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Create Customer:**
```json
POST /api/v1/customers/
Authorization: Bearer <token>
{
  "phone": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "City",
    "state": "State",
    "zipCode": "12345"
  }
}

Response:
{
  "success": true,
  "message": "Customer created successfully",
  "customer": {
    "id": "new_customer_id",
    "user_id": "user_id",
    "phone": "+1234567890",
    "address": {
      "street": "123 Main St",
      "city": "City",
      "state": "State",
      "zipCode": "12345"
    },
    "loyalty_points": 0,
    "total_orders": 0,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Menu Management Endpoints

**Get Categories:**
```json
GET /api/v1/categories/

Response:
{
  "success": true,
  "categories": [
    {
      "id": "category_id",
      "name": "Ramyeon",
      "description": "Korean instant noodles",
      "image_url": "https://example.com/ramyeon.jpg",
      "is_active": true,
      "sort_order": 1,
      "items": [
        {
          "id": "item_id",
          "name": "Shin Ramyun",
          "description": "Spicy Korean noodles",
          "price": 8.99,
          "image_url": "https://example.com/shin-ramyun.jpg",
          "is_available": true,
          "ingredients": ["noodles", "soup base", "vegetables"]
        }
      ]
    }
  ]
}
```

**Get Items by Category:**
```json
GET /api/v1/categories/{category_id}/items/

Response:
{
  "success": true,
  "items": [
    {
      "id": "item_id",
      "category_id": "category_id",
      "name": "Shin Ramyun",
      "description": "Spicy Korean noodles",
      "price": 8.99,
      "image_url": "https://example.com/shin-ramyun.jpg",
      "is_available": true,
      "ingredients": ["noodles", "soup base", "vegetables"],
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Cart Management Endpoints

**Get User Cart:**
```json
GET /api/v1/cart/
Authorization: Bearer <token>

Response:
{
  "success": true,
  "cart": {
    "id": "cart_id",
    "user_id": "user_id",
    "items": [
      {
        "item_id": "item_id",
        "name": "Shin Ramyun",
        "price": 8.99,
        "quantity": 2,
        "subtotal": 17.98
      }
    ],
    "total_amount": 17.98,
    "item_count": 2,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
}
```

**Add Item to Cart:**
```json
POST /api/v1/cart/add/
Authorization: Bearer <token>
{
  "item_id": "item_id",
  "quantity": 2
}

Response:
{
  "success": true,
  "message": "Item added to cart",
  "cart": {
    "id": "cart_id",
    "user_id": "user_id",
    "items": [
      {
        "item_id": "item_id",
        "name": "Shin Ramyun",
        "price": 8.99,
        "quantity": 2,
        "subtotal": 17.98
      }
    ],
    "total_amount": 17.98,
    "item_count": 2
  }
}
```

**Update Cart Item:**
```json
PUT /api/v1/cart/{item_id}/
Authorization: Bearer <token>
{
  "quantity": 3
}

Response:
{
  "success": true,
  "message": "Cart item updated",
  "cart": {
    "id": "cart_id",
    "user_id": "user_id",
    "items": [
      {
        "item_id": "item_id",
        "name": "Shin Ramyun",
        "price": 8.99,
        "quantity": 3,
        "subtotal": 26.97
      }
    ],
    "total_amount": 26.97,
    "item_count": 3
  }
}
```

**Remove Item from Cart:**
```json
DELETE /api/v1/cart/{item_id}/
Authorization: Bearer <token>

Response:
{
  "success": true,
  "message": "Item removed from cart",
  "cart": {
    "id": "cart_id",
    "user_id": "user_id",
    "items": [],
    "total_amount": 0,
    "item_count": 0
  }
}
```

#### Order Management Endpoints

**Create Order:**
```json
POST /api/v1/orders/
Authorization: Bearer <token>
{
  "items": [
    {
      "item_id": "item_id",
      "quantity": 2,
      "price": 8.99
    }
  ],
  "order_type": "dine-in",
  "payment_method": "cash",
  "customer_notes": "Extra spicy please"
}

Response:
{
  "success": true,
  "message": "Order created successfully",
  "order": {
    "id": "order_id",
    "customer_id": "customer_id",
    "items": [
      {
        "item_id": "item_id",
        "name": "Shin Ramyun",
        "quantity": 2,
        "price": 8.99,
        "subtotal": 17.98
      }
    ],
    "total_amount": 17.98,
    "status": "pending",
    "order_type": "dine-in",
    "payment_method": "cash",
    "customer_notes": "Extra spicy please",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**Get Order History:**
```json
GET /api/v1/orders/
Authorization: Bearer <token>

Response:
{
  "success": true,
  "orders": [
    {
      "id": "order_id",
      "customer_id": "customer_id",
      "items": [
        {
          "item_id": "item_id",
          "name": "Shin Ramyun",
          "quantity": 2,
          "price": 8.99,
          "subtotal": 17.98
        }
      ],
      "total_amount": 17.98,
      "status": "completed",
      "order_type": "dine-in",
      "payment_method": "cash",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T01:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3
  }
}
```

#### Promotion Endpoints

**Get Active Promotions:**
```json
GET /api/v1/promotions/

Response:
{
  "success": true,
  "promotions": [
    {
      "id": "promotion_id",
      "title": "Weekend Special",
      "description": "20% off all ramyeon",
      "discount_type": "percentage",
      "discount_value": 20,
      "valid_from": "2024-01-01T00:00:00Z",
      "valid_until": "2024-01-07T23:59:59Z",
      "is_active": true,
      "applicable_items": ["item_id_1", "item_id_2"]
    }
  ]
}
```

#### Report Endpoints

**Get Sales Report:**
```json
GET /api/v1/reports/sales/?start_date=2024-01-01&end_date=2024-01-31

Response:
{
  "success": true,
  "report": {
    "period": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-31"
    },
    "summary": {
      "total_orders": 150,
      "total_revenue": 2500.00,
      "average_order_value": 16.67
    },
    "daily_sales": [
      {
        "date": "2024-01-01",
        "orders": 5,
        "revenue": 85.50
      }
    ],
    "top_items": [
      {
        "item_id": "item_id",
        "name": "Shin Ramyun",
        "quantity_sold": 45,
        "revenue": 404.55
      }
    ]
  }
}
```

### Error Handling

#### Standard Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "field_name": ["Specific error message"]
    }
  }
}
```

#### Common Error Codes
- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `DUPLICATE_ENTRY`: Resource already exists
- `SERVER_ERROR`: Internal server error
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INVALID_TOKEN`: JWT token is invalid or expired

#### HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Handling

#### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required"],
      "password": ["Password must be at least 8 characters"]
    }
  }
}
```

#### Error Codes
- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `SERVER_ERROR`: Internal server error

### Performance Optimization

#### Frontend
- Code splitting and lazy loading
- Image optimization
- Bundle size monitoring
- Caching strategies

#### Backend
- Database query optimization
- Caching with Redis (future)
- Asynchronous task processing
- Database indexing

#### Database
- Proper indexing on frequently queried fields
- Connection pooling
- Query optimization
- Data archiving strategies

## Testing

### Backend Testing

#### Unit Tests
```bash
# Run all Django tests
python manage.py test

# Run specific app tests
python manage.py test app
python manage.py test notifications
python manage.py test reports

# Run with coverage
coverage run manage.py test
coverage report
coverage html  # Generate HTML coverage report
```

#### Test Structure
```
backend/backend/
├── app/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_services.py
│   │   └── test_serializers.py
│   └── tests.py
├── notifications/tests.py
├── reports/tests.py
└── promotions/tests.py
```

#### Test Examples
```python
# test_models.py
from django.test import TestCase
from app.models import User, Customer

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            email="test@example.com",
            firstName="Test",
            lastName="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)

# test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from app.models import User

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

    def test_login_success(self):
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
```

### Frontend Testing

#### Vue.js Unit Tests
```bash
# Customer Frontend
npm run test:unit

# Admin Frontend
cd backend/frontend
npm run test:unit
```

#### Test Structure
```
src/
├── components/
│   ├── __tests__/
│   │   ├── Menu.test.js
│   │   ├── Cart.test.js
│   │   └── Login.test.js
└── tests/
    ├── setup.js
    └── utils.js
```

#### Test Examples
```javascript
// Menu.test.js
import { mount } from '@vue/test-utils'
import Menu from '@/components/Menu.vue'

describe('Menu.vue', () => {
  it('renders menu items correctly', () => {
    const wrapper = mount(Menu, {
      props: {
        items: [
          { id: 1, name: 'Shin Ramyun', price: 8.99 }
        ]
      }
    })
    expect(wrapper.text()).toContain('Shin Ramyun')
    expect(wrapper.text()).toContain('$8.99')
  })

  it('emits add-to-cart event when item is clicked', async () => {
    const wrapper = mount(Menu)
    await wrapper.find('.add-to-cart').trigger('click')
    expect(wrapper.emitted('add-to-cart')).toBeTruthy()
  })
})
```

#### E2E Testing
```bash
# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npx playwright test

# Run with UI
npx playwright test --ui
```

### API Testing

#### Postman Collection
```json
{
  "info": {
    "name": "Ramyeon POS API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/v1/auth/login/",
              "host": ["{{base_url}}"],
              "path": ["api", "v1", "auth", "login", ""]
            }
          }
        }
      ]
    }
  ]
}
```

## Performance Optimization

### Frontend Optimization

#### Code Splitting
```javascript
// Lazy load components
const Menu = () => import('@/components/Menu.vue')
const Cart = () => import('@/components/Cart.vue')

// Route-based code splitting
const routes = [
  {
    path: '/menu',
    component: () => import('@/views/Menu.vue')
  }
]
```

#### Image Optimization
```javascript
// Use WebP format when supported
const getImageUrl = (imageName) => {
  const supportsWebP = document.createElement('canvas')
    .toDataURL('image/webp').indexOf('data:image/webp') === 0
  
  return supportsWebP 
    ? `/images/${imageName}.webp`
    : `/images/${imageName}.jpg`
}
```

#### Caching Strategies
```javascript
// Service Worker for caching
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      caches.open('api-cache').then(cache => {
        return cache.match(event.request).then(response => {
          if (response) {
            return response
          }
          return fetch(event.request).then(fetchResponse => {
            cache.put(event.request, fetchResponse.clone())
            return fetchResponse
          })
        })
      })
    )
  }
})
```

### Backend Optimization

#### Database Optimization
```python
# Use database indexes
class Customer(models.Model):
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

# Optimize queries
def get_customers_with_orders():
    return Customer.objects.select_related('user').prefetch_related('orders')
```

#### Caching
```python
# Redis caching
from django.core.cache import cache

def get_menu_categories():
    cache_key = 'menu_categories'
    categories = cache.get(cache_key)
    
    if not categories:
        categories = Category.objects.filter(is_active=True)
        cache.set(cache_key, categories, 300)  # 5 minutes
    
    return categories
```

#### API Response Optimization
```python
# Pagination
class CustomerViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    
    def list(self, request):
        queryset = Customer.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
```

### Database Optimization

#### Indexing Strategy
```javascript
// MongoDB indexes
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "created_at": 1 })
db.orders.createIndex({ "customer_id": 1, "created_at": -1 })
db.orders.createIndex({ "status": 1, "created_at": -1 })
```

#### Query Optimization
```python
# Use aggregation for complex queries
def get_sales_report(start_date, end_date):
    pipeline = [
        {
            "$match": {
                "created_at": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "total_revenue": {"$sum": "$total_amount"}
            }
        }
    ]
    return db.orders.aggregate(pipeline)
```

## Monitoring & Logging

### Application Logging

#### Django Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'app': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

#### Custom Logging
```python
import logging

logger = logging.getLogger(__name__)

def process_order(order_data):
    try:
        # Process order logic
        logger.info(f"Processing order: {order_data['id']}")
        # ... processing code ...
        logger.info(f"Order processed successfully: {order_data['id']}")
    except Exception as e:
        logger.error(f"Order processing failed: {str(e)}", exc_info=True)
        raise
```

### Performance Monitoring

#### Django Debug Toolbar
```python
# settings.py (development only)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

#### Application Performance Monitoring
```python
# Custom middleware for performance tracking
import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            if duration > 1.0:  # Log slow requests
                logger.warning(f"Slow request: {request.path} took {duration:.2f}s")
        return response
```

### Health Checks

#### API Health Endpoint
```python
# views.py
from django.http import JsonResponse
from django.db import connection
from app.database import DatabaseManager

def health_check(request):
    try:
        # Check database connection
        db_manager = DatabaseManager()
        db_manager.connect_to_mongodb()
        
        # Check database query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)
```

## Contributing

### Development Workflow

#### Git Workflow
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push to remote
git push origin feature/new-feature

# 4. Create pull request
# Use GitHub/GitLab interface to create PR
```

#### Commit Message Convention
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add JWT token refresh functionality
fix(cart): resolve cart item quantity update issue
docs(api): update API documentation for new endpoints
```

### Code Review Process

#### Pull Request Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation updated if needed
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact considered
- [ ] Security implications reviewed

#### Review Guidelines
1. **Functionality**: Does the code work as intended?
2. **Readability**: Is the code easy to understand?
3. **Performance**: Are there any performance concerns?
4. **Security**: Are there any security vulnerabilities?
5. **Testing**: Are there adequate tests?

### Development Environment Setup

#### VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss",
    "vue.volar",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json"
  ]
}
```

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.57.0
    hooks:
      - id: eslint
        files: \.(js|vue)$
```

---

This documentation provides a comprehensive overview of the Ramyeon POS system. For specific implementation details, refer to the inline code comments and individual component documentation.
