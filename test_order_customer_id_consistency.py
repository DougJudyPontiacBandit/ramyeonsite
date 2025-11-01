#!/usr/bin/env python
"""
Test script to verify customer_id consistency between order creation and retrieval.
This script checks if orders are created and retrieved with the same customer_id.

Usage:
    python test_order_customer_id_consistency.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posbackend.settings')
django.setup()

from backend.app.database import db_manager
from datetime import datetime, timedelta


def test_customer_id_consistency():
    """Test that customer_id is consistent between creation and retrieval."""
    
    print("=" * 80)
    print("CUSTOMER ID CONSISTENCY TEST")
    print("=" * 80)
    print()
    
    # Get MongoDB database
    db = db_manager.get_database()
    online_transactions = db.online_transactions
    customers = db.customers
    
    # Get all unique customer IDs from database
    print("📊 CHECKING DATABASE...")
    print()
    
    # 1. Check customer records
    customer_list = list(customers.find())
    print(f"✅ Found {len(customer_list)} customer(s) in database:")
    for customer in customer_list:
        print(f"   - Customer ID: {customer['_id']}")
        print(f"     Email: {customer.get('email', 'N/A')}")
        print(f"     Name: {customer.get('full_name', 'N/A')}")
        print()
    
    # 2. Check order records
    order_list = list(online_transactions.find())
    print(f"✅ Found {len(order_list)} order(s) in database:")
    for order in order_list:
        print(f"   - Order ID: {order['_id']}")
        print(f"     Customer ID: {order.get('customer_id', 'N/A')}")
        print(f"     Created: {order.get('created_at', 'N/A')}")
        print(f"     Items: {len(order.get('items', []))}")
        print()
    
    # 3. Check for mismatches
    print("🔍 CHECKING FOR MISMATCHES...")
    print()
    
    customer_ids_in_customers = {c['_id'] for c in customer_list}
    customer_ids_in_orders = {o.get('customer_id') for o in order_list if o.get('customer_id')}
    
    # Find orders with customer_ids that don't exist in customers collection
    orphaned_orders = []
    for order in order_list:
        order_customer_id = order.get('customer_id')
        if order_customer_id and order_customer_id not in customer_ids_in_customers:
            orphaned_orders.append({
                'order_id': order['_id'],
                'customer_id': order_customer_id,
                'created_at': order.get('created_at')
            })
    
    if orphaned_orders:
        print("⚠️  WARNING: Found orders with non-existent customer_id:")
        for orphan in orphaned_orders:
            print(f"   - Order: {orphan['order_id']}")
            print(f"     Customer ID: {orphan['customer_id']} (NOT FOUND in customers)")
            print(f"     Created: {orphan['created_at']}")
            print()
    else:
        print("✅ All orders have valid customer_id references")
        print()
    
    # 4. Test recent orders (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_orders = list(online_transactions.find({
        'created_at': {'$gte': yesterday}
    }).sort('created_at', -1))
    
    print(f"📅 RECENT ORDERS (Last 24 hours): {len(recent_orders)}")
    print()
    
    if recent_orders:
        for order in recent_orders:
            customer_id = order.get('customer_id')
            customer = customers.find_one({'_id': customer_id})
            
            status = "✅ OK" if customer else "❌ MISSING"
            print(f"   {status} Order: {order['_id']}")
            print(f"      Customer ID: {customer_id}")
            if customer:
                print(f"      Customer Email: {customer.get('email', 'N/A')}")
            else:
                print(f"      ❌ Customer NOT FOUND in database!")
            print()
    else:
        print("   No recent orders found")
        print()
    
    # 5. Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Customers: {len(customer_list)}")
    print(f"Total Orders: {len(order_list)}")
    print(f"Orphaned Orders: {len(orphaned_orders)}")
    print(f"Recent Orders (24h): {len(recent_orders)}")
    print()
    
    if orphaned_orders:
        print("⚠️  ACTION REQUIRED:")
        print("   Some orders have customer_id values that don't match any customer.")
        print("   This indicates the JWT token user_id doesn't match the customer _id.")
        print()
        print("   To fix:")
        print("   1. Check JWT token generation - ensure 'user_id' = customer '_id'")
        print("   2. Update orphaned orders to use correct customer_id")
        print()
        return False
    else:
        print("✅ SUCCESS: All orders have consistent customer_id!")
        print("   New orders should now appear in Order History immediately.")
        print()
        return True


if __name__ == '__main__':
    try:
        success = test_customer_id_consistency()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

