"""
MongoDB Service for POS System
Handles all database operations using the MongoDB Atlas connection
"""
from app.database import db_manager
from app.models import User, Customer, Product, Category, SalesLog, Promotions
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MongoDBService:
    """Service class for MongoDB operations"""
    
    def __init__(self):
        self.db = db_manager.get_database()
        if self.db is None:
            raise Exception("Database connection not available")
    
    # User Operations
    def get_all_users(self):
        """Get all users from the database"""
        try:
            users = list(self.db.users.find({}))
            return users
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.db.users.find_one({'_id': ObjectId(user_id)})
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            user = self.db.users.find_one({'email': email})
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user = User(**user_data)
            result = self.db.users.insert_one(user.to_dict())
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    # Customer Operations
    def get_all_customers(self):
        """Get all customers from the database"""
        try:
            customers = list(self.db.customers.find({}))
            return customers
        except Exception as e:
            logger.error(f"Error getting customers: {e}")
            return []
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        try:
            customer = self.db.customers.find_one({'_id': ObjectId(customer_id)})
            return customer
        except Exception as e:
            logger.error(f"Error getting customer by ID: {e}")
            return None
    
    def create_customer(self, customer_data):
        """Create a new customer"""
        try:
            customer = Customer(**customer_data)
            result = self.db.customers.insert_one(customer.to_dict())
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return None
    
    # Product Operations
    def get_all_products(self):
        """Get all products from the database"""
        try:
            products = list(self.db.products.find({}))
            return products
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return []
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        try:
            product = self.db.products.find_one({'_id': ObjectId(product_id)})
            return product
        except Exception as e:
            logger.error(f"Error getting product by ID: {e}")
            return None
    
    def get_products_by_category(self, category_id):
        """Get products by category"""
        try:
            products = list(self.db.products.find({'category_id': ObjectId(category_id)}))
            return products
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            return []
    
    def create_product(self, product_data):
        """Create a new product"""
        try:
            product = Product(**product_data)
            result = self.db.products.insert_one(product.to_dict())
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            return None
    
    # Category Operations
    def get_all_categories(self):
        """Get all categories from the database"""
        try:
            categories = list(self.db.category.find({}))
            return categories
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def get_category_by_id(self, category_id):
        """Get category by ID"""
        try:
            category = self.db.category.find_one({'_id': ObjectId(category_id)})
            return category
        except Exception as e:
            logger.error(f"Error getting category by ID: {e}")
            return None
    
    # Sales Log Operations
    def get_all_sales_logs(self):
        """Get all sales logs from the database"""
        try:
            sales_logs = list(self.db.sales_log.find({}))
            return sales_logs
        except Exception as e:
            logger.error(f"Error getting sales logs: {e}")
            return []
    
    def get_sales_log_by_id(self, sales_log_id):
        """Get sales log by ID"""
        try:
            sales_log = self.db.sales_log.find_one({'_id': ObjectId(sales_log_id)})
            return sales_log
        except Exception as e:
            logger.error(f"Error getting sales log by ID: {e}")
            return None
    
    def create_sales_log(self, sales_log_data):
        """Create a new sales log"""
        try:
            sales_log = SalesLog(**sales_log_data)
            result = self.db.sales_log.insert_one(sales_log.to_mongodb_dict())
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating sales log: {e}")
            return None
    
    # Promotions Operations
    def get_all_promotions(self):
        """Get all promotions from the database"""
        try:
            promotions = list(self.db.promotions.find({}))
            return promotions
        except Exception as e:
            logger.error(f"Error getting promotions: {e}")
            return []
    
    def get_promotion_by_id(self, promotion_id):
        """Get promotion by ID"""
        try:
            promotion = self.db.promotions.find_one({'_id': ObjectId(promotion_id)})
            return promotion
        except Exception as e:
            logger.error(f"Error getting promotion by ID: {e}")
            return None
    
    def create_promotion(self, promotion_data):
        """Create a new promotion"""
        try:
            promotion = Promotions(**promotion_data)
            result = self.db.promotions.insert_one(promotion.to_dict())
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating promotion: {e}")
            return None
    
    # Statistics Operations
    def get_database_stats(self):
        """Get database statistics"""
        try:
            stats = {
                'users': self.db.users.count_documents({}),
                'customers': self.db.customers.count_documents({}),
                'products': self.db.products.count_documents({}),
                'categories': self.db.category.count_documents({}),
                'sales_logs': self.db.sales_log.count_documents({}),
                'promotions': self.db.promotions.count_documents({}),
            }
            return stats
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}

# Singleton instance
mongodb_service = MongoDBService()
