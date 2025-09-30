#!/usr/bin/env python
"""
Simple authentication test
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

def simple_test():
    """Simple test with existing user"""
    try:
        auth_service = AuthService()
        
        # Use the existing testuser from the database
        email = "test@example.com"
        password = "password123"  # Try common passwords
        
        print(f"🔍 Testing login with: {email}")
        
        # First, let's see what users we have
        db = db_manager.get_database()
        users = list(db.users.find({}, {"username": 1, "email": 1, "role": 1}))
        print(f"📊 Available users: {len(users)}")
        for user in users[:3]:
            print(f"   - {user.get('username', 'N/A')} ({user.get('email', 'N/A')}) - {user.get('role', 'N/A')}")
        
        # Try to login
        try:
            result = auth_service.login(email, password)
            print(f"✅ Login successful!")
            print(f"   User: {result.get('user', {}).get('id', 'N/A')}")
            print(f"   Token: {result.get('access_token', 'N/A')[:30]}...")
            return True
        except Exception as login_error:
            print(f"❌ Login failed: {login_error}")
            
            # Let's try to create a completely new user
            print("\n🔧 Creating a fresh test user...")
            from app.services.user_service import UserService
            user_service = UserService()
            
            # Delete any existing test user
            db.users.delete_many({"email": "simpletest@example.com"})
            
            # Create new user
            new_user_data = {
                "username": "simpletest",
                "email": "simpletest@example.com", 
                "password": "simplepass123",
                "full_name": "Simple Test User",
                "role": "customer"
            }
            
            new_user = user_service.create_user(new_user_data, None)
            print(f"✅ New user created: {new_user['_id']}")
            
            # Try login with new user
            print("🔐 Testing login with new user...")
            login_result = auth_service.login("simpletest@example.com", "simplepass123")
            print(f"✅ New user login successful!")
            print(f"   User: {login_result.get('user', {}).get('id', 'N/A')}")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Simple Authentication Test...")
    print("=" * 50)
    simple_test()
    print("=" * 50)

