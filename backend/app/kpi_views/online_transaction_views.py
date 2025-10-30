from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..decorators.authenticationDecorator import require_authentication
from ..services.online_transactions_service import OnlineTransactionService
from ..database import db_manager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CreateOnlineOrderView(APIView):
    """Create a new online order (customer website)."""

    @require_authentication
    def post(self, request):
        try:
            service = OnlineTransactionService()

            customer_id = request.data.get('customer_id')
            # Fallback to token user id if not provided
            if not customer_id:
                user_ctx = getattr(request, 'current_user', None) or {}
                customer_id = user_ctx.get('user_id')

            if not customer_id:
                return Response({
                    'success': False,
                    'message': 'Customer ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            order_data = {
                'items': request.data.get('items', []),
                'delivery_address': request.data.get('delivery_address', {}),
                'delivery_type': request.data.get('delivery_type', 'delivery'),
                'payment_method': request.data.get('payment_method', 'cod'),
                'points_to_redeem': request.data.get('points_to_redeem', 0),
                'notes': request.data.get('notes') or request.data.get('special_instructions', ''),
            }

            result = service.create_online_order(order_data, customer_id)

            return Response({
                'success': True,
                'message': 'Order created successfully',
                'data': result['data']
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Online order validation error: {e}")
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Online order error: {e}")
            return Response({'success': False, 'message': f'Failed to create order: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerOrderHistoryView(APIView):
    """Get order history for the authenticated customer from MongoDB."""

    @require_authentication
    def get(self, request):
        try:
            # Get customer ID from JWT token
            user_ctx = getattr(request, 'current_user', None) or {}
            customer_id = user_ctx.get('user_id')

            if not customer_id:
                return Response({
                    'success': False,
                    'message': 'Customer ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get pagination parameters
            limit = int(request.GET.get('limit', 50))
            offset = int(request.GET.get('offset', 0))

            # Validate parameters
            if limit < 1 or limit > 100:
                limit = 50
            if offset < 0:
                offset = 0

            # Get MongoDB database
            db = db_manager.get_database()
            online_transactions = db.online_transactions

            # Fetch customer's online transactions from MongoDB
            # Filter by customer_id and sort by created_at descending
            cursor = online_transactions.find({
                'customer_id': customer_id
            }).sort('created_at', -1).skip(offset).limit(limit)

            # Convert cursor to list and serialize
            orders = []
            for order in cursor:
                # Get current status
                current_status = order.get('order_status', 'pending')
                
                # Import status info function
                from .order_status_views import get_status_display_info
                status_info = get_status_display_info(current_status)
                
                # Convert MongoDB document to JSON-serializable dict
                order_dict = {
                    'order_id': str(order.get('_id')),
                    'customer_id': order.get('customer_id'),
                    'customer_name': order.get('customer_name'),
                    'customer_email': order.get('customer_email'),
                    'items': order.get('items', []),
                    'subtotal': float(order.get('subtotal', 0)),
                    'points_redeemed': int(order.get('points_redeemed', 0)),
                    'points_discount': float(order.get('points_discount', 0)),
                    'subtotal_after_discount': float(order.get('subtotal_after_discount', 0)),
                    'delivery_fee': float(order.get('delivery_fee', 0)),
                    'service_fee': float(order.get('service_fee', 0)),
                    'total_amount': float(order.get('total_amount', 0)),
                    'delivery_type': order.get('delivery_type'),
                    'delivery_address': order.get('delivery_address', {}),
                    'payment_method': order.get('payment_method'),
                    'payment_status': order.get('payment_status', 'pending'),
                    'payment_reference': order.get('payment_reference'),
                    'order_status': current_status,
                    'status': current_status,
                    'status_info': status_info,  # Add status display info
                    'notes': order.get('notes', ''),
                    'loyalty_points_earned': int(order.get('loyalty_points_earned', 0)),
                    'created_at': order.get('created_at').isoformat() if order.get('created_at') else None,
                    'updated_at': order.get('updated_at').isoformat() if order.get('updated_at') else None,
                    'transaction_date': order.get('transaction_date').isoformat() if order.get('transaction_date') else None,
                }
                orders.append(order_dict)

            # Get total count for pagination info
            total_count = online_transactions.count_documents({'customer_id': customer_id})

            logger.info(f"Fetched {len(orders)} orders for customer {customer_id} (total: {total_count})")

            return Response({
                'success': True,
                'count': len(orders),
                'total': total_count,
                'offset': offset,
                'limit': limit,
                'results': orders
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(f"Order history parameter error: {e}")
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Order history error: {e}", exc_info=True)
            return Response({'success': False, 'message': f'Failed to fetch orders: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


