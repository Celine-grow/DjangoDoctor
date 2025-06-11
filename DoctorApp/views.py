from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DoctorRegistrationForm, DoctorLoginForm
from DoctorApp.models import Doctor
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

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
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login_doctor')
    else:
        form = DoctorLoginForm()
    
    return render(request, 'DoctorApp/login.html', {'form': form})

#the views that should only be executed if doctor is logged in
@login_required
def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'DoctorApp/dashboard.html', {'doctor': doctor})

def logout_doctor(request):
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    messages.success(request, 'You have been logged out')
    return redirect('login_doctor')