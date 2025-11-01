"""
Order Status Tracking - Test Script

This script tests the complete order status tracking functionality.
It simulates a POS staff member updating order status and a customer viewing updates.

Prerequisites:
1. Backend server running on http://localhost:8000
2. Valid JWT tokens for admin and customer
3. MongoDB connected

Usage:
    python test_order_status.py
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

# You need to set these tokens from your actual system
ADMIN_TOKEN = "YOUR_ADMIN_JWT_TOKEN_HERE"  # Get from POS login
CUSTOMER_TOKEN = "YOUR_CUSTOMER_JWT_TOKEN_HERE"  # Get from customer login

# Test order ID (you'll need an actual order ID)
TEST_ORDER_ID = "ONLINE-000001"  # Replace with real order ID


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response, title="Response"):
    """Pretty print API response."""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_update_status(order_id, status, notes="", token=ADMIN_TOKEN):
    """Test updating order status (POS staff)."""
    url = f"{BASE_URL}/online/orders/{order_id}/update-status/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "status": status,
        "notes": notes
    }
    
    print(f"\n🔄 Updating order to: {status}")
    if notes:
        print(f"   Notes: {notes}")
    
    response = requests.post(url, headers=headers, json=data)
    print_response(response, f"Update to {status}")
    
    return response.status_code == 200


def test_get_status(order_id, token=CUSTOMER_TOKEN):
    """Test getting order status (Customer)."""
    url = f"{BASE_URL}/online/orders/{order_id}/status/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📊 Fetching order status...")
    
    response = requests.get(url, headers=headers)
    print_response(response, "Current Status")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            status_info = data['data']['status_info']
            print(f"\n   {status_info['icon']} {status_info['label']}")
            print(f"   {status_info['description']}")
            print(f"   Progress: {status_info['progress']}%")
            
            # Print history
            history = data['data'].get('status_history', [])
            if history:
                print("\n   📜 Status History:")
                for entry in history:
                    timestamp = entry['timestamp']
                    print(f"      • {entry['status']} - {timestamp}")
                    if entry.get('notes'):
                        print(f"        Notes: {entry['notes']}")
    
    return response.status_code == 200


def test_get_order_history(token=CUSTOMER_TOKEN):
    """Test getting order history with status info."""
    url = f"{BASE_URL}/online/orders/history/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n📚 Fetching order history...")
    
    response = requests.get(url, headers=headers)
    print_response(response, "Order History")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            orders = data['results']
            print(f"\n   Found {len(orders)} orders:")
            for order in orders[:3]:  # Show first 3
                status_info = order.get('status_info', {})
                print(f"\n   Order: {order['order_id']}")
                print(f"   Status: {status_info.get('icon')} {status_info.get('label')}")
                print(f"   Progress: {status_info.get('progress')}%")
    
    return response.status_code == 200


def test_complete_workflow(order_id):
    """Test complete order status workflow."""
    print_section("COMPLETE ORDER STATUS WORKFLOW TEST")
    
    statuses = [
        ("confirmed", "Order confirmed by cashier"),
        ("preparing", "Gathering ingredients"),
        ("cooking", "Chef is preparing your ramen"),
        ("ready", "Your order is ready for pickup!"),
        ("out_for_delivery", "Driver John is on the way"),
        ("delivered", "Order delivered successfully"),
        ("completed", "Transaction completed")
    ]
    
    for status, notes in statuses:
        # POS updates status
        print_section(f"Step: {status.upper()}")
        success = test_update_status(order_id, status, notes)
        
        if not success:
            print(f"❌ Failed to update to {status}")
            return False
        
        # Wait a bit
        time.sleep(1)
        
        # Customer checks status
        test_get_status(order_id)
        
        # Wait before next update
        print("\n⏳ Waiting 2 seconds before next update...")
        time.sleep(2)
    
    return True


def test_security():
    """Test security features."""
    print_section("SECURITY TESTS")
    
    # Test 1: Customer tries to update status (should fail)
    print("\n🔒 Test: Customer trying to update status")
    url = f"{BASE_URL}/online/orders/{TEST_ORDER_ID}/update-status/"
    headers = {
        "Authorization": f"Bearer {CUSTOMER_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"status": "cooking"}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 403:
        print("✅ PASS: Customer correctly denied (403 Forbidden)")
    else:
        print(f"❌ FAIL: Expected 403, got {response.status_code}")
    
    # Test 2: Invalid status
    print("\n🔒 Test: Invalid status code")
    headers["Authorization"] = f"Bearer {ADMIN_TOKEN}"
    data = {"status": "invalid_status"}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 400:
        print("✅ PASS: Invalid status correctly rejected (400 Bad Request)")
    else:
        print(f"❌ FAIL: Expected 400, got {response.status_code}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("  ORDER STATUS TRACKING - TEST SUITE")
    print("=" * 60)
    print(f"\nTest Configuration:")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Order ID: {TEST_ORDER_ID}")
    print(f"  Admin Token: {'Set' if ADMIN_TOKEN != 'YOUR_ADMIN_JWT_TOKEN_HERE' else 'NOT SET'}")
    print(f"  Customer Token: {'Set' if CUSTOMER_TOKEN != 'YOUR_CUSTOMER_JWT_TOKEN_HERE' else 'NOT SET'}")
    
    if ADMIN_TOKEN == "YOUR_ADMIN_JWT_TOKEN_HERE" or CUSTOMER_TOKEN == "YOUR_CUSTOMER_JWT_TOKEN_HERE":
        print("\n❌ ERROR: Please set ADMIN_TOKEN and CUSTOMER_TOKEN in the script")
        print("\nHow to get tokens:")
        print("  1. Login to POS as admin → Copy JWT token")
        print("  2. Login to customer site → Copy JWT token")
        print("  3. Update tokens in this script")
        return
    
    # Run tests
    print_section("TEST 1: Get Order Status (Customer)")
    test_get_status(TEST_ORDER_ID)
    
    print_section("TEST 2: Update Order Status (POS)")
    test_update_status(TEST_ORDER_ID, "cooking", "Starting to cook now")
    
    print_section("TEST 3: Verify Update (Customer)")
    test_get_status(TEST_ORDER_ID)
    
    print_section("TEST 4: Get Order History")
    test_get_order_history()
    
    print_section("TEST 5: Security Tests")
    test_security()
    
    # Optional: Full workflow test
    print("\n" + "=" * 60)
    response = input("\nRun complete workflow test? (y/n): ")
    if response.lower() == 'y':
        test_complete_workflow(TEST_ORDER_ID)
    
    print("\n" + "=" * 60)
    print("  TEST SUITE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()




