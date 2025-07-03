# urls.py
from django.conf import settings
from django.urls import path, include
from django_mongoengine.mongo_admin.sites import site as mongo_admin_site
from django.conf.urls.static import static

urlpatterns = [
    path('mongo-admin/', mongo_admin_site.urls),  # Use this in browser
    path('', include('DoctorApp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)