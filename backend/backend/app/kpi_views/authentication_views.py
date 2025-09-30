from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from ..services.auth_services import AuthService
from ..services.session_services import SessionLogService
import logging

logger = logging.getLogger(__name__)

# ================ AUTHENTICATION VIEWS ================

class LoginView(APIView):
    def post(self, request):
        """User login"""
        try:
            auth_service = AuthService()
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response(
                    {"error": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = auth_service.login(email, password)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):
    def post(self, request):
        """User logout"""
        try:
            auth_service = AuthService()

            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                return Response(
                    {"error": "Missing or invalid authorization header"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Let AuthService handle everything including session logout
            token = authorization.replace("Bearer ", "").strip()
            result = auth_service.logout(token)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RefreshTokenView(APIView):
    def post(self, request):
        """Refresh access token"""
        try:
            auth_service = AuthService()
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = auth_service.refresh_access_token(refresh_token)
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CurrentUserView(APIView):
    def get(self, request):
        """Get current authenticated user"""
        try:
            auth_service = AuthService()

            authorization = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                return Response(
                    {"error": "Missing or invalid authorization header"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            token = authorization.split(" ")[1]
            user = auth_service.get_current_user(token)

            if user:
                return Response(user, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyTokenView(APIView):
    def post(self, request):
        """Verify if token is valid"""
        try:
            auth_service = AuthService()

            authorization = request.headers.get("Authorization")
            if authorization and authorization.startswith("Bearer "):
                token = authorization.split(" ")[1]
            else:
                token = request.data.get('token')

            if not token:
                return Response(
                    {"error": "Token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            payload = auth_service.verify_token(token)

            if payload:
                return Response({
                    "valid": True,
                    "user_id": payload.get("sub"),
                    "email": payload.get("email"),
                    "role": payload.get("role")
                }, status=status.HTTP_200_OK)

            return Response(
                {"valid": False, "error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegisterView(APIView):
    def post(self, request):
        """User registration - Public endpoint"""
        try:
            from ..services.user_service import UserService
            from ..serializers import UserCreateSerializer

            user_service = UserService()

            # Validate required fields (accept either full_name or first/last)
            required_fields = ['email', 'password']
            for field in required_fields:
                if not request.data.get(field):
                    return Response(
                        {"error": f"{field.replace('_', ' ').title()} is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Use the same serializer as user creation
            # Normalize name fields for serializer compatibility
            normalized_data = request.data.copy()
            if not normalized_data.get('full_name'):
                first = (normalized_data.get('first_name') or '').strip()
                last = (normalized_data.get('last_name') or '').strip()
                if first or last:
                    normalized_data['full_name'] = f"{first} {last}".strip()

            if not normalized_data.get('username'):
                # default username from email prefix
                email_val = normalized_data.get('email', '')
                normalized_data['username'] = email_val.split('@')[0] if '@' in email_val else email_val

            serializer = UserCreateSerializer(data=normalized_data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Validation failed", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set default role for registration
            user_data = serializer.validated_data.copy()
            user_data['role'] = user_data.get('role', 'customer')

            # Create user without requiring authentication (public registration)
            try:
                new_user = user_service.create_user(user_data, None)  # No current_user for public registration
            except Exception as create_error:
                return Response(
                    {"error": f"User creation failed: {str(create_error)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Auto-login after registration
            try:
                auth_service = AuthService()
                login_result = auth_service.login(user_data['email'], request.data.get('password'))

                if login_result.get('success'):
                    return Response({
                        "message": "Registration successful",
                        "user": new_user,
                        "token": login_result.get('access_token'),
                        "refresh_token": login_result.get('refresh_token')
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "message": "Registration successful, but auto-login failed. Please login manually.",
                        "user": new_user
                    }, status=status.HTTP_201_CREATED)
            except Exception as login_error:
                return Response({
                    "message": "Registration successful, but auto-login failed. Please login manually.",
                    "user": new_user,
                    "login_error": str(login_error)
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
