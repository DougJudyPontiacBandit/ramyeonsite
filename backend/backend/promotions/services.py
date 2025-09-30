from bson import ObjectId
from datetime import datetime
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)

class PromotionService:
    def __init__(self):
        self.db = db_manager.get_database()
        self.promotion_collection = self.db.promotions

    def get_all_promotions(self, include_deleted=False):
        """Get all promotions"""
        try:
            query = {}
            if not include_deleted:
                query['isDeleted'] = {'$ne': True}

            promotions = list(self.promotion_collection.find(query))
            return promotions
        except Exception as e:
            raise Exception(f"Error getting promotions: {str(e)}")

    def get_promotion_by_id(self, promotion_id, include_deleted=False):
        """Get promotion by ID"""
        try:
            if not promotion_id:
                return None

            query = {'_id': ObjectId(promotion_id)}
            if not include_deleted:
                query['isDeleted'] = {'$ne': True}

            return self.promotion_collection.find_one(query)
        except Exception as e:
            raise Exception(f"Error getting promotion: {str(e)}")

    def create_promotion(self, promotion_data, current_user=None):
        """Create new promotion"""
        try:
            now = datetime.utcnow()

            promotion = {
                'promotion_name': promotion_data.get('promotion_name', ''),
                'discount_type': promotion_data.get('discount_type', ''),
                'discount_value': promotion_data.get('discount_value', 0),
                'applicable_products': promotion_data.get('applicable_products', []),
                'start_date': promotion_data.get('start_date'),
                'end_date': promotion_data.get('end_date'),
                'status': promotion_data.get('status', 'active'),
                'isDeleted': False,
                'date_created': now,
                'last_updated': now
            }

            # Generate QR code
            import uuid
            promotion['qr_code'] = f"PROMO-{str(ObjectId())[:8]}-{str(uuid.uuid4())[:8]}".upper()

            result = self.promotion_collection.insert_one(promotion)
            promotion['_id'] = result.inserted_id

            return promotion
        except Exception as e:
            raise Exception(f"Error creating promotion: {str(e)}")

    def update_promotion(self, promotion_id, promotion_data, current_user=None):
        """Update promotion"""
        try:
            if not promotion_id:
                return None

            update_data = promotion_data.copy()
            update_data['last_updated'] = datetime.utcnow()

            result = self.promotion_collection.update_one(
                {'_id': ObjectId(promotion_id), 'isDeleted': {'$ne': True}},
                {'$set': update_data}
            )

            if result.modified_count == 0:
                return None

            return self.promotion_collection.find_one({'_id': ObjectId(promotion_id)})
        except Exception as e:
            raise Exception(f"Error updating promotion: {str(e)}")

    def delete_promotion(self, promotion_id, current_user=None):
        """Soft delete promotion"""
        try:
            result = self.promotion_collection.update_one(
                {'_id': ObjectId(promotion_id)},
                {'$set': {'isDeleted': True, 'last_updated': datetime.utcnow()}}
            )

            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Error deleting promotion: {str(e)}")

    def get_promotion_by_qr_code(self, qr_code, include_deleted=False):
        """Get promotion by QR code"""
        try:
            if not qr_code:
                return None

            query = {'qr_code': qr_code.strip()}
            if not include_deleted:
                query['isDeleted'] = {'$ne': True}

            return self.promotion_collection.find_one(query)
        except Exception as e:
            raise Exception(f"Error getting promotion by QR code: {str(e)}")

    def regenerate_qr_code(self, promotion_id, current_user=None):
        """Regenerate QR code for promotion"""
        try:
            if not promotion_id:
                return None

            # Generate new QR code
            import uuid
            new_qr_code = f"PROMO-{promotion_id[:8]}-{str(uuid.uuid4())[:8]}".upper()

            result = self.promotion_collection.update_one(
                {'_id': ObjectId(promotion_id), 'isDeleted': {'$ne': True}},
                {
                    '$set': {
                        'qr_code': new_qr_code,
                        'last_updated': datetime.utcnow()
                    }
                }
            )

            if result.modified_count == 0:
                return None

            return self.promotion_collection.find_one({'_id': ObjectId(promotion_id)})
        except Exception as e:
            raise Exception(f"Error regenerating QR code: {str(e)}")

    def get_active_promotions(self):
        """Get all active promotions (not deleted and status=active)"""
        try:
            now = datetime.utcnow()
            query = {
                'isDeleted': {'$ne': True},
                'status': 'active',
                'start_date': {'$lte': now},
                'end_date': {'$gte': now}
            }

            promotions = list(self.promotion_collection.find(query))
            return promotions
        except Exception as e:
            raise Exception(f"Error getting active promotions: {str(e)}")

    def calculate_discount(self, promotion, cart_items):
        """Calculate discount based on promotion and cart items"""
        try:
            discount_type = promotion.get('discount_type', '')
            discount_value = promotion.get('discount_value', 0)
            applicable_products = promotion.get('applicable_products', [])

            if discount_type == 'percentage':
                # Calculate total cart value
                total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
                discount = (total * discount_value) / 100
            elif discount_type == 'fixed':
                # Fixed discount on total
                total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items)
                discount = min(discount_value, total)  # Don't exceed total
            elif discount_type == 'product_specific' and applicable_products:
                # Discount only on specific products
                discounted_total = 0
                for item in cart_items:
                    if str(item.get('id')) in applicable_products:
                        discounted_total += item.get('price', 0) * item.get('quantity', 1)
                discount = (discounted_total * discount_value) / 100 if discount_type == 'percentage' else discount_value
            else:
                discount = 0

            return round(discount, 2)
        except Exception as e:
            raise Exception(f"Error calculating discount: {str(e)}")
