# urls.py

from django.urls import path, include
from django_mongoengine.mongo_admin.sites import site as mongo_admin_site

urlpatterns = [
    path('mongo-admin/', mongo_admin_site.urls),  # Use this in browser
    path('', include('DoctorApp.urls')),
]
