# 🔄 Frontend-Backend Connection Flow

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:8080                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Vue.js Components                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │ Login.vue│  │SignUp.vue│  │Profile.vue│ ...        │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │    │
│  │       │             │              │                   │    │
│  │       └─────────────┼──────────────┘                   │    │
│  │                     │                                  │    │
│  │              ┌──────▼──────┐                          │    │
│  │              │             │                          │    │
│  │              │  api.js     │  (Axios HTTP Client)    │    │
│  │              │             │                          │    │
│  │              │  - authAPI  │                          │    │
│  │              │  - posAPI   │                          │    │
│  │              └──────┬──────┘                          │    │
│  │                     │                                  │    │
│  └─────────────────────┼──────────────────────────────────┘    │
│                        │                                        │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         │ HTTP Request
                         │ Authorization: Bearer <JWT>
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO BACKEND                                │
│                  http://localhost:8000                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   URL Router                            │    │
│  │              (posbackend/urls.py)                       │    │
│  │                                                         │    │
│  │              path('api/', include('api.urls'))         │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       │                                         │
│  ┌────────────────────▼───────────────────────────────────┐    │
│  │               API URL Routes                            │    │
│  │                (api/urls.py)                            │    │
│  │                                                         │    │
│  │  ┌───────────────────────────────────────────────┐    │    │
│  │  │ Customer Auth Routes                          │    │    │
│  │  │  /api/auth/customer/login/                    │    │    │
│  │  │  /api/auth/customer/register/                 │    │    │
│  │  │  /api/auth/customer/me/                       │    │    │
│  │  │  /api/auth/customer/password/change/          │    │    │
│  │  └────────────┬──────────────────────────────────┘    │    │
│  │               │                                        │    │
│  │  ┌────────────▼──────────────────────────────────┐    │    │
│  │  │ POS Routes                                    │    │    │
│  │  │  /api/pos/scan-user/                          │    │    │
│  │  │  /api/pos/scan-promotion/                     │    │    │
│  │  │  /api/pos/redeem-promotion/                   │    │    │
│  │  │  /api/pos/award-points/                       │    │    │
│  │  │  /api/pos/process-order-points/               │    │    │
│  │  └────────────┬──────────────────────────────────┘    │    │
│  └───────────────┼──────────────────────────────────────┘    │
│                  │                                            │
│  ┌───────────────▼──────────────────────────────────────┐    │
│  │                    View Functions                     │    │
│  │                                                       │    │
│  │  ┌──────────────────┐  ┌──────────────────┐         │    │
│  │  │  auth_views.py   │  │  pos_views.py    │         │    │
│  │  │                  │  │                  │         │    │
│  │  │ - customer_login │  │ - scan_user_qr   │         │    │
│  │  │ - customer_reg.. │  │ - scan_promo..   │         │    │
│  │  │ - customer_me    │  │ - redeem_prom..  │         │    │
│  │  │ - change_passw.. │  │ - award_points   │         │    │
│  │  └────────┬─────────┘  └────────┬─────────┘         │    │
│  │           │                     │                    │    │
│  └───────────┼─────────────────────┼────────────────────┘    │
│              │                     │                          │
│  ┌───────────▼─────────────────────▼────────────────────┐    │
│  │              Services & Utils                         │    │
│  │                                                       │    │
│  │  ┌──────────────────────────────────────────┐        │    │
│  │  │  customer_auth_service.py                │        │    │
│  │  │  - authenticate_customer()               │        │    │
│  │  │  - create_customer()                     │        │    │
│  │  │  - hash_password()                       │        │    │
│  │  └────────────────┬─────────────────────────┘        │    │
│  │                   │                                  │    │
│  │  ┌────────────────▼─────────────────────────┐        │    │
│  │  │  jwt_utils.py                            │        │    │
│  │  │  - generate_jwt_token()                  │        │    │
│  │  │  - decode_jwt_token()                    │        │    │
│  │  │  - @jwt_required decorator               │        │    │
│  │  └────────────────┬─────────────────────────┘        │    │
│  │                   │                                  │    │
│  └───────────────────┼──────────────────────────────────┘    │
│                      │                                       │
│  ┌───────────────────▼──────────────────────────────────┐    │
│  │              Database Layer                           │    │
│  │                                                       │    │
│  │  ┌────────────────┐      ┌──────────────────┐        │    │
│  │  │   MongoDB      │      │  SQLite (Django) │        │    │
│  │  │   Atlas        │      │  Admin & Auth    │        │    │
│  │  │                │      │                  │        │    │
│  │  │ - customers    │      │ - sessions       │        │    │
│  │  │ - products     │      │ - admin users    │        │    │
│  │  │ - orders       │      └──────────────────┘        │    │
│  │  └────────────────┘                                  │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow

```
┌──────────┐                                              ┌──────────┐
│  User    │                                              │ Backend  │
└────┬─────┘                                              └────┬─────┘
     │                                                         │
     │  1. Enter email & password                             │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │                    2. Validate credentials              │
     │                       - Check email exists              │
     │                       - Verify password hash            │
     │                                                         │
     │  3. Return JWT token + customer data                   │
     │  ◀─────────────────────────────────────────────────────│
     │  {                                                      │
     │    token: "eyJhbGc...",                                │
     │    customer: { _id, email, ... },                      │
     │    message: "Login successful"                         │
     │  }                                                      │
     │                                                         │
     │  4. Save token to localStorage                         │
     │     - access_token                                     │
     │     - ramyeon_user_session                             │
     │                                                         │
     │  5. Make authenticated request                         │
     │     Authorization: Bearer <token>                      │
     │─────────────────────────────────────────────────────▶  │
     │                                                         │
     │                    6. Decode & validate JWT             │
     │                       - Check expiration                │
     │                       - Extract customer_id             │
     │                                                         │
     │  7. Return protected data                              │
     │  ◀─────────────────────────────────────────────────────│
     │                                                         │
```

---

## 📝 Request/Response Examples

### Example 1: User Registration

**Frontend (Login.vue):**
```javascript
const response = await authAPI.register({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  phone: '+1234567890',
  password: 'SecurePass123'
});
```

**What happens:**
```
1. Frontend → api.js
   ├─ Formats data: { email, password, username, full_name, phone }
   └─ axios.post('http://localhost:8000/api/auth/customer/register/', data)

2. Backend → urls.py
   ├─ Matches: path('auth/customer/register/', customer_register)
   └─ Routes to: auth_views.customer_register()

3. Backend → auth_views.py
   ├─ Calls: CustomerAuthService.create_customer()
   └─ Returns: { token, customer, message }

4. Backend → customer_auth_service.py
   ├─ Hashes password with bcrypt
   ├─ Generates customer ID: CUST-00001
   ├─ Inserts into MongoDB customers collection
   └─ Returns customer document

5. Backend → jwt_utils.py
   ├─ generate_jwt_token(customer)
   └─ Returns signed JWT token

6. Response → Frontend
   ├─ Status: 201 Created
   └─ Data: { token, customer, message }

7. Frontend → api.js
   ├─ Saves token to localStorage
   └─ Returns response to component

8. Component → Login.vue
   ├─ Creates user session
   ├─ Saves to localStorage
   └─ Emits 'loginSuccess' event
```

---

### Example 2: Get Customer Profile (Authenticated)

**Frontend:**
```javascript
const response = await authAPI.getProfile();
```

**What happens:**
```
1. Frontend → api.js
   ├─ Gets token from localStorage
   ├─ axios.get('http://localhost:8000/api/auth/customer/me/')
   └─ Headers: { Authorization: 'Bearer eyJhbGc...' }

2. Backend → interceptor (jwt_utils.py)
   ├─ Extracts token from Authorization header
   ├─ decode_jwt_token(token)
   ├─ Validates expiration
   ├─ Extracts customer_id from payload
   └─ Adds to request.customer

3. Backend → auth_views.py
   ├─ customer_me() function (protected with @jwt_required)
   ├─ Gets customer_id from request.customer
   ├─ Calls: CustomerAuthService.get_customer_by_id()
   └─ Returns sanitized customer data

4. Response → Frontend
   ├─ Status: 200 OK
   └─ Data: { customer: { _id, email, full_name, ... } }
```

---

## 🌊 Data Flow

### Registration/Login Flow
```
User Input → Vue Component → api.js → Axios → HTTP Request
                                                      ↓
                                              Django URL Router
                                                      ↓
                                               View Function
                                                      ↓
                                              Service Layer
                                                      ↓
                                           MongoDB (customers)
                                                      ↓
                                        Generate JWT Token
                                                      ↓
                                           HTTP Response
                                                      ↓
                              api.js ← Save Token ← Axios
                                                      ↓
                                           Vue Component
                                                      ↓
                                            Update UI
```

### Authenticated Request Flow
```
Vue Component → api.js → Add JWT from localStorage
                              ↓
                      Axios HTTP Request
                              ↓
                    Django @jwt_required
                              ↓
                    Validate & Decode JWT
                              ↓
                      Access customer_id
                              ↓
                    Query MongoDB/Database
                              ↓
                      Return Protected Data
                              ↓
                   api.js ← HTTP Response
                              ↓
                        Vue Component
                              ↓
                        Display Data
```

---

## 🔑 Token Management

### Token Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                    Token Lifecycle                       │
└─────────────────────────────────────────────────────────┘

1. LOGIN/REGISTER
   ├─ User authenticates
   ├─ Backend generates JWT
   ├─ Token expires in: 60 minutes (configurable)
   └─ Frontend saves to localStorage

2. SUBSEQUENT REQUESTS
   ├─ api.js interceptor reads token
   ├─ Adds to Authorization header
   └─ Backend validates token

3. TOKEN EXPIRATION
   ├─ Backend checks 'exp' claim
   ├─ If expired → 401 Unauthorized
   └─ Frontend should redirect to login

4. LOGOUT
   ├─ Frontend clears localStorage
   └─ Token becomes invalid
```

### Token Structure (JWT)

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "customer_id": "CUST-00001",
    "username": "john_doe",
    "email": "john@example.com",
    "exp": 1696857600,
    "iat": 1696854000
  },
  "signature": "..."
}
```

---

## 🛠️ Configuration Points

### Frontend (frontend/src/services/api.js)
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
// Change for production: 'https://api.yourdomain.com/api'
```

### Backend (backend/posbackend/settings.py)
```python
# CORS - Allow frontend origin
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]

# JWT Settings
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60
JWT_SECRET_KEY = 'your-secret-key'

# MongoDB Connection
MONGODB_URI = 'mongodb+srv://...'
```

---

## ✅ Connection Checklist

- [x] Backend running on http://localhost:8000
- [x] Frontend running on http://localhost:8080
- [x] CORS configured correctly
- [x] MongoDB connection active
- [x] JWT token generation working
- [x] api.js configured with correct base URL
- [x] Components importing from '@/services/api'
- [x] Token saved to localStorage on login
- [x] Token attached to authenticated requests
- [x] Error handling in place

---

## 🐛 Debugging Tips

### Check if Backend is Running
```bash
curl http://localhost:8000/admin/
# Should return Django admin page
```

### Check API Endpoint
```bash
curl -X POST http://localhost:8000/api/auth/customer/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'
```

### Check CORS Headers
```bash
curl -H "Origin: http://localhost:8080" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:8000/api/auth/customer/login/ \
  -v
```

### Check Token in Browser
```javascript
// In browser console
console.log(localStorage.getItem('access_token'));
```

### Check Network Tab
1. Open DevTools → Network
2. Perform login
3. Check request headers for `Authorization: Bearer ...`
4. Check response status and data

---

**Need more details?** See `API_INTEGRATION_GUIDE.md` for comprehensive documentation.

