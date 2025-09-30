#!/usr/bin/env python
"""
Complete authentication test with known credentials
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

def test_complete_auth_flow():
    """Test complete authentication flow with known credentials"""
    try:
        # Step 1: Create a test user with known password
        logger.info("📝 Step 1: Creating test user...")
        
        user_service = UserService()
        test_user_data = {
            "username": "authtest",
            "email": "authtest@example.com",
            "password": "testpass123",
            "full_name": "Auth Test User",
            "role": "customer"
        }
        
        # Check if user already exists
        db = db_manager.get_database()
        existing_user = db.users.find_one({"email": test_user_data["email"]})
        if existing_user:
            logger.info("⚠️  Test user already exists, deleting...")
            db.users.delete_one({"email": test_user_data["email"]})
        
        # Create new user
        new_user = user_service.create_user(test_user_data, None)
        logger.info(f"✅ User created: {new_user['_id']}")
        
        # Step 2: Test login with known credentials
        logger.info("\n🔐 Step 2: Testing login...")
        
        auth_service = AuthService()
        login_result = auth_service.login(test_user_data["email"], test_user_data["password"])
        
        if login_result.get('access_token'):
            logger.info("✅ Login successful!")
            logger.info(f"   User ID: {login_result['user']['id']}")
            logger.info(f"   Email: {login_result['user']['email']}")
            logger.info(f"   Role: {login_result['user']['role']}")
            logger.info(f"   Token: {login_result['access_token'][:30]}...")
            
            # Step 3: Test token verification
            logger.info("\n🔍 Step 3: Testing token verification...")
            
            token = login_result['access_token']
            current_user = auth_service.get_current_user(token)
            
            if current_user:
                logger.info("✅ Token verification successful!")
                logger.info(f"   Current user: {current_user['user_id']}")
                logger.info(f"   Email: {current_user['email']}")
            else:
                logger.error("❌ Token verification failed")
                return False
            
            # Step 4: Test logout
            logger.info("\n🚪 Step 4: Testing logout...")
            
            logout_result = auth_service.logout(token)
            if logout_result.get('message'):
                logger.info("✅ Logout successful!")
            else:
                logger.error("❌ Logout failed")
                return False
            
            logger.info("\n🎉 Complete authentication flow test PASSED!")
            return True
        else:
            logger.error("❌ Login failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Authentication test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Complete Authentication Flow...")
    print("=" * 60)
    
    success = test_complete_auth_flow()
    
    if success:
        print("\n✅ All authentication tests PASSED!")
        print("Your MongoDB Atlas authentication is working correctly.")
    else:
        print("\n❌ Authentication tests FAILED!")
        print("There are issues with the authentication system.")
    
    print("=" * 60)

