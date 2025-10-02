"""
MongoDB Views using MongoEngine models
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mongodb_models import User
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@api_view(['POST'])
def register_mongodb(request):
    """Register user in MongoDB"""
    try:
        data = request.data
        
        # Check if user already exists
        if User.objects(email=data.get('email')).first():
            return Response({'email': ['User with this email already exists']}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects(username=data.get('username', data.get('email').split('@')[0])).first():
            return Response({'username': ['User with this username already exists']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new user
        user = User(
            email=data.get('email').lower(),
            username=data.get('username', data.get('email').split('@')[0]),
            first_name=data.get('first_name', data.get('firstName', '')),
            last_name=data.get('last_name', data.get('lastName', '')),
            phone=data.get('phone', ''),
            points=0
        )
        
        # Set password (will be hashed automatically)
        user.set_password(data.get('password'))
        user.save()
        
        return Response({
            'message': 'User created successfully',
            'user': user.to_dict(),
            'access_token': 'dummy_token',  # You can add JWT here
            'refresh_token': 'dummy_refresh'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def login_mongodb(request):
    """Login user from MongoDB"""
    try:
        data = request.data
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        # Find user
        user = User.objects(email=email).first()
        
        if not user:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if not user.check_password(password):
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': 'dummy_token',
            'refresh_token': 'dummy_refresh'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
