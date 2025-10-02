"""
MongoDB Models using MongoEngine
These models will store data in MongoDB Atlas
"""
from mongoengine import Document, StringField, EmailField, IntField, FloatField, DateTimeField, ListField, ReferenceField, BooleanField
from datetime import datetime
import bcrypt


class User(Document):
    """User model for MongoDB"""
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)
    phone = StringField(max_length=20)
    points = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'users',
        'indexes': ['email', 'username']
    }
    
    def set_password(self, password):
        """Hash password before saving"""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if password matches"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'points': self.points,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Product(Document):
    """Product model for MongoDB"""
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    category = StringField()
    image = StringField()
    in_stock = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'products'
    }


class Order(Document):
    """Order model for MongoDB"""
    user = ReferenceField(User)
    products = ListField()
    total_amount = FloatField(required=True)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'orders'
    }
