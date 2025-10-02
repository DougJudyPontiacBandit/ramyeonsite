# MongoDB Atlas Setup Guide

## Why You Have 2 .env Files

You have **two different files** for environment variables:

1. **`.env`** - Your **actual environment file** with real credentials (DO NOT commit to git)
   - Contains your real MongoDB Atlas URI
   - Has your actual secret keys
   - Used by the application

2. **`.env.example`** - A **template file** showing what variables are needed (safe to commit)
   - Contains placeholder values
   - Shows other developers what they need to configure
   - Doesn't contain real credentials

**The `.env` file is in `.gitignore` so your credentials stay private!**

## Current MongoDB Configuration

Your `.env` file is now configured with:

```env
# MongoDB Atlas (Your Cloud Database)
MONGODB_URI=mongodb+srv://admin:ISZxn6AfY8wLSz2O@cluster0.qumhbyz.mongodb.net/pos_system?retryWrites=true&w=majority
MONGODB_DATABASE=pos_system

# Django Settings
SECRET_KEY=django-insecure-ramyeon-corner-secret-key-change-in-production-2025
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS for Vue.js
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# JWT Authentication
JWT_SECRET_KEY=ramyeon-jwt-secret-key-2025
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend
FRONTEND_URL=http://localhost:8080
```

## MongoDB Atlas Connection Details

- **Cluster:** cluster0.qumhbyz.mongodb.net
- **Database:** pos_system
- **Username:** admin
- **Password:** ISZxn6AfY8wLSz2O

## Setup Steps

### 1. Install Djongo (Django-MongoDB Connector)

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install djongo==1.3.6
```

### 2. Verify MongoDB Connection

The Django settings are now configured to use MongoDB Atlas:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'pos_system',
        'CLIENT': {
            'host': 'mongodb+srv://admin:ISZxn6AfY8wLSz2O@cluster0...'
        }
    }
}
```

### 3. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```powershell
python manage.py createsuperuser
```

### 5. Run Server

```powershell
python manage.py runserver
```

## MongoDB Atlas Features

✅ **Cloud Database** - Your data is stored securely in MongoDB Atlas  
✅ **Automatic Backups** - MongoDB Atlas handles backups  
✅ **Scalable** - Easy to scale as your app grows  
✅ **Global Distribution** - Can deploy in multiple regions  

## MongoDB Collections

With MongoDB, your Django models will be stored as collections:

- `users` - User accounts
- `categories` - Product categories  
- `products` - Menu items
- `vouchers` - Discount coupons
- `user_vouchers` - Claimed vouchers
- `promotions` - Special promotions
- `carts` - Shopping carts
- `cart_items` - Cart items
- `orders` - Customer orders
- `order_items` - Order items
- `newsletter_subscriptions` - Email subscriptions
- `contact_messages` - Contact form messages

## Important Security Notes

### ⚠️ NEVER Commit .env to Git

Your `.env` file contains sensitive credentials. It's already in `.gitignore`:

```gitignore
# Environment variables
.env
.env.local
```

### ✅ Share .env.example Instead

When sharing code, provide `.env.example` so others know what to configure:

```bash
# Other developers copy the example
cp .env.example .env

# Then they add their own credentials
```

### 🔒 Production Security

For production, make sure to:

1. **Change SECRET_KEY** to a strong random value
2. **Set DEBUG=False**
3. **Update ALLOWED_HOSTS** to your domain
4. **Use environment-specific .env files**
5. **Enable MongoDB Atlas IP whitelist**
6. **Use strong passwords**

## Testing MongoDB Connection

You can test the connection with a simple script:

```python
# test_mongo.py
from pymongo import MongoClient
import os
from decouple import config

uri = config('MONGODB_URI')
client = MongoClient(uri)

try:
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    
    # List databases
    print("\nDatabases:", client.list_database_names())
    
except Exception as e:
    print(f"❌ Error: {e}")
```

Run it:
```powershell
python test_mongo.py
```

## Troubleshooting

### Issue: "No module named 'djongo'"

**Solution:**
```powershell
pip install djongo==1.3.6
```

### Issue: Connection timeout

**Solutions:**
1. Check your MongoDB Atlas IP whitelist (add 0.0.0.0/0 for testing)
2. Verify your internet connection
3. Check if the cluster is active in MongoDB Atlas

### Issue: Authentication failed

**Solutions:**
1. Verify username/password in `.env`
2. Check MongoDB Atlas user permissions
3. Ensure database name is correct

## MongoDB Atlas Dashboard

Access your database at: https://cloud.mongodb.com

1. View collections and data
2. Monitor performance
3. Configure backups
4. Manage users and security
5. Check metrics and logs

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `MONGODB_URI` | Connection string to MongoDB Atlas | `mongodb+srv://user:pass@cluster...` |
| `MONGODB_DATABASE` | Database name | `pos_system` |
| `SECRET_KEY` | Django secret key | Random string |
| `DEBUG` | Enable debug mode | `True` for dev, `False` for prod |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs | `http://localhost:8080` |
| `JWT_SECRET_KEY` | JWT token signing key | Random string |

## Next Steps

1. ✅ Install djongo: `pip install djongo==1.3.6`
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Create superuser: `python manage.py createsuperuser`
4. ✅ Start server: `python manage.py runserver`
5. ✅ Test API endpoints at `http://localhost:8000/api/`

Your backend is now connected to **MongoDB Atlas in the cloud**! 🚀
