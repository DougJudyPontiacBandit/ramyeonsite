from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.PromotionListView.as_view(), name='promotion-list'),
    path('detail/<str:promotion_id>/', views.PromotionDetailView.as_view(), name='promotion-detail'),
    path('qr/<str:promotion_id>/', views.PromotionQRView.as_view(), name='promotion-qr'),
    path('scan/', views.PromotionQRScanView.as_view(), name='promotion-scan'),
    path('active/', views.ActivePromotionsView.as_view(), name='active-promotions'),
    path('apply/', views.PromotionApplyView.as_view(), name='promotion-apply'),
]
