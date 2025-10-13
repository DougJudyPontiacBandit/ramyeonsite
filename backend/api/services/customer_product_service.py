from datetime import datetime
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)

class CustomerProductService:
    """
    Customer-facing product service (READ-ONLY)
    Only shows active, in-stock products with customer-safe fields
    """
    
    def __init__(self):
        self.db = db_manager.get_database()
        self.product_collection = self.db.products
        self.category_collection = self.db.category
        self.promotion_collection = self.db.promotions
    
    # ================================================================
    # CORE PRODUCT BROWSING METHODS
    # ================================================================
    
    def get_all_active_products(self, filters=None, page=1, limit=20, sort_by='product_name', sort_order='asc'):
        """
        Get all active products available for customers
        
        Args:
            filters (dict): Optional filters (category_id, subcategory_name, search)
            page (int): Page number for pagination
            limit (int): Items per page
            sort_by (str): Field to sort by
            sort_order (str): 'asc' or 'desc'
        
        Returns:
            dict: Success status, products list, and pagination info
        """
        try:
            # Base query - only active, in-stock, non-deleted products
            query = {
                'status': 'active',
                'isDeleted': {'$ne': True},
                'stock': {'$gt': 0}  # Only show products with stock
            }
            
            # Apply filters
            if filters:
                # Category filter
                if filters.get('category_id'):
                    query['category_id'] = filters['category_id']
                
                # Subcategory filter
                if filters.get('subcategory_name'):
                    query['subcategory_name'] = filters['subcategory_name']
                
                # Search filter (product name or SKU)
                if filters.get('search'):
                    search_regex = {'$regex': filters['search'], '$options': 'i'}
                    query['$or'] = [
                        {'product_name': search_regex},
                        {'SKU': search_regex}
                    ]
                
                # Price range filter
                if filters.get('min_price') or filters.get('max_price'):
                    price_filter = {}
                    if filters.get('min_price'):
                        price_filter['$gte'] = float(filters['min_price'])
                    if filters.get('max_price'):
                        price_filter['$lte'] = float(filters['max_price'])
                    if price_filter:
                        query['selling_price'] = price_filter
            
            # Calculate pagination
            skip = (page - 1) * limit
            
            # Sort configuration
            sort_direction = 1 if sort_order.lower() == 'asc' else -1
            
            # Execute query
            products = list(self.product_collection.find(query, self._get_customer_safe_projection())
                          .sort(sort_by, sort_direction)
                          .skip(skip)
                          .limit(limit))
            
            # Get total count for pagination
            total_count = self.product_collection.count_documents(query)
            total_pages = (total_count + limit - 1) // limit
            
            # Enhance products with promotion info
            enhanced_products = []
            for product in products:
                enhanced_product = self._enhance_product_with_promotions(product)
                enhanced_products.append(enhanced_product)
            
            logger.info(f"Retrieved {len(enhanced_products)} active products (page {page}/{total_pages})")
            
            return {
                'success': True,
                'products': enhanced_products,
                'pagination': {
                    'current_page': page,
                    'total_pages': total_pages,
                    'total_count': total_count,
                    'has_next': page < total_pages,
                    'has_previous': page > 1,
                    'items_per_page': limit
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting active products: {e}")
            return {
                'success': False,
                'message': f'Error retrieving products: {str(e)}',
                'products': [],
                'pagination': {}
            }
    
    def get_product_by_id(self, product_id):
        """
        Get single product details for customer view
        
        Args:
            product_id (str): Product ID (PROD-##### format)
        
        Returns:
            dict: Success status and product details with promotions
        """
        try:
            if not product_id or not product_id.startswith('PROD-'):
                return {
                    'success': False,
                    'message': 'Invalid product ID format'
                }
            
            # Query for active, in-stock product
            query = {
                '_id': product_id,
                'status': 'active',
                'isDeleted': {'$ne': True},
                'stock': {'$gt': 0}
            }
            
            product = self.product_collection.find_one(query, self._get_customer_safe_projection())
            
            if not product:
                logger.warning(f"Product {product_id} not found or not available")
                return {
                    'success': False,
                    'message': 'Product not found or currently unavailable'
                }
            
            # Enhance with promotion info
            enhanced_product = self._enhance_product_with_promotions(product)
            
            logger.info(f"Retrieved product {product_id}: {enhanced_product.get('product_name')}")
            
            return {
                'success': True,
                'product': enhanced_product
            }
            
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return {
                'success': False,
                'message': f'Error retrieving product: {str(e)}'
            }
    
    def search_products(self, search_term, page=1, limit=20):
        """
        Search products by name or SKU
        
        Args:
            search_term (str): Search query
            page (int): Page number
            limit (int): Items per page
        
        Returns:
            dict: Success status and matching products
        """
        try:
            if not search_term or not search_term.strip():
                return {
                    'success': False,
                    'message': 'Search term is required',
                    'products': []
                }
            
            filters = {'search': search_term.strip()}
            result = self.get_all_active_products(filters=filters, page=page, limit=limit)
            
            logger.info(f"Search for '{search_term}' returned {len(result.get('products', []))} results")
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return {
                'success': False,
                'message': f'Search error: {str(e)}',
                'products': []
            }
    
    def get_products_by_category(self, category_id, subcategory_name=None, page=1, limit=20):
        """
        Get products by category and optional subcategory
        
        Args:
            category_id (str): Category ID (CTGY-### format)
            subcategory_name (str): Optional subcategory name
            page (int): Page number
            limit (int): Items per page
        
        Returns:
            dict: Success status and filtered products
        """
        try:
            if not category_id or not category_id.startswith('CTGY-'):
                return {
                    'success': False,
                    'message': 'Invalid category ID format',
                    'products': []
                }
            
            filters = {'category_id': category_id}
            if subcategory_name:
                filters['subcategory_name'] = subcategory_name
            
            result = self.get_all_active_products(filters=filters, page=page, limit=limit)
            
            logger.info(f"Retrieved products for category {category_id}" + 
                       (f" > {subcategory_name}" if subcategory_name else ""))
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            return {
                'success': False,
                'message': f'Error retrieving category products: {str(e)}',
                'products': []
            }
    
    def get_featured_products(self, limit=10):
        """
        Get featured/popular products for homepage
        
        Args:
            limit (int): Number of featured products to return
        
        Returns:
            dict: Success status and featured products
        """
        try:
            # Query for active, in-stock products sorted by creation date (newest first)
            # You can customize this logic based on your business needs
            query = {
                'status': 'active',
                'isDeleted': {'$ne': True},
                'stock': {'$gt': 0}
            }
            
            products = list(self.product_collection.find(query, self._get_customer_safe_projection())
                          .sort('created_at', -1)
                          .limit(limit))
            
            # Enhance with promotions
            enhanced_products = []
            for product in products:
                enhanced_product = self._enhance_product_with_promotions(product)
                enhanced_products.append(enhanced_product)
            
            logger.info(f"Retrieved {len(enhanced_products)} featured products")
            
            return {
                'success': True,
                'products': enhanced_products,
                'count': len(enhanced_products)
            }
            
        except Exception as e:
            logger.error(f"Error getting featured products: {e}")
            return {
                'success': False,
                'message': f'Error retrieving featured products: {str(e)}',
                'products': []
            }
    
    # ================================================================
    # HELPER METHODS
    # ================================================================
    
    def _get_customer_safe_projection(self):
        """
        Return only customer-safe fields (exclude admin-only data)
        
        Returns:
            dict: MongoDB projection for customer-safe fields
        """
        # ✅ FIX: Use ONLY inclusions (no exclusions mixed in)
        return {
            '_id': 1,
            'product_name': 1,
            'category_id': 1,
            'subcategory_name': 1,
            'SKU': 1,
            'unit': 1,
            'stock': 1,
            'selling_price': 1,
            'description': 1,
            'barcode': 1,
            'image': 1,
            'image_url': 1,
            'image_filename': 1,
            'status': 1,
            'created_at': 1,
            'updated_at': 1
            # ❌ REMOVED: All exclusions (cost_price: 0, supplier_id: 0, etc.)
            # MongoDB doesn't allow mixing inclusion and exclusion
        }
        
    def _enhance_product_with_promotions(self, product):
        """
        Add active promotion information to product
        
        Args:
            product (dict): Product document
        
        Returns:
            dict: Product with promotion info added
        """
        try:
            product_id = product.get('_id')
            category_id = product.get('category_id')
            
            now = datetime.utcnow()
            
            # Find active promotions that apply to this product
            promotion_query = {
                'status': 'active',
                'isDeleted': {'$ne': True},
                'start_date': {'$lte': now},
                'end_date': {'$gte': now},
                '$or': [
                    {'target_type': 'all'},
                    {'target_type': 'products', 'target_ids': product_id},
                    {'target_type': 'categories', 'target_ids': category_id}
                ]
            }
            
            active_promotions = list(self.promotion_collection.find(promotion_query).limit(5))
            
            if active_promotions:
                # Add promotion info to product
                product['has_promotion'] = True
                product['promotions'] = []
                
                for promo in active_promotions:
                    product['promotions'].append({
                        'promotion_id': promo.get('promotion_id'),
                        'name': promo.get('name'),
                        'type': promo.get('type'),
                        'discount_value': promo.get('discount_value'),
                        'end_date': promo.get('end_date').isoformat() if promo.get('end_date') else None
                    })
                
                # Calculate potential discount for display
                best_discount = self._calculate_best_discount(product, active_promotions)
                if best_discount > 0:
                    product['discounted_price'] = product['selling_price'] - best_discount
                    product['savings'] = best_discount
            else:
                product['has_promotion'] = False
                product['promotions'] = []
            
            return product
            
        except Exception as e:
            logger.error(f"Error enhancing product with promotions: {e}")
            # Return product without promotion info if error occurs
            product['has_promotion'] = False
            product['promotions'] = []
            return product
    
    def _calculate_best_discount(self, product, promotions):
        """
        Calculate the best discount amount from available promotions
        
        Args:
            product (dict): Product document
            promotions (list): List of applicable promotions
        
        Returns:
            float: Best discount amount
        """
        try:
            best_discount = 0.0
            selling_price = float(product.get('selling_price', 0))
            
            for promo in promotions:
                discount = 0.0
                
                if promo['type'] == 'percentage':
                    discount = selling_price * (promo['discount_value'] / 100)
                elif promo['type'] == 'fixed_amount':
                    discount = min(promo['discount_value'], selling_price)
                
                if discount > best_discount:
                    best_discount = discount
            
            return best_discount
            
        except Exception as e:
            logger.error(f"Error calculating discount: {e}")
            return 0.0