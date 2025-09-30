#!/usr/bin/env python
"""
Debug AuthService password verification
"""
import os
import sys
import django
from pathlib import Path
import bcrypt

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
django.setup()

from app.database import db_manager
from app.services.user_service import UserService

def debug_password_flow():
    """Debug the complete password hashing and verification flow"""
    try:
        # Step 1: Create a user with known password
        print("🔧 Step 1: Creating user with known password...")
        
        user_service = UserService()
        test_password = "testpass123"
        
        # Hash password using UserService method
        hashed_password = user_service.hash_password(test_password)
        print(f"🔐 Hashed password: {hashed_password}")
        
        # Step 2: Test verification with UserService method
        print("\n🔧 Step 2: Testing verification with UserService...")
        user_verify_result = user_service.verify_password(test_password, hashed_password)
        print(f"✅ UserService verification: {user_verify_result}")
        
        # Step 3: Test verification with bcrypt directly
        print("\n🔧 Step 3: Testing verification with bcrypt directly...")
        bcrypt_result = bcrypt.checkpw(test_password.encode('utf-8'), hashed_password.encode('utf-8'))
        print(f"✅ Bcrypt direct verification: {bcrypt_result}")
        
        # Step 4: Test with AuthService method
        print("\n🔧 Step 4: Testing verification with AuthService...")
        from app.services.auth_services import AuthService
        auth_service = AuthService()
        auth_verify_result = auth_service.verify_password(test_password, hashed_password)
        print(f"✅ AuthService verification: {auth_verify_result}")
        
        # Step 5: Test with actual database user
        print("\n🔧 Step 5: Testing with actual database user...")
        db = db_manager.get_database()
        user = db.users.find_one({"email": "authtest@example.com"})
        if user:
            print(f"👤 Found user: {user['username']}")
            print(f"🔐 Stored hash: {user['password']}")
            
            # Test with stored hash
            stored_verify = auth_service.verify_password(test_password, user['password'])
            print(f"✅ AuthService with stored hash: {stored_verify}")
            
            # Test with UserService
            user_service_verify = user_service.verify_password(test_password, user['password'])
            print(f"✅ UserService with stored hash: {user_service_verify}")
        else:
            print("❌ User not found in database")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Debugging Password Verification Flow...")
    print("=" * 60)
    debug_password_flow()
    print("=" * 60)

