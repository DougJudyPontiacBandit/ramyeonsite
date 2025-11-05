from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from ..services.customer_service import CustomerService
from ..services.auth_services import AuthService
from ..services.session_services import SessionLogService
from ..decorators.authenticationDecorator import require_admin, require_authentication, get_authenticated_user_from_jwt
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import logging

logger = logging.getLogger(__name__)

class CustomerLoginView(APIView):
    """Customer login using email/password; returns JWT compatible with auth decorator."""
    def __init__(self):
        self.customer_service = CustomerService()
        self.auth_service = AuthService()

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            customer = self.customer_service.authenticate_customer(email, password)
            if not customer:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

            customer_id = str(customer.get('_id'))
            token_data = {"sub": customer_id, "email": customer.get('email'), "role": "customer"}
            access_token = self.auth_service.create_access_token(token_data)
            refresh_token = self.auth_service.create_refresh_token(token_data)

            sanitized = {
                "id": customer_id,
                "email": customer.get('email'),
                "username": customer.get('username'),
                "full_name": customer.get('full_name'),
                "loyalty_points": customer.get('loyalty_points', 0),
                "role": "customer",
            }

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": sanitized
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Customer login error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerCurrentUserView(APIView):
    """Return current authenticated customer profile using JWT"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        try:
            user_ctx = getattr(request, 'current_user', None) or {}
            customer_id = user_ctx.get('user_id')
            if not customer_id:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            customer = self.customer_service.get_customer_by_id(customer_id)
            if not customer:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            # Sanitize
            customer_data = dict(customer)
            customer_data.pop('password', None)

            return Response({
                "success": True,
                "customer": customer_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Customer me error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerListView(APIView):
    def __init__(self):
        self.customer_service = CustomerService()

    @require_admin  
    def get(self, request):
        """Get customers with pagination and filters - Admin only"""
        try:
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 50))
            status_filter = request.query_params.get('status')
            min_loyalty_points = request.query_params.get('min_loyalty_points')
            include_deleted = request.query_params.get('include_deleted', 'false').lower() == 'true'
            sort_by = request.query_params.get('sort_by')
            
            if min_loyalty_points:
                min_loyalty_points = int(min_loyalty_points)
            
            result = self.customer_service.get_customers(
                page=page,
                limit=limit,
                status=status_filter,
                min_loyalty_points=min_loyalty_points,
                include_deleted=include_deleted,
                sort_by=sort_by
            )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting customers: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @require_authentication
    def post(self, request):
        """Create new customer - Authenticated users can create customers"""
        try:
            customer_data = request.data
            new_customer = self.customer_service.create_customer(
                customer_data, 
                request.current_user  # Set by decorator
            )
            
            return Response(new_customer, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomerDetailView(APIView):
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request, customer_id):
        """Get customer by ID - Authentication required"""
        try:
            customer = self.customer_service.get_customer_by_id(customer_id)
            if customer:
                return Response(customer, status=status.HTTP_200_OK)
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @require_authentication
    def put(self, request, customer_id):
        """Update customer - Authentication required"""
        try:
            customer_data = request.data
            updated_customer = self.customer_service.update_customer(
                customer_id, 
                customer_data, 
                request.current_user  # Set by decorator
            )
            
            if updated_customer:
                return Response(updated_customer, status=status.HTTP_200_OK)
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @require_authentication
    def delete(self, request, customer_id):
        """Delete customer - Admin only"""
        try:
            deleted = self.customer_service.soft_delete_customer(
                customer_id, 
                request.current_user
            )
            
            print(f"Delete result: {deleted}")
            
            if deleted:
                return Response(
                    {"message": "Customer deleted successfully"}, 
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Exception in delete: {e}")
            logger.error(f"Error deleting customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerRestoreView(APIView):
    """View for restoring soft-deleted customers"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_admin
    def post(self, request, customer_id):
        """Restore a soft-deleted customer - Admin only"""
        try:
            restored = self.customer_service.restore_customer(
                customer_id, 
                request.current_user
            )
            
            if restored:
                return Response(
                    {"message": "Customer restored successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Customer not found or not deleted"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Error restoring customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerHardDeleteView(APIView):
    """View for permanently deleting customers"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_admin
    def delete(self, request, customer_id):
        """PERMANENTLY delete customer - Admin only with confirmation"""
        try:
            confirm = request.query_params.get('confirm', '').lower()
            if confirm != 'yes':
                return Response({
                    "error": "Permanent deletion requires confirmation", 
                    "message": "Add ?confirm=yes to permanently delete this customer"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            deleted = self.customer_service.hard_delete_customer(
                customer_id, 
                request.current_user,
                confirmation_token="PERMANENT_DELETE_CONFIRMED"  # Add this
            )
            
            if deleted:
                return Response({
                    "message": "Customer permanently deleted"
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Error permanently deleting customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerSearchView(APIView):
    """View for searching customers"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        """Search customers by name, email, or phone"""
        try:
            search_term = request.query_params.get('q', '').strip()
            if not search_term:
                return Response(
                    {"error": "Search term 'q' parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            customers = self.customer_service.search_customers(search_term)
            return Response(customers, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error searching customers: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerByEmailView(APIView):
    """View for getting customer by email"""
    def __init__(self):
        self.customer_service = CustomerService()
        
    @require_authentication
    def get(self, request, email):
        """Get customer by email"""
        try:
            customer = self.customer_service.get_customer_by_email(email)
            if customer:
                return Response(customer, status=status.HTTP_200_OK)
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting customer by email {email}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerStatisticsView(APIView):
    """View for customer statistics and analytics"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        """Get customer statistics"""
        try:
            stats = self.customer_service.get_customer_statistics()
            return Response(stats, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting customer statistics: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomerLoyaltyView(APIView):
    """View for managing customer loyalty points"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def post(self, request, customer_id):
        """Update customer loyalty points"""
        try:
            points_to_add = request.data.get('points', 0)
            reason = request.data.get('reason', 'Manual adjustment')
            
            if not isinstance(points_to_add, (int, float)) or points_to_add <= 0:
                return Response(
                    {"error": "Points must be a positive number"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated_customer = self.customer_service.update_loyalty_points(
                customer_id, 
                points_to_add, 
                reason, 
                request.current_user
            )
            
            if updated_customer:
                return Response(updated_customer, status=status.HTTP_200_OK)
            return Response(
                {"error": "Customer not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            logger.error(f"Error updating loyalty points for customer {customer_id}: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


# ========== CUSTOMER-FACING LOYALTY ENDPOINTS (JWT AUTH) ==========

class CustomerLoyaltyBalanceView(APIView):
    """Get current customer's loyalty points balance (JWT auth)"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        """Get authenticated customer's loyalty points balance"""
        try:
            # Get customer ID from JWT token
            customer_id = request.current_user.get('_id')
            
            if not customer_id:
                return Response(
                    {"error": "Customer not authenticated"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get customer data
            customer = self.customer_service.get_customer_by_id(customer_id)
            
            if not customer:
                return Response(
                    {"error": "Customer not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response({
                "balance": customer.get('loyalty_points', 0),
                "customer_id": str(customer_id)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting loyalty balance: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerLoyaltyRedeemView(APIView):
    """Redeem loyalty points for current customer (JWT auth)"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def post(self, request):
        """Redeem loyalty points"""
        try:
            customer_id = request.current_user.get('_id')
            points_to_redeem = request.data.get('points_to_redeem', 0)
            order_id = request.data.get('order_id')
            
            if not customer_id:
                return Response(
                    {"error": "Customer not authenticated"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if points_to_redeem <= 0:
                return Response(
                    {"error": "Points to redeem must be positive"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Redeem points
            updated_customer = self.customer_service.redeem_loyalty_points(
                customer_id,
                points_to_redeem,
                reason=f"Redeemed for order {order_id}" if order_id else "Points redemption",
                current_user=request.current_user
            )
            
            if updated_customer:
                return Response({
                    "success": True,
                    "new_balance": updated_customer.get('loyalty_points', 0),
                    "points_redeemed": points_to_redeem
                }, status=status.HTTP_200_OK)
            
            return Response(
                {"error": "Failed to redeem points"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error redeeming loyalty points: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerLoyaltyAwardView(APIView):
    """Award loyalty points to current customer (JWT auth)"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication  
    def post(self, request):
        """Award loyalty points based on order amount"""
        try:
            customer_id = request.current_user.get('_id')
            order_amount = request.data.get('order_amount', 0)
            order_id = request.data.get('order_id')
            
            if not customer_id:
                return Response(
                    {"error": "Customer not authenticated"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if order_amount <= 0:
                return Response(
                    {"error": "Order amount must be positive"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate points (20% of order amount)
            points_to_award = int(order_amount * 0.20)
            
            # Award points
            updated_customer = self.customer_service.update_loyalty_points(
                customer_id,
                points_to_award,
                reason=f"Points earned from order {order_id}" if order_id else "Purchase reward",
                current_user=request.current_user
            )
            
            if updated_customer:
                return Response({
                    "success": True,
                    "points_awarded": points_to_award,
                    "total_points": updated_customer.get('loyalty_points', 0),
                    "order_amount": order_amount
                }, status=status.HTTP_200_OK)
            
            return Response(
                {"error": "Failed to award points"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Error awarding loyalty points: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerLoyaltyHistoryView(APIView):
    """Get current customer's loyalty points history (JWT auth)"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        """Get authenticated customer's loyalty points history"""
        try:
            customer_id = request.current_user.get('_id')
            
            if not customer_id:
                return Response(
                    {"error": "Customer not authenticated"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get customer data
            customer = self.customer_service.get_customer_by_id(customer_id)
            
            if not customer:
                return Response(
                    {"error": "Customer not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get loyalty history
            history = customer.get('loyalty_history', [])
            
            return Response({
                "results": history,
                "count": len(history)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting loyalty history: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerLoyaltyCurrentTierView(APIView):
    """Get current customer's loyalty tier (JWT auth)"""
    def __init__(self):
        self.customer_service = CustomerService()

    @require_authentication
    def get(self, request):
        """Get authenticated customer's current loyalty tier"""
        try:
            customer_id = request.current_user.get('_id')
            
            if not customer_id:
                return Response(
                    {"error": "Customer not authenticated"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get customer data
            customer = self.customer_service.get_customer_by_id(customer_id)
            
            if not customer:
                return Response(
                    {"error": "Customer not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calculate tier based on points
            points = customer.get('loyalty_points', 0)
            
            if points >= 3000:
                tier = {"name": "Platinum", "min_points": 3000, "max_points": None, "multiplier": 2.0}
            elif points >= 1500:
                tier = {"name": "Gold", "min_points": 1500, "max_points": 2999, "multiplier": 1.5}
            elif points >= 500:
                tier = {"name": "Silver", "min_points": 500, "max_points": 1499, "multiplier": 1.25}
            else:
                tier = {"name": "Bronze", "min_points": 0, "max_points": 499, "multiplier": 1.0}
            
            return Response(tier, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error getting current tier: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ========== CUSTOMER REGISTRATION ==========

class CustomerRegisterView(APIView):
    """Customer registration endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Extract registration data
            customer_data = {
                'email': request.data.get('email', '').strip().lower(),
                'password': request.data.get('password', ''),
                'username': request.data.get('username', '').strip(),
                'full_name': request.data.get('full_name', '').strip(),
                'phone': request.data.get('phone', '').strip(),
                'delivery_address': request.data.get('delivery_address', {})
            }
            
            # Validate required fields
            required_fields = ['email', 'password', 'username', 'full_name']
            for field in required_fields:
                if not customer_data.get(field):
                    return Response({
                        'success': False,
                        'error': f'{field.replace("_", " ").title()} is required'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate password strength
            if len(customer_data['password']) < 6:
                return Response({
                    'success': False,
                    'error': 'Password must be at least 6 characters long'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create customer using CustomerService
            customer_service = CustomerService()
            customer = customer_service.create_customer(customer_data)
            
            # Generate JWT token
            token_payload = {
                'customer_id': customer['_id'],
                'email': customer['email'],
                'username': customer['username'],
                'exp': datetime.utcnow() + timedelta(days=7)
            }
            
            token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
            
            # Create session
            session_service = SessionLogService()
            session_data = {
                'user_id': customer['_id'],
                'username': customer['username'],
                'email': customer['email'],
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT')
            }
            session = session_service.log_login(session_data)
            
            # Return success response
            return Response({
                'success': True,
                'message': 'Registration successful',
                'token': token,
                'customer': {
                    'id': customer['_id'],
                    'email': customer['email'],
                    'username': customer['username'],
                    'full_name': customer['full_name'],
                    'loyalty_points': customer.get('loyalty_points', 0),
                    'phone': customer.get('phone', ''),
                    'delivery_address': customer.get('delivery_address', {})
                },
                'session_id': session.get('_id') if session else None
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Customer registration error: {str(e)}")
            return Response({
                'success': False,
                'error': 'Registration failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)