from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_doctor, name='register_doctor'),
    path('login/', views.login_doctor, name='login_doctor'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout/', views.logout_doctor, name='logout_doctor'),
]