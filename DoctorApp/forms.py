from django import forms
from .models import Doctor

class DoctorRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    license_number = forms.CharField(max_length=50, required=True)
    specialization = forms.CharField(max_length=100, required=True)
    years_of_experience = forms.IntegerField(required=True)
    qualifications = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter each qualification on a new line",
        required=True
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
class DoctorLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
