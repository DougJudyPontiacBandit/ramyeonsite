from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..decorators.authenticationDecorator import require_authentication
import logging

logger = logging.getLogger(__name__)

class HomepageDataView(APIView):
    """View for homepage data"""
    def get(self, request):
        """Get homepage data including featured products, promotions, etc."""
        try:
            # Mock homepage data
            homepage_data = {
                "hero": {
                    "title": "Welcome to Ramyeon Corner",
                    "subtitle": "Authentic Korean Street Food",
                    "image": "/images/hero-ramyeon.jpg",
                    "cta_text": "Order Now",
                    "cta_link": "/menu"
                },
                "featured_products": [
                    {
                        "id": "1",
                        "name": "Shin Ramyun",
                        "description": "Spicy Korean instant noodles",
                        "price": 150.00,
                        "image": "/images/shin-ramyun.jpg",
                        "category": "ramyeon",
                        "rating": 4.5,
                        "is_featured": True
                    },
                    {
                        "id": "2",
                        "name": "Tteokbokki",
                        "description": "Spicy rice cakes",
                        "price": 120.00,
                        "image": "/images/tteokbokki.jpg",
                        "category": "tteokbokki",
                        "rating": 4.7,
                        "is_featured": True
                    },
                    {
                        "id": "3",
                        "name": "Bulgogi",
                        "description": "Marinated beef",
                        "price": 200.00,
                        "image": "/images/bulgogi.jpg",
                        "category": "meat",
                        "rating": 4.8,
                        "is_featured": True
                    }
                ],
                "categories": [
                    {
                        "id": "ramyeon",
                        "name": "Ramyeon",
                        "image": "/images/category-ramyeon.jpg",
                        "item_count": 15
                    },
                    {
                        "id": "tteokbokki",
                        "name": "Tteokbokki",
                        "image": "/images/category-tteokbokki.jpg",
                        "item_count": 8
                    },
                    {
                        "id": "meat",
                        "name": "Meat Dishes",
                        "image": "/images/category-meat.jpg",
                        "item_count": 12
                    },
                    {
                        "id": "sides",
                        "name": "Sides",
                        "image": "/images/category-sides.jpg",
                        "item_count": 20
                    }
                ],
                "promotions": [
                    {
                        "id": "1",
                        "title": "Weekend Special",
                        "description": "20% off on all ramyeon",
                        "discount": "20%",
                        "valid_until": "2024-12-31",
                        "image": "/images/promo-weekend.jpg"
                    },
                    {
                        "id": "2",
                        "title": "Student Discount",
                        "description": "15% off with student ID",
                        "discount": "15%",
                        "valid_until": "2024-12-31",
                        "image": "/images/promo-student.jpg"
                    }
                ],
                "stats": {
                    "total_orders": 12543,
                    "happy_customers": 8921,
                    "menu_items": 45,
                    "years_experience": 5
                },
                "testimonials": [
                    {
                        "id": "1",
                        "name": "Sarah Kim",
                        "rating": 5,
                        "comment": "Best Korean food in town! The Shin Ramyun is amazing.",
                        "date": "2024-01-15"
                    },
                    {
                        "id": "2",
                        "name": "Mike Johnson",
                        "rating": 5,
                        "comment": "Great service and delicious food. Will definitely order again!",
                        "date": "2024-01-10"
                    }
                ]
            }

            return Response(homepage_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting homepage data: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HomepageStatsView(APIView):
    """View for homepage statistics"""
    def get(self, request):
        """Get homepage statistics"""
        try:
            # Mock statistics
            stats = {
                "total_orders": 12543,
                "total_customers": 8921,
                "total_products": 45,
                "total_revenue": 1254300.00,
                "average_order_value": 100.00,
                "customer_satisfaction": 4.7,
                "popular_category": "ramyeon",
                "busiest_day": "Friday"
            }

            return Response({
                "stats": stats
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting homepage stats: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FeaturedProductsView(APIView):
    """View for featured products"""
    def get(self, request):
        """Get featured products for homepage"""
        try:
            # Mock featured products
            featured_products = [
                {
                    "id": "1",
                    "name": "Shin Ramyun",
                    "description": "Spicy Korean instant noodles",
                    "price": 150.00,
                    "original_price": 180.00,
                    "image": "/images/shin-ramyun.jpg",
                    "category": "ramyeon",
                    "rating": 4.5,
                    "reviews_count": 128,
                    "is_featured": True,
                    "is_on_sale": True,
                    "discount_percentage": 17
                },
                {
                    "id": "2",
                    "name": "Tteokbokki",
                    "description": "Spicy rice cakes with fish cakes",
                    "price": 120.00,
                    "image": "/images/tteokbokki.jpg",
                    "category": "tteokbokki",
                    "rating": 4.7,
                    "reviews_count": 95,
                    "is_featured": True,
                    "is_on_sale": False
                },
                {
                    "id": "3",
                    "name": "Bulgogi Bowl",
                    "description": "Marinated beef with rice",
                    "price": 200.00,
                    "image": "/images/bulgogi.jpg",
                    "category": "meat",
                    "rating": 4.8,
                    "reviews_count": 76,
                    "is_featured": True,
                    "is_on_sale": False
                }
            ]

            return Response({
                "featured_products": featured_products
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting featured products: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HomepagePromotionsView(APIView):
    """View for active promotions on homepage"""
    def get(self, request):
        """Get active promotions for homepage"""
        try:
            # Mock promotions
            promotions = [
                {
                    "id": "1",
                    "title": "Weekend Special",
                    "description": "20% off on all ramyeon dishes",
                    "discount_type": "percentage",
                    "discount_value": 20,
                    "minimum_order": 0,
                    "categories": ["ramyeon"],
                    "valid_from": "2024-01-01",
                    "valid_until": "2024-12-31",
                    "image": "/images/promo-weekend.jpg",
                    "is_active": True
                },
                {
                    "id": "2",
                    "title": "Student Discount",
                    "description": "15% off with valid student ID",
                    "discount_type": "percentage",
                    "discount_value": 15,
                    "minimum_order": 100,
                    "categories": ["all"],
                    "valid_from": "2024-01-01",
                    "valid_until": "2024-12-31",
                    "image": "/images/promo-student.jpg",
                    "is_active": True,
                    "requires_verification": True
                },
                {
                    "id": "3",
                    "title": "First Order Bonus",
                    "description": "Free delivery on first order",
                    "discount_type": "free_delivery",
                    "discount_value": 50,  # delivery fee
                    "minimum_order": 0,
                    "categories": ["all"],
                    "valid_from": "2024-01-01",
                    "valid_until": "2024-12-31",
                    "image": "/images/promo-first-order.jpg",
                    "is_active": True,
                    "first_time_only": True
                }
            ]

            return Response({
                "promotions": promotions
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting homepage promotions: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
