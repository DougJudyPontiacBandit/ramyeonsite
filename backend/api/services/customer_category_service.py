from datetime import datetime
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)

class CustomerCategoryService:
    """
    Customer-facing category service (READ-ONLY)
    Only shows active categories with available products
    """
    
    def __init__(self):
        self.db = db_manager.get_database()
        self.category_collection = self.db.category
        self.product_collection = self.db.products
    
    # ================================================================
    # CORE CATEGORY BROWSING METHODS
    # ================================================================
    
    def get_all_active_categories(self):
        """
        Get all active categories for customer menu browsing
        
        Returns:
            dict: Success status and list of active categories
        """
        try:
            query = {
                'status': 'active',
                'isDeleted': {'$ne': True}
            }
            
            categories = list(self.category_collection.find(query, self._get_customer_safe_projection())
                            .sort('category_name', 1))
            
            # Enhance categories with product counts
            enhanced_categories = []
            for category in categories:
                # Count available products in this category
                product_count = self._count_available_products(category['_id'])
                
                category['product_count'] = product_count
                category['has_products'] = product_count > 0
                
                # Only include categories with available products
                if category['has_products']:
                    enhanced_categories.append(category)
            
            logger.info(f"Retrieved {len(enhanced_categories)} active categories with products")
            
            return {
                'success': True,
                'categories': enhanced_categories,
                'count': len(enhanced_categories)
            }
            
        except Exception as e:
            logger.error(f"Error getting active categories: {e}")
            return {
                'success': False,
                'message': f'Error retrieving categories: {str(e)}',
                'categories': []
            }
    
    def get_category_by_id(self, category_id):
        """
        Get single category details with subcategories
        
        Args:
            category_id (str): Category ID (CTGY-### format)
        
        Returns:
            dict: Success status and category details
        """
        try:
            if not category_id or not category_id.startswith('CTGY-'):
                return {
                    'success': False,
                    'message': 'Invalid category ID format'
                }
            
            query = {
                '_id': category_id,
                'status': 'active',
                'isDeleted': {'$ne': True}
            }
            
            category = self.category_collection.find_one(query, self._get_customer_safe_projection())
            
            if not category:
                logger.warning(f"Category {category_id} not found or not active")
                return {
                    'success': False,
                    'message': 'Category not found or currently unavailable'
                }
            
            # Count products in this category
            category['product_count'] = self._count_available_products(category_id)
            
            # Enhance subcategories with product counts
            if category.get('sub_categories'):
                enhanced_subcategories = []
                for subcat in category['sub_categories']:
                    subcat_product_count = self._count_available_products(
                        category_id, 
                        subcat.get('name')
                    )
                    subcat['product_count'] = subcat_product_count
                    
                    # Only include subcategories with products
                    if subcat_product_count > 0:
                        enhanced_subcategories.append(subcat)
                
                category['sub_categories'] = enhanced_subcategories
            
            logger.info(f"Retrieved category {category_id}: {category.get('category_name')}")
            
            return {
                'success': True,
                'category': category
            }
            
        except Exception as e:
            logger.error(f"Error getting category {category_id}: {e}")
            return {
                'success': False,
                'message': f'Error retrieving category: {str(e)}'
            }
    
    def get_category_with_products(self, category_id, subcategory_name=None, page=1, limit=20):
        """
        Get category with its available products
        
        Args:
            category_id (str): Category ID
            subcategory_name (str): Optional subcategory filter
            page (int): Page number for product pagination
            limit (int): Products per page
        
        Returns:
            dict: Category info with paginated products
        """
        try:
            # Get category details
            category_result = self.get_category_by_id(category_id)
            
            if not category_result['success']:
                return category_result
            
            category = category_result['category']
            
            # Get products in this category
            product_query = {
                'category_id': category_id,
                'status': 'active',
                'isDeleted': {'$ne': True},
                'stock': {'$gt': 0}
            }
            
            if subcategory_name:
                product_query['subcategory_name'] = subcategory_name
            
            # Calculate pagination
            skip = (page - 1) * limit
            
            products = list(self.product_collection.find(product_query)
                          .sort('product_name', 1)
                          .skip(skip)
                          .limit(limit))
            
            # Get total product count
            total_products = self.product_collection.count_documents(product_query)
            total_pages = (total_products + limit - 1) // limit
            
            logger.info(f"Retrieved category {category_id} with {len(products)} products")
            
            return {
                'success': True,
                'category': category,
                'products': products,
                'pagination': {
                    'current_page': page,
                    'total_pages': total_pages,
                    'total_count': total_products,
                    'has_next': page < total_pages,
                    'has_previous': page > 1,
                    'items_per_page': limit
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting category with products: {e}")
            return {
                'success': False,
                'message': f'Error retrieving category with products: {str(e)}'
            }
    
    # ================================================================
    # HELPER METHODS
    # ================================================================
    
    def _get_customer_safe_projection(self):
        """
        Return only customer-safe category fields
        
        Returns:
            dict: MongoDB projection for customer-safe fields
        """
        return {
            '_id': 1,
            'category_name': 1,
            'description': 1,
            'image_url': 1,
            'image_filename': 1,
            'sub_categories': 1,
            'status': 1
        }
    
    def _count_available_products(self, category_id, subcategory_name=None):
        """
        Count available products in category/subcategory
        
        Args:
            category_id (str): Category ID
            subcategory_name (str): Optional subcategory name
        
        Returns:
            int: Count of available products
        """
        try:
            query = {
                'category_id': category_id,
                'status': 'active',
                'isDeleted': {'$ne': True},
                'stock': {'$gt': 0}
            }
            
            if subcategory_name:
                query['subcategory_name'] = subcategory_name
            
            count = self.product_collection.count_documents(query)
            return count
            
        except Exception as e:
            logger.error(f"Error counting products: {e}")
            return 0