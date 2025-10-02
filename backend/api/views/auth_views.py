from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from api.services.customer_auth_service import CustomerAuthService
from api.utils.jwt_utils import generate_jwt_token, sanitize_customer_data, jwt_required
import logging

logger = logging.getLogger(__name__)

customer_service = CustomerAuthService()

@api_view(['POST'])
def customer_login(request):
    """Customer login endpoint"""
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        customer = customer_service.authenticate_customer(email, password)
        
        if not customer:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = generate_jwt_token(customer)
        customer_data = sanitize_customer_data(customer)
        
        return Response({
            'token': token,
            'customer': customer_data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response(
            {'error': 'An error occurred during login'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def customer_register(request):
    """Customer registration endpoint"""
    try:
        customer_data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'username': request.data.get('username'),
            'full_name': request.data.get('full_name'),
            'phone': request.data.get('phone', ''),
            'delivery_address': request.data.get('delivery_address', {})
        }
        
        customer = customer_service.create_customer(customer_data)
        token = generate_jwt_token(customer)
        customer_data = sanitize_customer_data(customer)
        
        return Response({
            'token': token,
            'customer': customer_data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return Response(
            {'error': 'An error occurred during registration'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@jwt_required
def customer_me(request):
    """Get current customer info from JWT token"""
    try:
        customer_id = request.customer['customer_id']
        customer = customer_service.get_customer_by_id(customer_id)
        
        if not customer:
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        customer_data = sanitize_customer_data(customer)
        
        return Response({
            'customer': customer_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Get customer error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@jwt_required
def customer_change_password(request):
    """Change customer password"""
    try:
        customer_id = request.customer['customer_id']
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Old password and new password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success = customer_service.change_customer_password(
            customer_id, old_password, new_password
        )
        
        if success:
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to change password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        return Response(
            {'error': 'An error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )