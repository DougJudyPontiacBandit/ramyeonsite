from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.cart_service import CartService
from ..decorators.authenticationDecorator import require_authentication
import logging

logger = logging.getLogger(__name__)

class CartView(APIView):
    """View for cart operations"""
    def __init__(self):
        self.cart_service = CartService()

    @require_authentication
    def get(self, request):
        """Get user's cart"""
        try:
            customer_id = request.current_user.get('user_id')
            cart = self.cart_service.get_cart_by_customer(customer_id)

            if cart:
                return Response({
                    "success": True,
                    "cart": cart
                }, status=status.HTTP_200_OK)
            else:
                # Return empty cart
                return Response({
                    "success": True,
                    "cart": {
                        "items": [],
                        "total_amount": 0.0,
                        "item_count": 0
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error getting cart: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def post(self, request):
        """Create or get cart for user"""
        try:
            customer_id = request.current_user.get('user_id')
            cart = self.cart_service.get_or_create_cart(customer_id)

            return Response({
                "success": True,
                "cart": cart
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating cart: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @require_authentication
    def delete(self, request):
        """Clear cart"""
        try:
            customer_id = request.current_user.get('user_id')
            cleared = self.cart_service.clear_cart(customer_id)

            return Response({
                "success": True,
                "message": "Cart cleared successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error clearing cart: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CartItemView(APIView):
    """View for cart item operations"""
    def __init__(self):
        self.cart_service = CartService()

    @require_authentication
    def post(self, request):
        """Add item to cart"""
        try:
            customer_id = request.current_user.get('user_id')
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            price = request.data.get('price', 0.0)
            product_name = request.data.get('product_name', '')

            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart = self.cart_service.add_item_to_cart(
                customer_id,
                product_id,
                quantity,
                price,
                product_name
            )

            return Response({
                "success": True,
                "cart": cart
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error adding item to cart: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @require_authentication
    def put(self, request):
        """Update item quantity in cart"""
        try:
            customer_id = request.current_user.get('user_id')
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)

            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart = self.cart_service.update_item_quantity(
                customer_id,
                product_id,
                quantity
            )

            if cart:
                return Response({
                    "success": True,
                    "cart": cart
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Cart or item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating cart item: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @require_authentication
    def delete(self, request):
        """Remove item from cart"""
        try:
            customer_id = request.current_user.get('user_id')
            product_id = request.query_params.get('product_id')

            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart = self.cart_service.remove_item_from_cart(
                customer_id,
                product_id
            )

            if cart:
                return Response({
                    "success": True,
                    "cart": cart
                }, status=status.HTTP_200_OK)
            return Response(
                {"error": "Cart or item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error removing item from cart: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CartCheckoutView(APIView):
    """View for cart checkout"""
    def __init__(self):
        self.cart_service = CartService()

    @require_authentication
    def post(self, request):
        """Checkout cart - convert to POS transaction"""
        try:
            customer_id = request.current_user.get('user_id')
            promotion_name = request.data.get('promotion_name')
            delivery_type = request.data.get('delivery_type')
            delivery_address = request.data.get('delivery_address')
            payment_method = request.data.get('payment_method')
            special_instructions = request.data.get('special_instructions')

            # Get cart
            cart = self.cart_service.get_cart_by_customer(customer_id)
            if not cart or not cart.get('items'):
                return Response(
                    {"error": "Cart is empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert cart items to checkout data format
            checkout_data = []
            for item in cart['items']:
                checkout_data.append({
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': item['price']
                })

            # Process transaction via POS
            from ..services.pos.promotionCon import PromoConnection
            promo_service = PromoConnection()

            result = promo_service.pos_transaction(
                checkout_data=checkout_data,
                promotion_name=promotion_name,
                cashier_id=customer_id,  # Self-checkout
                metadata={
                    "delivery_type": delivery_type,
                    "delivery_address": delivery_address,
                    "payment_method": payment_method,
                    "special_instructions": special_instructions
                }
            )

            if result['success']:
                # Clear cart after successful transaction
                self.cart_service.clear_cart(customer_id)

                # Award loyalty points
                total_amount = result.get('transaction', {}).get('total_amount', 0)
                points_to_award = int(total_amount)

                if points_to_award > 0:
                    from ..services.customer_service import CustomerService
                    customer_service = CustomerService()
                    customer_service.update_loyalty_points(
                        customer_id,
                        points_to_award,
                        f"Cart Checkout - Transaction {result.get('transaction', {}).get('transaction_id', '')}",
                        request.current_user
                    )
                    result['points_awarded'] = points_to_award

                return Response({
                    "success": True,
                    "message": "Checkout successful",
                    "transaction": result,
                    "delivery": {
                        "delivery_type": delivery_type,
                        "delivery_address": delivery_address,
                        "payment_method": payment_method,
                        "special_instructions": special_instructions
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error during cart checkout: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
