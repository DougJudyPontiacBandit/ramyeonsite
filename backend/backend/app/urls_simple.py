from django.urls import path
from .kpi_views.authentication_views import LoginView, LogoutView, RegisterView, CurrentUserView, RefreshTokenView, VerifyTokenView

urlpatterns = [
    # Authentication endpoints only
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
    path('auth/verify-token/', VerifyTokenView.as_view(), name='verify-token'),
]

