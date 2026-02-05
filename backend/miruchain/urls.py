"""
URL configuration for MIRUCHAIN project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/referrals/', include('referrals.urls')),
    path('api/v1/links/', include('links.urls')),
    path('api/v1/transactions/', include('transactions.urls')),
    path('api/v1/admin/', include('admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "MIRUCHAIN Administration"
admin.site.site_title = "MIRUCHAIN Admin Portal"
admin.site.index_title = "Welcome to MIRUCHAIN Platform Administration"
