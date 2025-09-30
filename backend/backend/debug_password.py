#!/usr/bin/env python
"""
Debug password hashing and verification
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

def test_password_verification():
    """Test password verification with existing users"""
    try:
        db = db_manager.get_database()
        if db is None:
            print("❌ Database connection failed")
            return
        
        # Get the test user
        user = db.users.find_one({"email": "test@example.com"})
        if not user:
            print("❌ User not found")
            return
        
        print(f"👤 User: {user['username']} ({user['email']})")
        print(f"🔐 Password hash: {user['password']}")
        
        # Test different passwords
        test_passwords = [
            "password123",
            "password",
            "test123",
            "admin123",
            "testuser",
            "123456"
        ]
        
        for password in test_passwords:
            try:
                result = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
                print(f"🔍 Testing '{password}': {'✅ MATCH' if result else '❌ No match'}")
                if result:
                    print(f"🎉 Found correct password: '{password}'")
                    return password
            except Exception as e:
                print(f"🔍 Testing '{password}': ❌ Error - {e}")
        
        print("❌ No matching password found")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Debugging Password Verification...")
    print("=" * 50)
    test_password_verification()

