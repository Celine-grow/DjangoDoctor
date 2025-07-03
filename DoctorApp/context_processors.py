# filepath: d:\Cystella Django\DoctorPortal\DoctorApp\context_processors.py
from .models import Patient

def patients_list(request):
    try:
        patients = Patient.objects.all()
    except Exception:
        patients = []
    return {'patients': patients}