# admin.py

from django_mongoengine.mongo_admin import DocumentAdmin
from django_mongoengine.mongo_admin.sites import site as mongo_admin_site  # Explicit name
from .models import Doctor

class DoctorAdmin(DocumentAdmin):
    list_display = ('first_name', 'last_name', 'email', 'specialization', 'license_number')
    search_fields = ('first_name', 'last_name', 'email', 'license_number', 'specialization')

mongo_admin_site.register(Doctor, DoctorAdmin)
