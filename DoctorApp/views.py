from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .forms import DoctorRegistrationForm,DoctorProfileForm, DoctorLoginForm
from DoctorApp.models import Doctor
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import requests
from bson import ObjectId
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Patient
from pycaret.regression import load_model, predict_model
# Load Excel once when server starts
med_df = pd.read_csv('DoctorApp\static\data\Resources Inventory Cost Sheet.csv')

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            # Check if email or license number already exists
            if Doctor.objects.filter(email=form.cleaned_data['email']).first():
                messages.error(request, 'Email already registered')
                return redirect('register_doctor')

            if Doctor.objects.filter(license_number=form.cleaned_data['license_number']).first():
                messages.error(request, 'License number already registered')
                return redirect('register_doctor')

            # Create an instance of the Doctor
            doctor = Doctor(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                contact=form.cleaned_data['contact'],
                license_number=form.cleaned_data['license_number'],
                specialization=form.cleaned_data['specialization'],
                years_of_experience=form.cleaned_data['years_of_experience'],
                qualifications=[q.strip() for q in form.cleaned_data['qualifications'].split('\n') if q.strip()]
            )
            doctor.set_password(form.cleaned_data['password'])
            doctor.save()

            messages.success(request, 'Registration successful!')
            return redirect('login_doctor')
    else:
        form = DoctorRegistrationForm()

    return render(request, 'DoctorApp/register.html', {'form': form})

def login_doctor(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            doctor = Doctor.objects.filter(email=email).first()

            if doctor and doctor.check_password(password):
                request.session['doctor_id'] = str(doctor.id)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login_doctor')
    else:
        form = DoctorLoginForm()

    return render(request, 'DoctorApp/login.html', {'form': form})




def message_patient(request, patient_name):
    # Get doctor from session
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        messages.error(request, "You must be logged in as a doctor to send messages.")
        return redirect('doctor_login')

    try:
        doctor = Doctor.objects.get(id=ObjectId(doctor_id))
    except Doctor.DoesNotExist:
        messages.error(request, "Logged-in doctor not found.")
        return redirect('doctor_login')

    # 🧠 GET patient info to pass to template
    try:
        patient = Patient.objects.get(first_name=patient_name)
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found.")
        return redirect('dashboard')  # Or wherever

    if request.method == 'POST':
        print("🟢 POST request received")
        print("📝 Message:", request.POST.get('message'))
        message_text = request.POST.get('message')
        doctor_name = f"{doctor.first_name} {doctor.last_name}"
        document_file = request.FILES.get('document')
        document_url = ''

        if document_file:
            fs = FileSystemStorage()
            filename = fs.save(document_file.name, document_file)
            document_url = request.build_absolute_uri(fs.url(filename))

        payload = {
            "patient_email": patient.email,
            "doctor_name": doctor_name,
            "message": message_text,
            "document_url": document_url
        }

        api_url = "http://10.2.8.100:8000/api/auth/receive_message/"

        try:
            response = requests.post(api_url, json=payload, timeout=5)
            print("📡 Response status:", response.status_code)
            print("📡 Response body:", response.text)
            if response.status_code == 201:
                messages.success(request, "Message sent successfully!")
            else:
                messages.error(request, f"API error: {response.json()}")
        except Exception as e:
            messages.error(request, f"Could not connect to patient system: {e}")

        return redirect('message_patient', patient_name=patient_name)

    # GET request - show chat page with patient info
    return render(request, 'DoctorApp/chat.html', {
        'patient_email': patient_name,
        'doctor_name': f"{doctor.first_name} {doctor.last_name}",
        'patient': patient  # ✅ pass full patient object
    })
@csrf_exempt
def add_patient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient = Patient.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                contactno=data.get('contactno'),
                email=data.get('email'),
                date_of_birth=data.get('date_of_birth')
            )
            return JsonResponse({'message': 'Patient added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def list_patients(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        data = list(patients.values())  # returns list of dicts
        return JsonResponse(data, safe=False)


# #the views that should only be executed if doctor is logged in
@login_required
def doctor_dashboard(request):
     doctor_id = request.session.get('doctor_id')
     doctor = Doctor.objects.get(id=doctor_id)
     patients = Patient.objects.all()
     return render(request, 'DoctorApp/dashboard.html') #{'doctor': doctor,'patients': patients})

def logout_doctor(request):
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    messages.success(request, 'You have been logged out')
    return redirect('login_doctor')
@login_required
def settings_view(request):
      doctor_id = request.session.get('doctor_id')
      if not doctor_id:
          messages.error(request, "You must be logged in as a doctor to access settings.")
          return redirect('login_doctor')
      try:
          doctor = Doctor.objects.get(id=doctor_id)
      except Doctor.DoesNotExist:
          messages.error(request, "Doctor profile not found")
          return redirect('dashboard')

      if request.method == 'POST':
          form = DoctorProfileForm(request.POST)
          if form.is_valid():
              #Update doctor fields manually
              doctor.first_name = form.cleaned_data['first_name']
              doctor.last_name = form.cleaned_data['last_name']
              doctor.email = form.cleaned_data['email']
              doctor.contact = form.cleaned_data['contact']
              doctor.specialization = form.cleaned_data['specialization']
              doctor.license_number = form.cleaned_data['license_number']
              doctor.years_of_experience = form.cleaned_data['years_of_experience']
              doctor.qualifications = form.cleaned_data['qualifications'].split('\n')

              try:
                  doctor.save()
                  messages.success(request, 'Profile updated successfully!')
                  return redirect('settings')
              except Exception as e:
                  messages.error(request, f'Error saving profile: {str(e)}')
          else:
              initial_data = {
                  'first_name': doctor.first_name,
                  'last_name': doctor.last_name,
                  'email': doctor.email,
                  'contact': doctor.contact,
                  'specialization': doctor.specialization,
                  'license_number': doctor.license_number,
                  'years_of_experience': doctor.years_of_experience,
                  'qualifications': '\n'.join(doctor.qualifications) if doctor.qualifications else '',
              }
              form = DoctorProfileForm(initial=initial_data)
    
              return render(request, 'DoctorApp/settings.html', {'form': form, 'doctor': doctor})


# these are the routes ive set up

# def doctor_dashboard(request):
#     return render(request, 'DoctorApp/dashboard.html')

def settings_view(request):
    return render(request, 'DoctorApp/settings.html')

def patients(request):
    return render(request, 'DoctorApp/patients.html')

def chat(request):
    return render(request, 'DoctorApp/chat.html')


def cystela(request):
    return render(request, 'DoctorApp/cystela.html')

from pycaret.regression import load_model, predict_model

# Load the model once when views.py is loaded
growth_model = load_model('DoctorApp/growth_rate_model')  # adjust path if needed

@csrf_exempt
def predict_growth_rate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Build DataFrame for prediction
            df = pd.DataFrame([{
                'age': data['age'],
                'size': data['size'],
                'ca125': data['ca125'],
                'menopause': data['menopause'],
                'ultrasound': data['ultrasound'],
                'symptoms': data['symptoms'],
                'management': data.get('management', 'awaiting'),
                'region': data['region']
            }])

            # ✅ Predict with PyCaret model 
            result = predict_model(growth_model, data=df)
            prediction = float(result['prediction_label'].iloc[0])

            # ✅ Classify prediction
            def classify(rate):
                if rate <= 0:
                    return 'Shrinking'
                elif rate < 0.012:
                    return 'Stable'
                elif rate < 0.020:
                    return 'Moderate-growing'
                else:
                    return 'Fast-growing'

            category = classify(prediction)

            # ✅ Recommend management based on category
            def recommend(category):
                return {
                    'Shrinking': 'Monitor or consider medication',
                    'Stable': 'Observation or schedule routine follow-up',
                    'Moderate-growing': 'Refer to gynecologist for further assessment',
                    'Fast-growing': 'Urgent surgical evaluation recommended'
                }.get(category, 'Consult specialist')

            recommended = recommend(category)

            return JsonResponse({
                'prediction': round(prediction, 4),
                'category': category, 
                'recommended_management': recommended
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)



#inventory for views 
from django.http import JsonResponse

def get_inventory(request):
    region = request.GET.get('region')
    if not region:
        return JsonResponse({'error': 'Region not specified'}, status=400)

    try:
        # Normalize whitespace and lowercase
        df = med_df.copy()
        df['Region'] = df['Region'].str.strip().str.lower()
        region = region.strip().lower()

        # Only select medications
        meds = df[(df['Region'] == region) & (df['Category'].str.lower() == 'medications')]

        # Prepare response
        data = meds[['Item', 'Cost (KES)', 'Available Stock']].rename(
            columns={'Item': 'Medication', 'Cost (KES)': 'Cost', 'Available Stock': 'Stock'}
        ).to_dict(orient='records')

        return JsonResponse({'medications': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
