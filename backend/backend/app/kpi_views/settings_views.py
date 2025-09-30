from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import UserSettings
from ..decorators.authenticationDecorator import require_authentication
import logging

logger = logging.getLogger(__name__)

class UserSettingsView(APIView):
    """View for user settings management"""
    @require_authentication
    def get(self, request):
        """Get user settings"""
        try:
            user_id = request.current_user.get('user_id')

            # In a real implementation, you'd query the database
            # settings = db.collection.find_one({"user_id": user_id})

            # Mock default settings
            settings = UserSettings(user_id=user_id)

            return Response({
                "settings": settings.to_dict()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting user settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def post(self, request):
        """Create or update user settings"""
        try:
            user_id = request.current_user.get('user_id')
            settings_data = request.data.get('settings', {})

            # Validate settings data
            valid_themes = ['light', 'dark', 'auto']
            if 'theme' in settings_data and settings_data['theme'] not in valid_themes:
                return Response(
                    {"error": f"Invalid theme. Must be one of: {valid_themes}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            valid_languages = ['en', 'ko', 'zh', 'ja']
            if 'language' in settings_data and settings_data['language'] not in valid_languages:
                return Response(
                    {"error": f"Invalid language. Must be one of: {valid_languages}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update settings
            settings = UserSettings(user_id=user_id, **settings_data)

            # In a real implementation, you'd save to database
            # db.collection.update_one(
            #     {"user_id": user_id},
            #     {"$set": settings.to_dict()},
            #     upsert=True
            # )

            return Response({
                "message": "Settings updated successfully",
                "settings": settings.to_dict()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating user settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def put(self, request):
        """Update specific user settings"""
        try:
            user_id = request.current_user.get('user_id')
            settings_data = request.data.get('settings', {})

            # In a real implementation, you'd update specific fields
            # db.collection.update_one(
            #     {"user_id": user_id},
            #     {"$set": settings_data}
            # )

            return Response({
                "message": "Settings updated successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating user settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def delete(self, request):
        """Reset user settings to defaults"""
        try:
            user_id = request.current_user.get('user_id')

            # In a real implementation, you'd delete or reset settings
            # db.collection.delete_one({"user_id": user_id})

            # Return default settings
            default_settings = UserSettings(user_id=user_id)

            return Response({
                "message": "Settings reset to defaults",
                "settings": default_settings.to_dict()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error resetting user settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserSettingsNotificationView(APIView):
    """View for managing notification settings"""
    @require_authentication
    def get(self, request):
        """Get notification settings"""
        try:
            user_id = request.current_user.get('user_id')

            # Mock notification settings
            notifications = {
                'email': True,
                'push': True,
                'sms': False,
                'promotions': True,
                'order_updates': True
            }

            return Response({
                "notifications": notifications
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting notification settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def put(self, request):
        """Update notification settings"""
        try:
            user_id = request.current_user.get('user_id')
            notification_data = request.data.get('notifications', {})

            # Validate notification types
            valid_types = ['email', 'push', 'sms', 'promotions', 'order_updates']
            for key in notification_data:
                if key not in valid_types:
                    return Response(
                        {"error": f"Invalid notification type: {key}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # In a real implementation, you'd update the settings
            # db.collection.update_one(
            #     {"user_id": user_id},
            #     {"$set": {"notifications": notification_data}}
            # )

            return Response({
                "message": "Notification settings updated successfully",
                "notifications": notification_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating notification settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserSettingsPrivacyView(APIView):
    """View for managing privacy settings"""
    @require_authentication
    def get(self, request):
        """Get privacy settings"""
        try:
            user_id = request.current_user.get('user_id')

            # Mock privacy settings
            privacy = {
                'profile_visible': True,
                'activity_visible': False,
                'data_sharing': False
            }

            return Response({
                "privacy": privacy
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error getting privacy settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @require_authentication
    def put(self, request):
        """Update privacy settings"""
        try:
            user_id = request.current_user.get('user_id')
            privacy_data = request.data.get('privacy', {})

            # Validate privacy types
            valid_types = ['profile_visible', 'activity_visible', 'data_sharing']
            for key in privacy_data:
                if key not in valid_types:
                    return Response(
                        {"error": f"Invalid privacy type: {key}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # In a real implementation, you'd update the settings
            # db.collection.update_one(
            #     {"user_id": user_id},
            #     {"$set": {"privacy": privacy_data}}
            # )

            return Response({
                "message": "Privacy settings updated successfully",
                "privacy": privacy_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating privacy settings: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
