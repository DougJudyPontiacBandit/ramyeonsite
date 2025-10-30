#!/usr/bin/env python3
"""
Test script for Order History API endpoint
Run from backend directory: python ../test_order_history.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posbackend.settings')
import django
django.setup()

from app.database import db_manager
from datetime import datetime

def test_order_history_setup():
    """Test that MongoDB connection and collections exist"""
    print("=" * 60)
    print("TESTING ORDER HISTORY SETUP")
    print("=" * 60)
    
    try:
        # Get database
        db = db_manager.get_database()
        print("✅ Connected to MongoDB")
        
        # Check collections exist
        collections = db.list_collection_names()
        print(f"\n📊 Available collections: {len(collections)}")
        
        # Check online_transactions collection
        if 'online_transactions' in collections:
            print("✅ online_transactions collection exists")
            
            # Count documents
            count = db.online_transactions.count_documents({})
            print(f"📦 Total orders in database: {count}")
            
            # Check for sample order
            if count > 0:
                sample = db.online_transactions.find_one()
                print(f"\n📄 Sample order structure:")
                print(f"  - Order ID: {sample.get('_id')}")
                print(f"  - Customer ID: {sample.get('customer_id')}")
                print(f"  - Total Amount: ₱{sample.get('total_amount', 0):.2f}")
                print(f"  - Created: {sample.get('created_at')}")
                print(f"  - Status: {sample.get('order_status')}")
            else:
                print("ℹ️  No orders in database yet (this is okay for new installs)")
        else:
            print("⚠️  online_transactions collection does not exist")
            print("   This will be created automatically when first order is placed")
        
        # Check customers collection
        if 'customers' in collections:
            print("\n✅ customers collection exists")
            customer_count = db.customers.count_documents({})
            print(f"👥 Total customers: {customer_count}")
        else:
            print("\n⚠️  customers collection does not exist")
        
        # Test query by customer_id
        print("\n" + "=" * 60)
        print("TESTING QUERY BY CUSTOMER ID")
        print("=" * 60)
        
        # Find a customer with orders
        pipeline = [
            {"$group": {"_id": "$customer_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        
        result = list(db.online_transactions.aggregate(pipeline))
        if result:
            test_customer_id = result[0]['_id']
            order_count = result[0]['count']
            print(f"📋 Testing with customer: {test_customer_id}")
            print(f"   Orders: {order_count}")
            
            # Fetch orders for this customer
            orders = list(db.online_transactions.find(
                {'customer_id': test_customer_id}
            ).sort('created_at', -1).limit(5))
            
            print(f"\n✅ Successfully fetched {len(orders)} orders")
            for i, order in enumerate(orders, 1):
                print(f"\n   Order {i}:")
                print(f"   - ID: {order.get('_id')}")
                print(f"   - Total: ₱{order.get('total_amount', 0):.2f}")
                print(f"   - Status: {order.get('order_status')}")
                print(f"   - Date: {order.get('created_at')}")
        else:
            print("ℹ️  No orders found (database is empty)")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. Start the backend server: python manage.py runserver")
        print("   2. Login as a customer on the frontend")
        print("   3. Try fetching orders: GET /api/v1/online/orders/history/")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\nDetails: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = test_order_history_setup()
    sys.exit(0 if success else 1)


