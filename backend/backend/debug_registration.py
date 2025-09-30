#!/usr/bin/env python
"""
Debug registration process step by step
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

from app.services.user_service import UserService
from app.services.auth_services import AuthService
from app.serializers import UserCreateSerializer

def debug_registration():
    """Debug registration process step by step"""
    try:
        print("🔍 Debugging Registration Process...")
        print("=" * 50)
        
        # Step 1: Test data
        test_data = {
            "email": "debugtest@example.com",
            "password": "debugpass123",
            "first_name": "Debug",
            "last_name": "Test",
            "full_name": "Debug Test User",
            "username": "debugtest"
        }
        
        print("📝 Step 1: Test data")
        print(f"   Data: {test_data}")
        
        # Step 2: Test serializer validation
        print("\n🔧 Step 2: Testing serializer validation...")
        serializer = UserCreateSerializer(data=test_data)
        if serializer.is_valid():
            print("✅ Serializer validation passed")
            validated_data = serializer.validated_data.copy()
            validated_data['role'] = 'customer'
            print(f"   Validated data: {validated_data}")
        else:
            print("❌ Serializer validation failed")
            print(f"   Errors: {serializer.errors}")
            return False
        
        # Step 3: Test user creation
        print("\n🔧 Step 3: Testing user creation...")
        user_service = UserService()
        
        # Check if user already exists
        from app.database import db_manager
        db = db_manager.get_database()
        existing_user = db.users.find_one({"email": test_data["email"]})
        if existing_user:
            print("⚠️  User already exists, deleting...")
            db.users.delete_one({"email": test_data["email"]})
        
        try:
            new_user = user_service.create_user(validated_data, None)
            print("✅ User creation successful")
            print(f"   User ID: {new_user.get('_id')}")
            print(f"   Email: {new_user.get('email')}")
            print(f"   Username: {new_user.get('username')}")
            print(f"   Role: {new_user.get('role')}")
        except Exception as create_error:
            print(f"❌ User creation failed: {create_error}")
            return False
        
        # Step 4: Test login
        print("\n🔧 Step 4: Testing login...")
        auth_service = AuthService()
        try:
            login_result = auth_service.login(test_data['email'], test_data['password'])
            if login_result.get('success'):
                print("✅ Login successful")
                print(f"   Token: {login_result.get('access_token', 'N/A')[:30]}...")
                print(f"   User: {login_result.get('user', {}).get('id', 'N/A')}")
            else:
                print("❌ Login failed - no success flag")
                print(f"   Result: {login_result}")
        except Exception as login_error:
            print(f"❌ Login failed: {login_error}")
            return False
        
        print("\n🎉 Registration process completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_registration()

