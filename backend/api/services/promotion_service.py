from bson import ObjectId
from datetime import datetime, timezone
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)

class PromotionService:
    """Customer-facing Promotions Service"""
    
    def __init__(self):
        self.db = db_manager.get_database()
        self.collection = self.db.promotions
    
    def _serialize_promotion_data(self, promotion):
        """Convert MongoDB ObjectIds and dates to JSON-serializable format"""
        if promotion:
            if '_id' in promotion:
                promotion['_id'] = str(promotion['_id'])
            
            # Convert datetime objects to ISO strings
            for field in ['start_date', 'end_date', 'created_at', 'updated_at', 'activated_at', 'deactivated_at', 'deleted_at']:
                if field in promotion and promotion[field]:
                    if hasattr(promotion[field], 'isoformat'):
                        promotion[field] = promotion[field].isoformat()
            
            # Handle target_ids
            if 'target_ids' in promotion and promotion['target_ids']:
                promotion['target_ids'] = [
                    str(id) if hasattr(id, '__str__') else id 
                    for id in promotion['target_ids']
                ]
        
        return promotion
    
    def get_active_promotions(self):
        """Get all active promotions for customers"""
        try:
            now = datetime.now(timezone.utc)
            
            active_promotions = list(self.collection.find({
                'isDeleted': {'$ne': True},
                'status': 'active',
                'start_date': {'$lte': now},
                'end_date': {'$gte': now}
            }).sort('created_at', -1))
            
            # Serialize all promotions
            serialized_promotions = [
                self._serialize_promotion_data(promo.copy()) 
                for promo in active_promotions
            ]
            
            return {
                'success': True,
                'promotions': serialized_promotions,
                'count': len(serialized_promotions)
            }
            
        except Exception as e:
            logger.error(f"Error getting active promotions: {e}")
            return {
                'success': False,
                'message': f'Error retrieving active promotions: {str(e)}',
                'promotions': [],
                'count': 0
            }
    
    def get_promotion_by_id(self, promotion_id):
        """Get specific promotion by ID"""
        try:
            promotion = self.collection.find_one({'promotion_id': promotion_id})
            
            if not promotion:
                return {'success': False, 'message': 'Promotion not found'}
            
            # Check if deleted or not active
            if promotion.get('isDeleted'):
                return {'success': False, 'message': 'Promotion not available'}
            
            if promotion.get('status') != 'active':
                return {'success': False, 'message': 'Promotion is not currently active'}
            
            # Add computed fields
            now = datetime.now(timezone.utc)
            promotion['is_expired'] = now > promotion['end_date']
            promotion['is_active'] = (
                promotion['status'] == 'active' and 
                promotion['start_date'] <= now <= promotion['end_date']
            )
            promotion['days_remaining'] = (promotion['end_date'] - now).days if not promotion['is_expired'] else 0
            
            if promotion.get('usage_limit'):
                promotion['usage_percentage'] = (
                    promotion['current_usage'] / promotion['usage_limit'] * 100
                )
            else:
                promotion['usage_percentage'] = 0
            
            return {
                'success': True,
                'promotion': self._serialize_promotion_data(promotion)
            }
            
        except Exception as e:
            logger.error(f"Error getting promotion {promotion_id}: {e}")
            return {
                'success': False,
                'message': f'Error retrieving promotion: {str(e)}'
            }
    
    def get_all_promotions(self, filters=None, page=1, limit=20, sort_by='created_at', sort_order='desc'):
        """List all available promotions with filtering and pagination"""
        try:
            # Build query - exclude deleted by default
            query = {'isDeleted': {'$ne': True}}
            
            # Only show active promotions for customers
            query['status'] = 'active'
            
            # Date filter - only show current promotions
            now = datetime.now(timezone.utc)
            query['start_date'] = {'$lte': now}
            query['end_date'] = {'$gte': now}
            
            # Apply additional filters if provided
            if filters:
                if filters.get('type'):
                    query['type'] = filters['type']
                
                if filters.get('target_type'):
                    query['target_type'] = filters['target_type']
                
                # Search by name or description
                if filters.get('search_query'):
                    query['$or'] = [
                        {'name': {'$regex': filters['search_query'], '$options': 'i'}},
                        {'description': {'$regex': filters['search_query'], '$options': 'i'}}
                    ]
            
            # Calculate pagination
            skip = (page - 1) * limit
            
            # Sort configuration
            sort_direction = -1 if sort_order.lower() == 'desc' else 1
            
            # Execute query
            promotions = list(self.collection.find(query)
                            .sort(sort_by, sort_direction)
                            .skip(skip)
                            .limit(limit))
            
            # Serialize all promotions
            serialized_promotions = [
                self._serialize_promotion_data(promo.copy()) 
                for promo in promotions
            ]
            
            # Get total count for pagination
            total_count = self.collection.count_documents(query)
            total_pages = (total_count + limit - 1) // limit
            
            return {
                'success': True,
                'promotions': serialized_promotions,
                'pagination': {
                    'current_page': page,
                    'total_pages': total_pages,
                    'total_count': total_count,
                    'has_next': page < total_pages,
                    'has_previous': page > 1
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting promotions: {e}")
            return {
                'success': False,
                'message': f'Error retrieving promotions: {str(e)}',
                'promotions': [],
                'pagination': {
                    'current_page': page,
                    'total_pages': 0,
                    'total_count': 0,
                    'has_next': False,
                    'has_previous': False
                }
            }
    
    def get_promotions_by_product(self, product_id):
        """Get all active promotions applicable to a specific product"""
        try:
            now = datetime.now(timezone.utc)
            
            query = {
                'isDeleted': {'$ne': True},
                'status': 'active',
                'start_date': {'$lte': now},
                'end_date': {'$gte': now},
                '$or': [
                    {'target_type': 'all'},
                    {'target_type': 'products', 'target_ids': product_id}
                ]
            }
            
            promotions = list(self.collection.find(query).sort('discount_value', -1))
            
            serialized_promotions = [
                self._serialize_promotion_data(promo.copy()) 
                for promo in promotions
            ]
            
            return {
                'success': True,
                'promotions': serialized_promotions,
                'count': len(serialized_promotions)
            }
            
        except Exception as e:
            logger.error(f"Error getting promotions for product {product_id}: {e}")
            return {
                'success': False,
                'message': f'Error retrieving promotions: {str(e)}',
                'promotions': [],
                'count': 0
            }
    
    def get_promotions_by_category(self, category_id):
        """Get all active promotions applicable to a specific category"""
        try:
            now = datetime.now(timezone.utc)
            
            query = {
                'isDeleted': {'$ne': True},
                'status': 'active',
                'start_date': {'$lte': now},
                'end_date': {'$gte': now},
                '$or': [
                    {'target_type': 'all'},
                    {'target_type': 'categories', 'target_ids': category_id}
                ]
            }
            
            promotions = list(self.collection.find(query).sort('discount_value', -1))
            
            serialized_promotions = [
                self._serialize_promotion_data(promo.copy()) 
                for promo in promotions
            ]
            
            return {
                'success': True,
                'promotions': serialized_promotions,
                'count': len(serialized_promotions)
            }
            
        except Exception as e:
            logger.error(f"Error getting promotions for category {category_id}: {e}")
            return {
                'success': False,
                'message': f'Error retrieving promotions: {str(e)}',
                'promotions': [],
                'count': 0
            }
    
    def calculate_discount_for_order(self, order_data):
        """Calculate best discount for an order (read-only, no tracking)"""
        try:
            # Get active promotions
            active_result = self.get_active_promotions()
            
            if not active_result['success'] or not active_result['promotions']:
                return {
                    'success': True,
                    'discount_applied': 0.0,
                    'promotion_used': None,
                    'message': 'No active promotions available'
                }
            
            best_promotion = None
            best_discount = 0.0
            
            # Evaluate each promotion
            for promotion in active_result['promotions']:
                discount = self._calculate_promotion_discount(promotion, order_data)
                
                if discount > best_discount and self._check_usage_limit(promotion):
                    best_promotion = promotion
                    best_discount = discount
            
            if not best_promotion:
                return {
                    'success': True,
                    'discount_applied': 0.0,
                    'promotion_used': None,
                    'message': 'No applicable promotions for this order'
                }
            
            return {
                'success': True,
                'discount_applied': best_discount,
                'promotion_used': best_promotion,
                'message': f'Promotion {best_promotion["promotion_id"]} applied'
            }
            
        except Exception as e:
            logger.error(f"Error calculating discount for order: {e}")
            return {
                'success': False,
                'message': f'Error calculating discount: {str(e)}',
                'discount_applied': 0.0,
                'promotion_used': None
            }
    
    def _calculate_promotion_discount(self, promotion, order_data):
        """Calculate discount amount based on promotion type"""
        try:
            if not self._is_order_eligible(promotion, order_data):
                return 0.0
            
            eligible_amount = self._get_eligible_order_amount(promotion, order_data)
            
            if promotion['type'] == 'percentage':
                return eligible_amount * (promotion['discount_value'] / 100)
            
            elif promotion['type'] == 'fixed_amount':
                return min(promotion['discount_value'], eligible_amount)
            
            elif promotion['type'] == 'buy_x_get_y':
                return self._calculate_bxgy_discount(promotion, order_data)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating promotion discount: {e}")
            return 0.0
    
    def _is_order_eligible(self, promotion, order_data):
        """Check if order qualifies for promotion"""
        try:
            if promotion['target_type'] == 'all':
                return len(order_data.get('items', [])) > 0
            
            elif promotion['target_type'] == 'products':
                order_product_ids = [str(item.get('product_id')) for item in order_data.get('items', [])]
                return any(str(product_id) in order_product_ids for product_id in promotion['target_ids'])
            
            elif promotion['target_type'] == 'categories':
                order_category_ids = [str(item.get('category_id')) for item in order_data.get('items', []) if item.get('category_id')]
                return any(str(category_id) in order_category_ids for category_id in promotion['target_ids'])
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking order eligibility: {e}")
            return False
    
    def _get_eligible_order_amount(self, promotion, order_data):
        """Get portion of order eligible for discount"""
        try:
            eligible_amount = 0.0
            
            if promotion['target_type'] == 'all':
                return float(order_data.get('total_amount', 0))
            
            for item in order_data.get('items', []):
                item_eligible = False
                
                if promotion['target_type'] == 'products':
                    item_eligible = str(item.get('product_id')) in [str(pid) for pid in promotion['target_ids']]
                elif promotion['target_type'] == 'categories':
                    item_eligible = str(item.get('category_id')) in [str(cid) for cid in promotion['target_ids']]
                
                if item_eligible:
                    eligible_amount += float(item.get('price', 0)) * int(item.get('quantity', 1))
            
            return eligible_amount
            
        except Exception as e:
            logger.error(f"Error calculating eligible order amount: {e}")
            return 0.0
    
    def _calculate_bxgy_discount(self, promotion, order_data):
        """Calculate Buy X Get Y discount"""
        try:
            discount_config = promotion.get('discount_config', {})
            buy_quantity = discount_config.get('buy_quantity', 2)
            get_quantity = discount_config.get('get_quantity', 1)
            
            eligible_items = []
            for item in order_data.get('items', []):
                if promotion['target_type'] == 'all' or \
                   (promotion['target_type'] == 'products' and str(item.get('product_id')) in [str(pid) for pid in promotion['target_ids']]) or \
                   (promotion['target_type'] == 'categories' and str(item.get('category_id')) in [str(cid) for cid in promotion['target_ids']]):
                    eligible_items.extend([item] * int(item.get('quantity', 1)))
            
            if len(eligible_items) < buy_quantity:
                return 0.0
            
            # Sort by price (lowest first for maximum customer benefit)
            eligible_items.sort(key=lambda x: float(x.get('price', 0)))
            
            # Calculate how many free items customer gets
            sets_qualified = len(eligible_items) // (buy_quantity + get_quantity)
            free_items = sets_qualified * get_quantity
            
            # Calculate discount (sum of cheapest items that are free)
            discount = sum(float(item.get('price', 0)) for item in eligible_items[:free_items])
            
            return discount
            
        except Exception as e:
            logger.error(f"Error calculating BXGY discount: {e}")
            return 0.0
    
    def _check_usage_limit(self, promotion):
        """Check if promotion usage limit reached"""
        try:
            usage_limit = promotion.get('usage_limit')
            if not usage_limit:
                return True  # No limit set
            
            current_usage = promotion.get('current_usage', 0)
            return current_usage < usage_limit
            
        except Exception as e:
            logger.error(f"Error checking usage limit: {e}")
            return False