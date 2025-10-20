from datetime import datetime
from app.database import db_manager
import bcrypt
import logging

logger = logging.getLogger(__name__)

class CustomerAuthService:
    """Lightweight customer authentication service - customer website only"""
    
    def __init__(self):
        self.db = db_manager.get_database()
        self.customer_collection = self.db.customers
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        if not password:
            raise ValueError("Password cannot be empty")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    
    def authenticate_customer(self, email, password):
        """Authenticate customer with email and password"""
        try:
            if not email or not password:
                return None
            
            customer = self.customer_collection.find_one({
                'email': email.strip().lower(),
                'isDeleted': {'$ne': True},
                'status': 'active'
            })
            
            if not customer:
                return None
            
            if self.verify_password(password, customer['password']):
                # Update last login timestamp
                self.customer_collection.update_one(
                    {'_id': customer['_id']},
                    {'$set': {'last_updated': datetime.utcnow()}}
                )
                return customer
            
            return None
            
        except Exception as e:
            logger.error(f"Error authenticating customer: {str(e)}")
            raise Exception(f"Error authenticating customer: {str(e)}")
    
    def generate_customer_id(self):
        """Generate sequential CUST-##### format ID"""
        try:
            pipeline = [
                {"$match": {"_id": {"$regex": "^CUST-"}}},
                {"$addFields": {
                    "id_number": {
                        "$toInt": {"$substr": ["$_id", 5, -1]}
                    }
                }},
                {"$sort": {"id_number": -1}},
                {"$limit": 1}
            ]
            
            result = list(self.customer_collection.aggregate(pipeline))
            next_number = (result[0]["id_number"] + 1) if result else 1
            
            return f"CUST-{next_number:05d}"
            
        except Exception as e:
            logger.error(f"Error generating customer ID: {e}")
            import time
            return f"CUST-{int(time.time()) % 100000:05d}"
    
    def create_customer(self, customer_data):
        """Create new customer account"""
        try:
            required_fields = ["email", "password", "username", "full_name"]
            for field in required_fields:
                if not customer_data.get(field):
                    raise ValueError(f"{field.replace('_', ' ').title()} is required")
            
            # Check if email already exists
            existing_customer = self.customer_collection.find_one({
                "email": customer_data["email"].strip().lower(),
                "isDeleted": {"$ne": True}
            })
            if existing_customer:
                raise ValueError("Email already exists")
            
            # Check if username already exists
            existing_username = self.customer_collection.find_one({
                "username": customer_data["username"].strip(),
                "isDeleted": {"$ne": True}
            })
            if existing_username:
                raise ValueError("Username already exists")
            
            # Generate sequential ID
            customer_id = self.generate_customer_id()
            now = datetime.utcnow()
            
            # Create customer record
            customer_record = {
                "_id": customer_id,
                "username": customer_data["username"].strip(),
                "full_name": customer_data["full_name"].strip(),
                "email": customer_data["email"].strip().lower(),
                "password": self.hash_password(customer_data["password"]),
                "phone": customer_data.get("phone", ""),
                "delivery_address": customer_data.get("delivery_address", {}),
                "loyalty_points": 0,
                "last_purchase": None,
                "isDeleted": False,
                "date_created": now,
                "last_updated": now,
                "status": "active"
            }
            
            self.customer_collection.insert_one(customer_record)
            
            return customer_record
            
        except Exception as e:
            raise Exception(f"Error creating customer: {str(e)}")
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        try:
            if not customer_id:
                return None
                
            query = {
                '_id': customer_id,
                'isDeleted': {'$ne': True}
            }
            
            return self.customer_collection.find_one(query)
            
        except Exception as e:
            raise Exception(f"Error getting customer: {str(e)}")
    
    def change_customer_password(self, customer_id, old_password, new_password):
        """Change customer password"""
        try:
            customer = self.get_customer_by_id(customer_id)
            if not customer:
                return False
            
            if not self.verify_password(old_password, customer['password']):
                raise ValueError("Current password is incorrect")
            
            result = self.customer_collection.update_one(
                {'_id': customer_id},
                {
                    '$set': {
                        'password': self.hash_password(new_password),
                        'last_updated': datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Error changing password: {str(e)}")
    
    def update_customer_profile(self, customer_id, profile_data):
        """Update customer profile information"""
        try:
            customer = self.get_customer_by_id(customer_id)
            if not customer:
                raise ValueError("Customer not found")
            
            # Fields that can be updated
            allowed_fields = ['full_name', 'phone', 'delivery_address', 'profile_picture', 'birthdate']
            update_data = {}
            
            for field in allowed_fields:
                if field in profile_data and profile_data[field] is not None:
                    update_data[field] = profile_data[field]
            
            # Check if email is being updated
            if 'email' in profile_data and profile_data['email']:
                new_email = profile_data['email'].strip().lower()
                # Check if new email is different and not already in use
                if new_email != customer['email']:
                    existing_email = self.customer_collection.find_one({
                        'email': new_email,
                        '_id': {'$ne': customer_id},
                        'isDeleted': {'$ne': True}
                    })
                    if existing_email:
                        raise ValueError("Email already in use by another customer")
                    update_data['email'] = new_email
            
            # Check if username is being updated
            if 'username' in profile_data and profile_data['username']:
                new_username = profile_data['username'].strip()
                if new_username != customer['username']:
                    existing_username = self.customer_collection.find_one({
                        'username': new_username,
                        '_id': {'$ne': customer_id},
                        'isDeleted': {'$ne': True}
                    })
                    if existing_username:
                        raise ValueError("Username already in use by another customer")
                    update_data['username'] = new_username
            
            # Add preferences if provided
            if 'preferences' in profile_data:
                update_data['preferences'] = profile_data['preferences']
            
            # Update timestamp
            update_data['last_updated'] = datetime.utcnow()
            
            # Perform update
            result = self.customer_collection.update_one(
                {'_id': customer_id},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                return self.get_customer_by_id(customer_id)
            
            # Return customer even if nothing was modified
            return customer
            
        except ValueError as e:
            raise e
        except Exception as e:
            logger.error(f"Error updating customer profile: {str(e)}")
            raise Exception(f"Error updating customer profile: {str(e)}")