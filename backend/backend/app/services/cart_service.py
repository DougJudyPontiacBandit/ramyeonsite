from bson import ObjectId
from datetime import datetime
from ..database import db_manager
import logging

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self):
        self.db = db_manager.get_database()
        self.cart_collection = self.db.carts

    def get_or_create_cart(self, customer_id):
        """Get existing cart or create new one for customer"""
        try:
            # Try to find existing active cart
            cart = self.cart_collection.find_one({
                'customer_id': customer_id,
                'status': 'active'
            })

            if cart:
                return cart

            # Create new cart
            new_cart = {
                '_id': ObjectId(),
                'customer_id': customer_id,
                'items': [],
                'total_amount': 0.0,
                'status': 'active',
                'date_created': datetime.utcnow(),
                'last_updated': datetime.utcnow()
            }

            self.cart_collection.insert_one(new_cart)
            return new_cart

        except Exception as e:
            raise Exception(f"Error getting or creating cart: {str(e)}")

    def get_cart_by_customer(self, customer_id):
        """Get cart by customer ID"""
        try:
            cart = self.cart_collection.find_one({
                'customer_id': customer_id,
                'status': 'active'
            })

            if cart:
                # Add item count for convenience
                cart['item_count'] = len(cart.get('items', []))

            return cart

        except Exception as e:
            raise Exception(f"Error getting cart: {str(e)}")

    def add_item_to_cart(self, customer_id, product_id, quantity, price, product_name=""):
        """Add item to cart"""
        try:
            cart = self.get_or_create_cart(customer_id)
            if not cart:
                raise Exception("Could not get or create cart")

            # Check if item already exists
            item_exists = False
            for item in cart.get('items', []):
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    item['subtotal'] = item['quantity'] * item['price']
                    item_exists = True
                    break

            if not item_exists:
                # Add new item
                new_item = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': quantity * price
                }
                cart['items'].append(new_item)

            # Update total
            cart['total_amount'] = sum(item['subtotal'] for item in cart['items'])
            cart['last_updated'] = datetime.utcnow()

            # Save to database
            self.cart_collection.update_one(
                {'_id': cart['_id']},
                {'$set': {
                    'items': cart['items'],
                    'total_amount': cart['total_amount'],
                    'last_updated': cart['last_updated']
                }}
            )

            cart['item_count'] = len(cart['items'])
            return cart

        except Exception as e:
            raise Exception(f"Error adding item to cart: {str(e)}")

    def update_item_quantity(self, customer_id, product_id, quantity):
        """Update item quantity in cart"""
        try:
            cart = self.get_cart_by_customer(customer_id)
            if not cart:
                return None

            item_found = False
            for item in cart.get('items', []):
                if item['product_id'] == product_id:
                    if quantity <= 0:
                        # Remove item if quantity is 0 or negative
                        cart['items'].remove(item)
                    else:
                        item['quantity'] = quantity
                        item['subtotal'] = quantity * item['price']
                    item_found = True
                    break

            if not item_found:
                return None

            # Update total
            cart['total_amount'] = sum(item['subtotal'] for item in cart['items'])
            cart['last_updated'] = datetime.utcnow()

            # Save to database
            self.cart_collection.update_one(
                {'_id': cart['_id']},
                {'$set': {
                    'items': cart['items'],
                    'total_amount': cart['total_amount'],
                    'last_updated': cart['last_updated']
                }}
            )

            cart['item_count'] = len(cart['items'])
            return cart

        except Exception as e:
            raise Exception(f"Error updating item quantity: {str(e)}")

    def remove_item_from_cart(self, customer_id, product_id):
        """Remove item from cart"""
        try:
            cart = self.get_cart_by_customer(customer_id)
            if not cart:
                return None

            # Remove item
            cart['items'] = [item for item in cart['items'] if item['product_id'] != product_id]

            # Update total
            cart['total_amount'] = sum(item['subtotal'] for item in cart['items'])
            cart['last_updated'] = datetime.utcnow()

            # Save to database
            self.cart_collection.update_one(
                {'_id': cart['_id']},
                {'$set': {
                    'items': cart['items'],
                    'total_amount': cart['total_amount'],
                    'last_updated': cart['last_updated']
                }}
            )

            cart['item_count'] = len(cart['items'])
            return cart

        except Exception as e:
            raise Exception(f"Error removing item from cart: {str(e)}")

    def clear_cart(self, customer_id):
        """Clear all items from cart"""
        try:
            result = self.cart_collection.update_one(
                {'customer_id': customer_id, 'status': 'active'},
                {'$set': {
                    'items': [],
                    'total_amount': 0.0,
                    'last_updated': datetime.utcnow()
                }}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Error clearing cart: {str(e)}")

    def abandon_cart(self, customer_id):
        """Mark cart as abandoned"""
        try:
            result = self.cart_collection.update_one(
                {'customer_id': customer_id, 'status': 'active'},
                {'$set': {
                    'status': 'abandoned',
                    'last_updated': datetime.utcnow()
                }}
            )

            return result.modified_count > 0

        except Exception as e:
            raise Exception(f"Error abandoning cart: {str(e)}")
