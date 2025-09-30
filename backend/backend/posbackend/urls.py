from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app.urls_simple')),
    path('', lambda request: HttpResponse("POS System API is running!")),
]
