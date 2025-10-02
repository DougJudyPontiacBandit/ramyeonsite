import jwt
from datetime import datetime, timedelta
from django.conf import settings
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def generate_jwt_token(customer):
    """Generate JWT token for customer"""
    payload = {
        'customer_id': customer['_id'],
        'username': customer['username'],
        'email': customer['email'],
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def decode_jwt_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return Response(
                {'error': 'Authentication token is missing'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Decode token
        payload = decode_jwt_token(token)
        if not payload:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Add customer info to request
        request.customer = payload
        
        return f(request, *args, **kwargs)
    
    return decorated_function

def sanitize_customer_data(customer):
    """Remove sensitive data from customer object before sending to frontend"""
    if not customer:
        return None
    
    # Create a copy to avoid modifying original
    customer_data = customer.copy() if isinstance(customer, dict) else dict(customer)
    
    # Remove password field
    customer_data.pop('password', None)
    
    # Convert ObjectId to string if present
    if '_id' in customer_data:
        customer_data['_id'] = str(customer_data['_id'])
    
    return customer_data