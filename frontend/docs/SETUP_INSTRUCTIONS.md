# 🚀 Setup Instructions - Enhanced Backend

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- MongoDB Atlas account (free tier works)
- Git

---

## Step 1: Clone & Navigate

```bash
cd backend
```

---

## Step 2: Create Virtual Environment

### Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**
- Django 5.2.1
- Django REST Framework
- MongoDB Engine
- PyJWT (authentication)
- bcrypt (password hashing)
- QR Code libraries
- And more...

---

## Step 4: Configure Environment

Create `.env` file in `backend/` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ramyeon_db?retryWrites=true&w=majority
MONGODB_DATABASE=ramyeon_db

# CORS for Frontend
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend URL
FRONTEND_URL=http://localhost:8080
```

**Important:** Replace MongoDB credentials with your own!

---

## Step 5: Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying api.0001_initial... OK
  Applying api.0002_add_qr_code_fields... OK
  ...
```

---

## Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

**Enter:**
- Username: `admin`
- Email: `admin@ramyeon.com`
- Password: (your choice, e.g., `Admin123!`)

---

## Step 7: Generate QR Codes for Existing Users (if any)

```bash
python manage.py shell
```

Then run:
```python
from backend.api.models import User, Promotion
import uuid
import hashlib

# Generate QR codes for users without one
for user in User.objects.filter(qr_code__isnull=True):
    unique_string = f"USER-{user.username}-{uuid.uuid4().hex[:8]}"
    user.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
    user.save()
    print(f"✅ Generated QR for {user.username}: {user.qr_code}")

# Generate QR codes for promotions without one
for promo in Promotion.objects.filter(qr_code__isnull=True):
    unique_string = f"PROMO-{promo.title}-{uuid.uuid4().hex[:8]}"
    promo.qr_code = hashlib.sha256(unique_string.encode()).hexdigest()[:32].upper()
    promo.save()
    print(f"✅ Generated QR for promotion: {promo.title}")

# Exit shell
exit()
```

---

## Step 8: Create Sample Data (Optional but Recommended)

```bash
python manage.py shell
```

```python
from backend.api.models import Category, Product, Promotion, LoyaltyReward
from django.utils import timezone
from datetime import timedelta

# Create categories
noodle_cat = Category.objects.create(
    name="Noodles",
    description="Korean instant noodles",
    is_active=True
)

snack_cat = Category.objects.create(
    name="Snacks",
    description="Korean snacks and side dishes",
    is_active=True
)

# Create products
Product.objects.create(
    name="Shin Ramyun",
    description="Spicy Korean instant noodles",
    category=noodle_cat,
    price=150.00,
    stock_quantity=100,
    is_available=True,
    is_featured=True
)

Product.objects.create(
    name="Samyang Hot Chicken",
    description="Very spicy chicken flavored ramen",
    category=noodle_cat,
    price=180.00,
    stock_quantity=50,
    is_available=True,
    is_featured=True
)

Product.objects.create(
    name="Tteokbokki",
    description="Spicy rice cakes",
    category=snack_cat,
    price=200.00,
    stock_quantity=75,
    is_available=True,
    is_featured=False
)

# Create promotions
Promotion.objects.create(
    title="Weekend Special",
    description="20% off all noodles + 100 bonus points",
    discount_percentage=20.00,
    category=noodle_cat,
    points_reward=100,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=30),
    is_active=True
)

Promotion.objects.create(
    title="Buy 2 Get Points",
    description="Buy any 2 items and get 50 bonus points",
    discount_percentage=0,
    points_reward=50,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=60),
    is_active=True
)

# Create loyalty rewards
LoyaltyReward.objects.create(
    name="₱50 Discount Voucher",
    description="Get ₱50 off your next order",
    points_required=250,
    discount_type="fixed",
    discount_value=50.00,
    stock_quantity=0,  # Unlimited
    is_active=True,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=365)
)

LoyaltyReward.objects.create(
    name="₱100 Discount Voucher",
    description="Get ₱100 off your next order",
    points_required=500,
    discount_type="fixed",
    discount_value=100.00,
    stock_quantity=0,  # Unlimited
    is_active=True,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=365)
)

LoyaltyReward.objects.create(
    name="20% Off Your Order",
    description="Get 20% discount on your entire order",
    points_required=750,
    discount_type="percentage",
    discount_value=20.00,
    stock_quantity=100,  # Limited
    is_active=True,
    valid_from=timezone.now(),
    valid_until=timezone.now() + timedelta(days=365)
)

print("✅ Sample data created successfully!")
exit()
```

---

## Step 9: Run Development Server

```bash
python manage.py runserver
```

**Server will start at:**
```
http://127.0.0.1:8000/
```

---

## Step 10: Verify Installation

### 1. Check Admin Panel
Visit: `http://localhost:8000/admin/`
- Login with superuser credentials
- Verify all models are visible

### 2. Check API Browsable Interface
Visit: `http://localhost:8000/api/`
- Should see API root with all endpoints

### 3. Test User Registration
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

**Expected response:**
```json
{
  "message": "User created successfully",
  "user": {
    "id": "...",
    "username": "testuser",
    "qr_code": "ABC123..." // ✅ QR code auto-generated!
  }
}
```

---

## 📁 Project Structure

```
backend/
├── backend/
│   ├── api/
│   │   ├── models.py          # ✅ Database models
│   │   ├── serializers.py     # ✅ API serializers
│   │   ├── views.py           # ✅ Main API views
│   │   ├── pos_views.py       # ✅ POS/Cashier views
│   │   ├── urls.py            # ✅ URL routing
│   │   ├── admin.py           # ✅ Admin panel config
│   │   └── mongodb_views.py   # ✅ MongoDB auth
│   ├── settings.py            # ✅ Django settings
│   └── urls.py                # ✅ Main URL config
├── manage.py                  # ✅ Django management
├── requirements.txt           # ✅ Dependencies
└── .env                       # ⚠️ Create this!
```

---

## 🔍 Troubleshooting

### Issue: "No module named 'mongoengine'"
**Solution:**
```bash
pip install mongoengine
```

### Issue: "MongoDB connection failed"
**Solution:**
- Check MongoDB URI in `.env`
- Verify MongoDB Atlas is accessible
- Check network/firewall settings

### Issue: "QR codes not showing in admin"
**Solution:**
```bash
python manage.py shell
from backend.api.models import User
for user in User.objects.all():
    user.save()  # Triggers QR code generation
```

### Issue: "CORS errors from frontend"
**Solution:**
- Verify `CORS_ALLOWED_ORIGINS` in `.env`
- Make sure frontend URL is included
- Check `corsheaders` is in `INSTALLED_APPS`

### Issue: "Migrations not applying"
**Solution:**
```bash
# Delete migration files (keep __init__.py)
# Then recreate
python manage.py makemigrations api
python manage.py migrate
```

---

## 🎯 Next Steps

1. **Test All Endpoints:**
   - Use Postman or the browsable API
   - Verify QR codes are generated
   - Test points system

2. **Configure Frontend:**
   - Update API base URL
   - Implement QR code display
   - Build POS interface

3. **Customize:**
   - Adjust points calculation (currently 1 point per ₱10)
   - Add more reward tiers
   - Create promotional campaigns

---

## 📞 Getting Help

1. Check Django logs in terminal
2. Visit admin panel for data inspection
3. Use Django shell for debugging:
   ```bash
   python manage.py shell
   ```

---

## ✅ Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] .env file created and configured
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Sample data loaded
- [ ] Server running successfully
- [ ] Admin panel accessible
- [ ] API endpoints responding
- [ ] QR codes generating for new users
- [ ] Points system working

---

**Setup complete! Your enhanced backend is ready! 🎉**
