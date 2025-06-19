from django.urls import path
from . import views

urlpatterns = [
#     path('register/', views.register_doctor, name='register_doctor'),
#     path('login/', views.login_doctor, name='login_doctor'),
#     path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
#     path('logout/', views.logout_doctor, name='logout_doctor'),
# 
 path('', views.login, name='login'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('patients/', views.patients, name='patients'),  
 path('chat/', views.chat, name='chat'),
 path('cystela/', views.cystela, name='cystela'),  
 path('settings/', views.settings, name='settings'),  

]