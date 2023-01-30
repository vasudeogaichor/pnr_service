from django.contrib import admin
from django.urls import path, include
from pnr_api import urls as pnr_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('get_pnr_status/', include(pnr_api_urls)),
]
