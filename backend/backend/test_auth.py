#!/usr/bin/env python
"""
Test script to debug authentication issues
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
django.setup()

from app.database import db_manager
from app.services.auth_services import AuthService
from app.services.user_service import UserService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_users():
    """Check what users exist in the database"""
    try:
        db = db_manager.get_database()
        if db is None:
            logger.error("Failed to connect to database")
            return False
        
        logger.info("🔍 Checking existing users in database...")
        
        # Get all users
        users = list(db.users.find({}))
        logger.info(f"📊 Total users found: {len(users)}")
        
        for i, user in enumerate(users[:5]):  # Show first 5 users
            logger.info(f"👤 User {i+1}:")
            logger.info(f"   ID: {user.get('_id', 'N/A')}")
            logger.info(f"   Username: {user.get('username', 'N/A')}")
            logger.info(f"   Email: {user.get('email', 'N/A')}")
            logger.info(f"   Role: {user.get('role', 'N/A')}")
            logger.info(f"   Status: {user.get('status', 'N/A')}")
            logger.info(f"   Password hash: {user.get('password', 'N/A')[:20]}...")
            logger.info(f"   Created: {user.get('date_created', 'N/A')}")
            logger.info("")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error checking users: {e}")
        return False

def test_login():
    """Test login with existing user"""
    try:
        auth_service = AuthService()
        
        # Try to login with the test user we saw in the database
        logger.info("🔐 Testing login with testuser...")
        
        result = auth_service.login("test@example.com", "password123")
        
        if result.get('access_token'):
            logger.info("✅ Login successful!")
            logger.info(f"   Token: {result['access_token'][:20]}...")
            logger.info(f"   User: {result['user']}")
            return True
        else:
            logger.error("❌ Login failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Login test failed: {e}")
        return False

def test_registration():
    """Test user registration"""
    try:
        user_service = UserService()
        
        # Test data for registration
        test_user_data = {
            "username": "testuser_new",
            "email": "testnew@example.com",
            "password": "password123",
            "full_name": "Test User New",
            "role": "customer"
        }
        
        logger.info("📝 Testing user registration...")
        
        # Check if user already exists
        db = db_manager.get_database()
        existing_user = db.users.find_one({"email": test_user_data["email"]})
        if existing_user:
            logger.info("⚠️  User already exists, skipping registration test")
            return True
        
        # Create user
        new_user = user_service.create_user(test_user_data, None)
        
        if new_user:
            logger.info("✅ Registration successful!")
            logger.info(f"   New user ID: {new_user.get('_id')}")
            logger.info(f"   Email: {new_user.get('email')}")
            return True
        else:
            logger.error("❌ Registration failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Registration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Authentication System...")
    print("=" * 50)
    
    # Test database connection and users
    if test_database_users():
        print("\n" + "=" * 50)
        
        # Test login
        test_login()
        
        print("\n" + "=" * 50)
        
        # Test registration
        test_registration()
    
    print("\n" + "=" * 50)
    print("🏁 Authentication testing completed!")

