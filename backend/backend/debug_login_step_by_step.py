#!/usr/bin/env python
"""
Debug login process step by step
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

def debug_login_step_by_step():
    """Debug the login process step by step"""
    try:
        auth_service = AuthService()
        email = "authtest@example.com"
        password = "testpass123"
        
        print(f"🔍 Debugging login for: {email}")
        print("=" * 50)
        
        # Step 1: Find user by email
        print("🔧 Step 1: Finding user by email...")
        user = auth_service.user_collection.find_one({"email": email})
        if not user:
            print("❌ User not found")
            return False
        
        print(f"✅ User found: {user['username']} (ID: {user['_id']})")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user['role']}")
        print(f"   Status: {user['status']}")
        print(f"   Password hash: {user['password'][:30]}...")
        
        # Step 2: Check password verification
        print("\n🔧 Step 2: Verifying password...")
        password_valid = auth_service.verify_password(password, user["password"])
        print(f"✅ Password verification: {password_valid}")
        
        if not password_valid:
            print("❌ Password verification failed")
            return False
        
        # Step 3: Check user status
        print("\n🔧 Step 3: Checking user status...")
        user_status = user.get("status", "active")
        print(f"   Status: {user_status}")
        
        if user_status != "active":
            print(f"❌ User status is not active: {user_status}")
            return False
        
        # Step 4: Check user role
        print("\n🔧 Step 4: Checking user role...")
        user_role = user.get("role", "").lower()
        print(f"   Role: {user_role}")
        
        allowed_roles = ["admin", "user", "customer", "employee"]
        if user_role not in allowed_roles:
            print(f"❌ Invalid user role: {user_role}")
            return False
        
        print("✅ All checks passed!")
        
        # Step 5: Try to create tokens
        print("\n🔧 Step 5: Creating tokens...")
        try:
            user_id = user["_id"]
            token_data = {"sub": user_id, "email": user["email"], "role": user["role"]}
            access_token = auth_service.create_access_token(token_data)
            refresh_token = auth_service.create_refresh_token(token_data)
            
            print(f"✅ Access token created: {access_token[:30]}...")
            print(f"✅ Refresh token created: {refresh_token[:30]}...")
            
            # Step 6: Test token verification
            print("\n🔧 Step 6: Testing token verification...")
            current_user = auth_service.get_current_user(access_token)
            if current_user:
                print(f"✅ Token verification successful: {current_user['user_id']}")
            else:
                print("❌ Token verification failed")
                return False
            
            print("\n🎉 Complete login flow successful!")
            return True
            
        except Exception as token_error:
            print(f"❌ Token creation failed: {token_error}")
            return False
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debugging Login Process Step by Step...")
    print("=" * 60)
    debug_login_step_by_step()
    print("=" * 60)

