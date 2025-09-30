#!/usr/bin/env python
"""
Test script to verify MongoDB Atlas connection
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posbackend.settings')
django.setup()

from app.database import db_manager
from app.models import User, Customer, Product, Category, SalesLog, Promotions
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test MongoDB connection and basic operations"""
    try:
        # Get database connection
        db = db_manager.get_database()
        if db is None:
            logger.error("Failed to connect to database")
            return False
        
        logger.info("✅ Successfully connected to MongoDB Atlas")
        
        # Test collections
        collections = db.list_collection_names()
        logger.info(f"📁 Available collections: {collections}")
        
        # Test reading from collections
        if 'users' in collections:
            users_count = db.users.count_documents({})
            logger.info(f"👥 Users collection: {users_count} documents")
            
            # Get a sample user
            sample_user = db.users.find_one()
            if sample_user:
                logger.info(f"📄 Sample user: {sample_user.get('username', 'N/A')} - {sample_user.get('email', 'N/A')}")
        
        if 'products' in collections:
            products_count = db.products.count_documents({})
            logger.info(f"🛍️ Products collection: {products_count} documents")
            
            # Get a sample product
            sample_product = db.products.find_one()
            if sample_product:
                logger.info(f"📄 Sample product: {sample_product.get('product_name', 'N/A')} - ${sample_product.get('selling_price', 0)}")
        
        if 'customers' in collections:
            customers_count = db.customers.count_documents({})
            logger.info(f"👤 Customers collection: {customers_count} documents")
        
        if 'promotions' in collections:
            promotions_count = db.promotions.count_documents({})
            logger.info(f"🎯 Promotions collection: {promotions_count} documents")
        
        if 'sales_log' in collections:
            sales_count = db.sales_log.count_documents({})
            logger.info(f"💰 Sales Log collection: {sales_count} documents")
        
        logger.info("🎉 All tests passed! Your MongoDB connection is working correctly.")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing MongoDB connection: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing MongoDB Atlas Connection...")
    print("=" * 50)
    
    success = test_connection()
    
    if success:
        print("\n✅ MongoDB connection test completed successfully!")
        print("Your backend is now connected to your MongoDB Atlas database.")
    else:
        print("\n❌ MongoDB connection test failed!")
        print("Please check your connection string and network access.")
    
    print("=" * 50)
