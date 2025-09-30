from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Newsletter
from ..decorators.authenticationDecorator import require_authentication
import logging

logger = logging.getLogger(__name__)

class NewsletterSubscribeView(APIView):
    """View for newsletter subscription"""
    def post(self, request):
        """Subscribe to newsletter"""
        try:
            email = request.data.get('email', '').strip()
            preferences = request.data.get('preferences', {})
            source = request.data.get('source', 'website')

            if not email:
                return Response(
                    {"error": "Email is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if already subscribed
            # In a real implementation, you'd query the database
            # For now, we'll create a new subscription

            newsletter = Newsletter(
                email=email,
                subscribed=True,
                preferences=preferences,
                source=source
            )

            # Here you would save to database
            # newsletter_data = newsletter.to_dict()
            # db.collection.insert_one(newsletter_data)

            return Response({
                "message": "Successfully subscribed to newsletter",
                "email": email,
                "preferences": preferences
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error subscribing to newsletter: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NewsletterUnsubscribeView(APIView):
    """View for newsletter unsubscription"""
    def post(self, request):
        """Unsubscribe from newsletter"""
        try:
            email = request.data.get('email', '').strip()

            if not email:
                return Response(
                    {"error": "Email is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # In a real implementation, you'd find and update the subscription
            # newsletter = db.collection.find_one({"email": email})
            # if newsletter:
            #     newsletter_obj = Newsletter.from_dict(newsletter)
            #     newsletter_obj.unsubscribe()
            #     db.collection.update_one({"email": email}, {"$set": newsletter_obj.to_dict()})

            return Response({
                "message": "Successfully unsubscribed from newsletter",
                "email": email
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error unsubscribing from newsletter: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NewsletterListView(APIView):
    """View for listing newsletter subscriptions"""
    @require_authentication
    def get(self, request):
        """Get newsletter subscriptions (admin only)"""
        try:
            # This would be admin-only in a real implementation
            # For now, return mock data

            mock_subscriptions = [
                {
                    "email": "user1@example.com",
                    "subscribed": True,
                    "subscribed_at": "2024-01-01T00:00:00Z",
                    "preferences": {"categories": ["ramyeon"], "frequency": "weekly"},
                    "source": "website"
                },
                {
                    "email": "user2@example.com",
                    "subscribed": True,
                    "subscribed_at": "2024-01-02T00:00:00Z",
                    "preferences": {"categories": ["tteokbokki"], "frequency": "monthly"},
                    "source": "app"
                }
            ]

            return Response({
                "subscriptions": mock_subscriptions,
                "total": len(mock_subscriptions)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting newsletter subscriptions: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NewsletterStatusView(APIView):
    """View for checking newsletter subscription status"""
    def post(self, request):
        """Check if email is subscribed to newsletter"""
        try:
            email = request.data.get('email', '').strip()

            if not email:
                return Response(
                    {"error": "Email is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # In a real implementation, you'd query the database
            # subscription = db.collection.find_one({"email": email})

            # Mock response
            is_subscribed = True  # This would be subscription.get('subscribed', False) if subscription else False

            return Response({
                "email": email,
                "subscribed": is_subscribed
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error checking newsletter status: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
