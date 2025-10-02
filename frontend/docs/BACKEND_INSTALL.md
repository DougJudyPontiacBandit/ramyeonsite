# 🚀 Backend Installation Instructions

## Quick Setup for MongoDB Atlas

Your backend is configured to use **MongoDB Atlas** (cloud database).

### Step-by-Step Installation

#### 1. Open PowerShell in Backend Directory

```powershell
cd C:\Users\nemen\Documents\USC\2025\IT\Capstone\ramyeonsite\backend
```

#### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Install Required Packages

```powershell
pip install djongo==1.3.6
pip install PyJWT
```

Or install all at once:
```powershell
pip install -r requirements.txt
```

#### 4. Verify .env Configuration

Your `.env` file is already set up with MongoDB Atlas:

```env
MONGODB_URI=mongodb+srv://admin:ISZxn6AfY8wLSz2O@cluster0.qumhbyz.mongodb.net/pos_system?retryWrites=true&w=majority
MONGODB_DATABASE=pos_system
```

✅ This is correct! No changes needed.

#### 5. Run Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

This creates the collections in your MongoDB Atlas database.

#### 6. Create Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Follow the prompts:
- Username: (choose a username)
- Email: (your email)
- Password: (choose a secure password)

#### 7. Start Development Server

```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

#### 8. Test the API

Open your browser or use curl:

- **API Root:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Products:** http://localhost:8000/api/products/
- **Categories:** http://localhost:8000/api/categories/

## Environment Files Explained

### `.env` (Your Actual Credentials)
- Contains real MongoDB Atlas URI with password
- **NOT** committed to Git (in .gitignore)
- Used by the application

### `.env.example` (Template)
- Shows what variables are needed
- Safe to commit to Git
- For other developers

**You need BOTH files:**
1. `.env` - for running the app
2. `.env.example` - for documentation

## MongoDB Atlas Dashboard

Access your database online:
1. Go to https://cloud.mongodb.com
2. Login with your account
3. Select your cluster (cluster0)
4. Browse collections in the `pos_system` database

## Troubleshooting

### Issue: "No module named 'djongo'"
**Solution:**
```powershell
pip install djongo==1.3.6
```

### Issue: "No module named 'jwt'"
**Solution:**
```powershell
pip install PyJWT
```

### Issue: Can't connect to MongoDB
**Solutions:**
1. Check internet connection
2. Verify MongoDB Atlas cluster is running
3. Check IP whitelist in MongoDB Atlas (allow 0.0.0.0/0 for testing)
4. Verify credentials in `.env`

### Issue: Migration errors
**Solution:**
```powershell
python manage.py makemigrations --empty api
python manage.py migrate
```

## Database Collections

After migration, your MongoDB will have these collections:

- `users` - User accounts
- `categories` - Product categories
- `products` - Menu items
- `vouchers` - Discount coupons
- `user_vouchers` - Claimed vouchers
- `promotions` - Special offers
- `carts` - Shopping carts
- `cart_items` - Items in carts
- `orders` - Customer orders
- `order_items` - Items in orders
- `newsletter_subscriptions` - Newsletter emails
- `contact_messages` - Contact form messages

## Testing API Endpoints

### Using Browser
Visit: http://localhost:8000/api/

### Using curl (PowerShell)

```powershell
# Get all products
curl http://localhost:8000/api/products/

# Get all categories
curl http://localhost:8000/api/categories/

# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"TestPass123!\",\"password2\":\"TestPass123!\",\"first_name\":\"Test\",\"last_name\":\"User\"}'
```

## Next Steps

1. ✅ Install dependencies: `pip install djongo PyJWT`
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Create superuser: `python manage.py createsuperuser`
4. ✅ Start server: `python manage.py runserver`
5. 🔄 Connect Vue.js frontend to the API
6. 🔄 Add sample data via admin panel

## Quick Reference

| Command | Purpose |
|---------|---------|
| `.\venv\Scripts\Activate.ps1` | Activate virtual env |
| `pip install djongo` | Install MongoDB connector |
| `python manage.py migrate` | Setup database |
| `python manage.py createsuperuser` | Create admin |
| `python manage.py runserver` | Start server |
| `deactivate` | Deactivate virtual env |

**Your backend is ready to connect with MongoDB Atlas in the cloud! 🚀**
