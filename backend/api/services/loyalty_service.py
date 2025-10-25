from datetime import datetime
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)

class LoyaltyService:
    """Loyalty Points Service for Customer Website"""
    
    def __init__(self):
        self.db = db_manager.get_database()
        self.customer_collection = self.db.customers
        self.loyalty_transactions = self.db.loyalty_transactions
    
    def get_customer_points(self, customer_id):
        """Get customer's current loyalty points"""
        try:
            customer = self.customer_collection.find_one({
                '_id': customer_id,
                'isDeleted': {'$ne': True}
            })
            
            if not customer:
                return None
                
            return {
                'customer_id': customer['_id'],
                'loyalty_points': customer.get('loyalty_points', 0),
                'email': customer.get('email'),
                'full_name': customer.get('full_name')
            }
        except Exception as e:
            logger.error(f"Error getting customer points: {str(e)}")
            raise Exception(f"Error getting customer points: {str(e)}")
    
    def calculate_points_earned(self, order_amount):
        """Calculate points to be earned from order (20% of order value)"""
        return int(order_amount * 0.20)
    
    def validate_points_redemption(self, customer_id, points_to_redeem):
        """Validate if customer can redeem points"""
        try:
            customer = self.customer_collection.find_one({
                '_id': customer_id,
                'isDeleted': {'$ne': True}
            })
            
            if not customer:
                return False, "Customer not found"
            
            current_points = customer.get('loyalty_points', 0)
            
            # Check minimum points (40 points = ₱10)
            if points_to_redeem < 40:
                return False, "Minimum 40 points required (₱10)"
            
            # Check maximum points per transaction (80 points = ₱20)
            if points_to_redeem > 80:
                return False, "Maximum 80 points per transaction (₱20)"
            
            # Check if customer has enough points
            if points_to_redeem > current_points:
                return False, "Insufficient points"
            
            return True, "Valid redemption"
            
        except Exception as e:
            logger.error(f"Error validating points redemption: {str(e)}")
            raise Exception(f"Error validating points redemption: {str(e)}")
    
    def redeem_points(self, customer_id, points_to_redeem, order_id):
        """Redeem customer points and update database"""
        try:
            # Validate redemption
            is_valid, message = self.validate_points_redemption(customer_id, points_to_redeem)
            if not is_valid:
                return False, message
            
            # Calculate discount amount (4 points = ₱1)
            discount_amount = points_to_redeem / 4
            
            # Update customer points in database
            result = self.customer_collection.update_one(
                {'_id': customer_id},
                {
                    '$inc': {'loyalty_points': -points_to_redeem},
                    '$set': {'last_updated': datetime.utcnow()}
                }
            )
            
            if result.modified_count == 0:
                return False, "Failed to update points"
            
            # Record transaction
            transaction = {
                'customer_id': customer_id,
                'order_id': order_id,
                'type': 'redemption',
                'points': -points_to_redeem,
                'discount_amount': discount_amount,
                'timestamp': datetime.utcnow(),
                'status': 'completed'
            }
            
            self.loyalty_transactions.insert_one(transaction)
            
            logger.info(f"Points redeemed: {points_to_redeem} points for customer {customer_id}")
            
            return True, {
                'points_redeemed': points_to_redeem,
                'discount_amount': discount_amount,
                'remaining_points': self.get_customer_points(customer_id)['loyalty_points']
            }
            
        except Exception as e:
            logger.error(f"Error redeeming points: {str(e)}")
            raise Exception(f"Error redeeming points: {str(e)}")
    
    def award_points(self, customer_id, order_amount, order_id):
        """Award points to customer after successful order"""
        try:
            points_earned = self.calculate_points_earned(order_amount)
            
            if points_earned <= 0:
                return True, "No points to award"
            
            # Update customer points in database
            result = self.customer_collection.update_one(
                {'_id': customer_id},
                {
                    '$inc': {'loyalty_points': points_earned},
                    '$set': {
                        'last_updated': datetime.utcnow(),
                        'last_purchase': datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count == 0:
                return False, "Failed to award points"
            
            # Record transaction
            transaction = {
                'customer_id': customer_id,
                'order_id': order_id,
                'type': 'earning',
                'points': points_earned,
                'order_amount': order_amount,
                'timestamp': datetime.utcnow(),
                'status': 'completed'
            }
            
            self.loyalty_transactions.insert_one(transaction)
            
            logger.info(f"Points awarded: {points_earned} points to customer {customer_id}")
            
            return True, {
                'points_earned': points_earned,
                'total_points': self.get_customer_points(customer_id)['loyalty_points']
            }
            
        except Exception as e:
            logger.error(f"Error awarding points: {str(e)}")
            raise Exception(f"Error awarding points: {str(e)}")
    
    def get_points_history(self, customer_id, limit=50):
        """Get customer's points transaction history"""
        try:
            transactions = list(self.loyalty_transactions.find(
                {'customer_id': customer_id}
            ).sort('timestamp', -1).limit(limit))
            
            return [{
                'type': t['type'],
                'points': t['points'],
                'order_id': t.get('order_id'),
                'timestamp': t['timestamp'],
                'discount_amount': t.get('discount_amount'),
                'order_amount': t.get('order_amount')
            } for t in transactions]
            
        except Exception as e:
            logger.error(f"Error getting points history: {str(e)}")
            raise Exception(f"Error getting points history: {str(e)}")






