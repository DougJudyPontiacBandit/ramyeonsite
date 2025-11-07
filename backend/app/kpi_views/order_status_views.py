from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..decorators.authenticationDecorator import require_authentication
from ..database import db_manager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UpdateOrderStatusView(APIView):
    """Update order status (for POS/Admin use)."""

    @require_authentication
    def post(self, request, order_id):
        try:
            # Get user context
            user_ctx = getattr(request, 'current_user', None) or {}
            user_role = user_ctx.get('role', 'user')

            # Only allow admin/cashier to update order status
            if user_role not in ['admin', 'cashier', 'manager']:
                return Response({
                    'success': False,
                    'message': 'Unauthorized. Only POS staff can update order status.'
                }, status=status.HTTP_403_FORBIDDEN)

            new_status = request.data.get('status')
            notes = request.data.get('notes', '')

            # Validate status
            valid_statuses = [
                'pending',
                'confirmed',
                'preparing',
                'cooking',
                'ready',
                'out_for_delivery',
                'delivered',
                'completed',
                'cancelled'
            ]

            if not new_status or new_status not in valid_statuses:
                return Response({
                    'success': False,
                    'message': f'Invalid status. Valid options: {", ".join(valid_statuses)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get MongoDB database
            db = db_manager.get_database()
            online_transactions = db.online_transactions

            # Find the order
            order = online_transactions.find_one({'_id': order_id})

            if not order:
                return Response({
                    'success': False,
                    'message': 'Order not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Prepare status history entry
            now_utc = datetime.utcnow()
            status_entry = {
                'status': new_status,
                'timestamp': now_utc,
                'updated_by': user_ctx.get('user_id'),
                'notes': notes
            }

            # Update order
            update_result = online_transactions.update_one(
                {'_id': order_id},
                {
                    '$set': {
                        'order_status': new_status,
                        'status': new_status,
                        'updated_at': now_utc,
                        'last_updated_by': user_ctx.get('user_id')
                    },
                    '$push': {
                        'status_history': status_entry
                    }
                }
            )

            # Check if update was acknowledged (modified_count can be 0 if status is same)
            if update_result.matched_count == 0:
                return Response({
                    'success': False,
                    'message': 'Order not found or update failed'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Order {order_id} status updated to {new_status} by {user_ctx.get('user_id')}")

            return Response({
                'success': True,
                'message': 'Order status updated successfully',
                'data': {
                    'order_id': order_id,
                    'new_status': new_status,
                    'updated_at': now_utc.isoformat()
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating order status: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'Failed to update order status: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetOrderStatusView(APIView):
    """Get current order status (for customer tracking)."""

    @require_authentication
    def get(self, request, order_id):
        try:
            # Get customer ID from JWT token
            user_ctx = getattr(request, 'current_user', None) or {}
            customer_id = user_ctx.get('user_id')

            if not customer_id:
                return Response({
                    'success': False,
                    'message': 'Customer ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get MongoDB database
            db = db_manager.get_database()
            online_transactions = db.online_transactions

            # Find the order
            order = online_transactions.find_one({'_id': order_id})

            if not order:
                return Response({
                    'success': False,
                    'message': 'Order not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Verify customer owns this order (security check)
            if order.get('customer_id') != customer_id:
                return Response({
                    'success': False,
                    'message': 'Unauthorized access to order'
                }, status=status.HTTP_403_FORBIDDEN)

            # Get status information
            current_status = order.get('order_status', 'pending')
            status_history = order.get('status_history', [])

            # Format status history
            formatted_history = []
            for entry in status_history:
                formatted_history.append({
                    'status': entry.get('status'),
                    'timestamp': entry.get('timestamp').isoformat() if entry.get('timestamp') else None,
                    'notes': entry.get('notes', '')
                })

            # Status display information
            status_info = get_status_display_info(current_status)

            logger.info(f"Customer {customer_id} checked status for order {order_id}")

            return Response({
                'success': True,
                'data': {
                    'order_id': order_id,
                    'current_status': current_status,
                    'status_info': status_info,
                    'status_history': formatted_history,
                    'last_updated': order.get('updated_at').isoformat() if order.get('updated_at') else None
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching order status: {e}", exc_info=True)
            return Response({
                'success': False,
                'message': f'Failed to fetch order status: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_status_display_info(status_code):
    """Get display information for order status."""
    status_map = {
        'pending': {
            'label': 'Order Pending',
            'description': 'Your order has been placed and is waiting for confirmation',
            'icon': '🕐',
            'color': 'yellow',
            'progress': 10
        },
        'confirmed': {
            'label': 'Order Confirmed',
            'description': 'Your order has been confirmed and will be prepared soon',
            'icon': '✅',
            'color': 'blue',
            'progress': 20
        },
        'preparing': {
            'label': 'Preparing Order',
            'description': 'We are gathering your items',
            'icon': '📦',
            'color': 'blue',
            'progress': 40
        },
        'cooking': {
            'label': 'Cooking',
            'description': 'Your food is being prepared in our kitchen',
            'icon': '👨‍🍳',
            'color': 'orange',
            'progress': 60
        },
        'ready': {
            'label': 'Ready for Pickup/Delivery',
            'description': 'Your order is ready!',
            'icon': '✨',
            'color': 'green',
            'progress': 80
        },
        'out_for_delivery': {
            'label': 'Out for Delivery',
            'description': 'Your order is on the way to you',
            'icon': '🚚',
            'color': 'blue',
            'progress': 90
        },
        'delivered': {
            'label': 'Delivered',
            'description': 'Your order has been delivered',
            'icon': '📦',
            'color': 'green',
            'progress': 95
        },
        'completed': {
            'label': 'Completed',
            'description': 'Order completed successfully',
            'icon': '🎉',
            'color': 'green',
            'progress': 100
        },
        'cancelled': {
            'label': 'Cancelled',
            'description': 'This order has been cancelled',
            'icon': '❌',
            'color': 'red',
            'progress': 0
        }
    }

    return status_map.get(status_code, {
        'label': 'Unknown Status',
        'description': 'Status information not available',
        'icon': '❓',
        'color': 'gray',
        'progress': 0
    })

