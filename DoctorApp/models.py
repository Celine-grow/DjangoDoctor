from mongoengine import Document,fields
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime


class Doctor(Document):
    # Personal Information
    first_name = fields.StringField(required=True, max_length=50)
    last_name = fields.StringField(required=True, max_length=50)
    email = fields.EmailField(required=True, unique=True)
    contact = fields.StringField(required=True, max_length=15)
    password = fields.StringField(required=True)
    
    # Professional Information
    license_number = fields.StringField(required=True, unique=True)
    specialization = fields.StringField(required=True)
    years_of_experience = fields.IntField()
    qualifications = fields.ListField(fields.StringField())
    
    # Time of Creation
    created_at = fields.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'doctors',
        'indexes': ['email', 'license_number']
    }

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialization})"

