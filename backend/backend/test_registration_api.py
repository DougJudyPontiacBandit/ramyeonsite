#!/usr/bin/env python
"""
Test registration API endpoint directly
"""
import os
import sys
import django
from pathlib import Path
import requests
import json

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
django.setup()

def test_registration_api():
    """Test the registration API endpoint"""
    try:
        # Test data
        registration_data = {
            "email": "freshuser@example.com",
            "password": "testpass123",
            "first_name": "Fresh",
            "last_name": "User",
            "full_name": "Fresh User",
            "username": "freshuser"
        }
        
        print("🔍 Testing Registration API...")
        print(f"📝 Registration data: {registration_data}")
        
        # Make API call
        url = "http://localhost:8000/api/v1/auth/register/"
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"🌐 Making request to: {url}")
        
        response = requests.post(url, json=registration_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"📋 Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📋 Response Text: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Django server not running on port 8000")
        print("💡 Make sure to start Django server with: python manage.py runserver --settings=settings.local")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_login_api():
    """Test the login API endpoint"""
    try:
        login_data = {
            "email": "freshuser@example.com",
            "password": "testpass123"
        }
        
        print("\n🔍 Testing Login API...")
        print(f"📝 Login data: {login_data}")
        
        url = "http://localhost:8000/api/v1/auth/login/"
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=login_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"📋 Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📋 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Registration and Login APIs...")
    print("=" * 60)
    
    # Test registration
    reg_success = test_registration_api()
    
    if reg_success:
        # Test login
        test_login_api()
    
    print("=" * 60)
    print("🏁 API testing completed!")
