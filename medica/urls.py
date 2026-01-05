from django.contrib import admin
from django.urls import path, include  # <--- Make sure 'include' is imported
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Connect the 'core' app URLs to the homepage
    path('', include('core.urls')), 
]

# This snippet allows Django to serve your uploaded images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)