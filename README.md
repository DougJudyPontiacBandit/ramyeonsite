# Ramyeon Site - POS System

A comprehensive Point of Sale (POS) system for a ramyeon (Korean instant noodle) restaurant, featuring customer ordering, admin management, and backend API services.

## Project Description

This is a full-stack web application built with Vue.js 3 (frontend), Django REST Framework (backend), and MongoDB (database). It provides a complete POS solution with customer ordering interface, admin dashboard for restaurant management, and robust backend APIs.

## Tech Stack

### Customer Frontend
- **Framework:** Vue.js 3.2.13
- **Styling:** Tailwind CSS 4.1.13
- **Build Tool:** Vue CLI 5.0.0
- **QR Code Generation:** qrcode 1.5.4
- **AI Integration:** Anthropic AI SDK 0.61.0
- **HTTP Client:** Axios 1.12.2

### Backend API
- **Framework:** Django 5.2.1 + Django REST Framework 3.16.0
- **Database:** MongoDB Atlas (cloud) with local fallback
- **MongoDB Driver:** PyMongo 4.13.0
- **Authentication:** JWT tokens with bcrypt 4.3.0
- **CORS:** django-cors-headers 4.7.0
- **Environment:** python-decouple 3.8

### Admin Frontend
- **Framework:** Vue.js 3.5.13
- **Build Tool:** Vite 6.2.4
- **Charts:** Chart.js 4.5.0 + vue-chartjs 5.3.2
- **State Management:** Pinia 3.0.1
- **Routing:** Vue Router 4.5.0
- **UI Components:** Bootstrap 5.3.7

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **RAM:** 8GB (16GB recommended for development)
- **Storage:** 5GB free space
- **Internet:** Stable connection for MongoDB Atlas

### Required Software

#### 1. Node.js and npm
- **Node.js:** Version 18.0.0 or higher
- **npm:** Version 8.0.0 or higher (comes with Node.js)
- **Download:** [Node.js Official Website](https://nodejs.org/)

#### 2. Python
- **Python:** Version 3.9 or higher (3.11+ recommended)
- **pip:** Latest version
- **Download:** [Python Official Website](https://python.org/)

#### 3. Git
- **Git:** Latest version
- **Download:** [Git Official Website](https://git-scm.com/)

#### 4. MongoDB (Choose one)
- **MongoDB Atlas (Recommended):** Cloud-hosted database
- **MongoDB Community Edition:** Local installation
- **Download:** [MongoDB Official Website](https://www.mongodb.com/try/download/community)

#### 5. Code Editor (Optional but recommended)
- **Visual Studio Code:** [Download here](https://code.visualstudio.com/)
- **Extensions:** Python, Vue.js, MongoDB

## Installation & Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd ramyeonsite

# Verify you're in the correct directory
ls -la  # Should show package.json, src/, backend/, etc.
```

### Step 2: Customer Frontend Setup

```bash
# Install Node.js dependencies (this may take 2-3 minutes)
npm install

# Verify installation
npm list --depth=0

# Environment setup (optional but recommended)
# Create .env file for API endpoints
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run serve
# Frontend will be available at http://localhost:8080
```

**Expected Output:**
```
App running at:
- Local:   http://localhost:8080/
- Network: http://192.168.x.x:8080/
```

### Step 3: Backend API Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell/Command Prompt):
venv\Scripts\activate
# Windows (Git Bash):
source venv/Scripts/activate
# macOS/Linux:
source venv/bin/activate

# Verify virtual environment is active (should show (venv) in prompt)
which python  # Should point to venv/bin/python

# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install Python dependencies (this may take 3-5 minutes)
pip install -r requirements.txt

# Verify installation
pip list

# Database setup (see Database Configuration section below)

# Run Django migrations (if using SQLite fallback)
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start Django development server
python manage.py runserver
# Backend API will be available at http://localhost:8000
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Django version 5.2.1, using settings 'posbackend.settings.local'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 4: Admin Frontend Setup

```bash
# Navigate to admin frontend directory
cd backend/frontend

# Install Node.js dependencies
npm install

# Environment setup
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run dev
# Admin frontend will be available at http://localhost:5173
```

**Expected Output:**
```
VITE v6.2.4  ready in 500 ms
➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 5: Verify Installation

Open three terminal windows and run each service:

**Terminal 1 - Customer Frontend:**
```bash
npm run serve
```

**Terminal 2 - Backend API:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

**Terminal 3 - Admin Frontend:**
```bash
cd backend/frontend
npm run dev
```

**Test the installation:**
1. Visit http://localhost:8080 (Customer Frontend)
2. Visit http://localhost:8000/api/v1/ (Backend API)
3. Visit http://localhost:5173 (Admin Frontend)

## Database Configuration

### Option A: MongoDB Atlas (Recommended)

#### Step 1: Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Try Free" and sign up with your email
3. Choose "Shared" cluster (free tier)
4. Select a region close to your location
5. Create cluster (this may take 3-5 minutes)

#### Step 2: Configure Database Access
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create a username and strong password
5. Set privileges to "Read and write to any database"
6. Click "Add User"

#### Step 3: Configure Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Choose "Allow access from anywhere" (0.0.0.0/0) for development
4. Click "Confirm"

#### Step 4: Get Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

#### Step 5: Environment Variables
Create `.env` file in `backend/` directory:
```env
# Database Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/pos_system
MONGODB_DATABASE=pos_system

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
TIME_ZONE=Asia/Manila

# CORS Settings (for development)
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173
```

### Option B: Local MongoDB

#### Step 1: Install MongoDB Community Edition

**Windows:**
1. Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Choose "Complete" installation
4. Install MongoDB Compass (optional GUI)
5. Start MongoDB service: `net start MongoDB`

**macOS:**
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

**Ubuntu/Linux:**
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Step 2: Environment Variables
Create `.env` file in `backend/` directory:
```env
# Database Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=pos_system

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
TIME_ZONE=Asia/Manila

# CORS Settings (for development)
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173
```

### Step 3: Test Database Connection

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Test MongoDB connection
python manage.py shell
```

In the Django shell:
```python
from app.database import DatabaseManager
db_manager = DatabaseManager()
db_manager.connect_to_mongodb()
print("Database connected successfully!")
exit()
```

## Development Workflow

### Running All Services

**Option 1: Manual Setup (Recommended for Development)**
```bash
# Terminal 1: Customer Frontend
npm run serve

# Terminal 2: Backend API
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver

# Terminal 3: Admin Frontend
cd backend/frontend
npm run dev
```

**Option 2: Using npm scripts (if configured)**
```bash
# Run all services with one command (if package.json scripts are set up)
npm run dev:all
```

### Available Services
- **Customer Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000
- **Admin Frontend:** http://localhost:5173
- **API Documentation:** http://localhost:8000/api/v1/

### Development Commands

#### Customer Frontend
```bash
# Development server
npm run serve

# Build for production
npm run build

# Lint and fix code
npm run lint

# Run Claude AI script
npm run claude
```

#### Backend API
```bash
# Start development server
python manage.py runserver

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

#### Admin Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test:unit

# Lint code
npm run lint

# Format code
npm run format
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Node.js Issues

**Problem:** `npm install` fails with permission errors
```bash
# Solution: Fix npm permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
# Or use sudo (not recommended)
sudo npm install
```

**Problem:** `npm install` fails with network errors
```bash
# Solution: Clear npm cache and use different registry
npm cache clean --force
npm install --registry https://registry.npmjs.org/
```

**Problem:** Node.js version mismatch
```bash
# Check Node.js version
node --version

# Install Node Version Manager (nvm)
# Windows: Download from https://github.com/coreybutler/nvm-windows
# macOS/Linux:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18.0.0
nvm use 18.0.0
```

#### 2. Python Issues

**Problem:** `pip install` fails with permission errors
```bash
# Solution: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem:** Python version not found
```bash
# Check Python version
python --version
python3 --version

# Install Python 3.9+ if not available
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

**Problem:** Virtual environment not activating
```bash
# Windows PowerShell (if execution policy error):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Windows Command Prompt:
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

#### 3. MongoDB Issues

**Problem:** MongoDB connection failed
```bash
# Check if MongoDB is running
# Windows:
net start MongoDB

# macOS:
brew services start mongodb/brew/mongodb-community

# Ubuntu/Linux:
sudo systemctl start mongod
sudo systemctl status mongod
```

**Problem:** MongoDB Atlas connection timeout
```bash
# Check network access in MongoDB Atlas
# Ensure IP address is whitelisted
# Test connection string format
```

**Problem:** Database authentication failed
```bash
# Verify credentials in .env file
# Check username and password in MongoDB Atlas
# Ensure user has proper permissions
```

#### 4. Django Issues

**Problem:** `python manage.py runserver` fails
```bash
# Check if virtual environment is activated
which python  # Should show venv path

# Install missing dependencies
pip install -r requirements.txt

# Check Django version
python -m django --version
```

**Problem:** Database migration errors
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial

# Create new migrations
python manage.py makemigrations
python manage.py migrate
```

**Problem:** CORS errors in browser
```bash
# Check CORS settings in settings.py
# Ensure frontend URLs are in CORS_ALLOWED_ORIGINS
# Restart Django server after changes
```

#### 5. Vue.js Issues

**Problem:** `npm run serve` fails
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version compatibility
node --version  # Should be 18+
```

**Problem:** Build errors
```bash
# Check for syntax errors
npm run lint

# Clear cache
npm cache clean --force

# Update dependencies
npm update
```

**Problem:** Hot reload not working
```bash
# Check if ports are available
netstat -an | grep :8080
netstat -an | grep :5173

# Try different port
npm run serve -- --port 8081
```

### Performance Issues

#### 1. Slow npm install
```bash
# Use npm ci for faster installs
npm ci

# Use yarn instead of npm
npm install -g yarn
yarn install
```

#### 2. Slow Django startup
```bash
# Use development settings
export DJANGO_SETTINGS_MODULE=posbackend.settings.local

# Disable debug toolbar if installed
# Check for heavy imports in settings
```

#### 3. Memory issues
```bash
# Monitor memory usage
# Close unnecessary applications
# Use lighter development tools
```

### Debugging Tips

#### 1. Enable Debug Mode
```bash
# Backend: Set DEBUG=True in .env
# Frontend: Use Vue DevTools browser extension
```

#### 2. Check Logs
```bash
# Django logs: Check console output
# Browser logs: Open Developer Tools (F12)
# Network logs: Check Network tab in DevTools
```

#### 3. Database Debugging
```bash
# Connect to MongoDB directly
# Use MongoDB Compass for GUI
# Check database collections and documents
```

### Getting Help

1. **Check the logs** - Look for error messages in terminal output
2. **Verify installation** - Ensure all dependencies are installed correctly
3. **Check versions** - Ensure Node.js, Python, and MongoDB versions are compatible
4. **Restart services** - Sometimes a simple restart fixes issues
5. **Clear caches** - Clear npm cache, browser cache, and Django cache
6. **Check documentation** - Refer to official documentation for each technology
7. **Ask for help** - Contact the development team with specific error messages

## Project Structure

```
ramyeonsite/
├── public/                          # Customer frontend static assets
├── src/                             # Customer frontend source
│   ├── components/                  # Vue components (Menu, Cart, Auth, etc.)
│   ├── assets/                      # Images, styles, food photos
│   ├── App.vue                      # Root component
│   └── main.js                      # Application entry point
├── backend/                         # Backend services
│   ├── backend/                     # Django project
│   │   ├── posbackend/              # Django settings
│   │   ├── app/                     # Main Django app
│   │   │   ├── views.py             # API endpoints
│   │   │   ├── models.py            # Data models
│   │   │   ├── database.py          # MongoDB connection
│   │   │   └── kpi_views/           # Business logic views
│   │   ├── notifications/           # Notification system
│   │   ├── promotions/              # Promotion management
│   │   ├── reports/                 # Reporting system
│   │   └── requirements.txt         # Python dependencies
│   └── frontend/                    # Admin frontend
│       ├── src/                     # Admin Vue app
│       ├── public/
│       └── package.json
├── scripts/                         # Utility scripts
├── package.json                     # Customer frontend dependencies
└── README.md                        # This file
```

## Key Features

### Customer Frontend
- User authentication (Login/Signup)
- Interactive menu browsing with food items
- Shopping cart with persistent storage
- Promotions and voucher system
- QR code generation for orders
- Responsive design with dark mode
- Contact and about pages

### Backend API
- RESTful API endpoints
- JWT-based authentication
- MongoDB integration with fallback
- Customer management
- Order processing
- Inventory management
- Reporting and analytics

### Admin Frontend
- POS interface for order management
- Customer database management
- Sales reporting and analytics
- Inventory tracking
- Promotion management

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/logout/` - User logout

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}/` - Get user details
- `PUT /api/v1/users/{id}/` - Update user
- `DELETE /api/v1/users/{id}/` - Delete user

### Customers
- `GET /api/v1/customers/` - List customers
- `POST /api/v1/customers/` - Create customer

### Categories
- `GET /api/v1/categories/` - List menu categories
- `POST /api/v1/categories/` - Create category

### Cart & Orders
- `GET /api/v1/cart/` - Get user cart
- `POST /api/v1/cart/add/` - Add item to cart
- `POST /api/v1/orders/` - Create order

### Promotions
- `GET /api/v1/promotions/` - List active promotions
- `POST /api/v1/promotions/` - Create promotion

### Reports
- `GET /api/v1/reports/sales/` - Sales reports
- `GET /api/v1/reports/categories/` - Category reports

## Scripts

### Customer Frontend
- `npm run serve` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Lint and fix code
- `npm run claude` - Run Claude AI script

### Backend
- `python manage.py runserver` - Start Django server
- `python manage.py migrate` - Run database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py shell` - Django shell

### Admin Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Lint code

## Configuration

For detailed Vue CLI configuration options, see the [Configuration Reference](https://cli.vuejs.org/config/).

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

## License

This project is private and proprietary.
