from django.urls import path
from . import views
# from .views import message_patient

urlpatterns = [
    path('', views.register_doctor, name='register_doctor'),
    path('login/', views.login_doctor, name='login_doctor'),
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('patients/', views.patients, name='patients'),  
    # path('message/<str:patient_name>/', message_patient, name='message_patient'),
    path('cystela/', views.cystela, name='cystela'),  
    path('predict/', views.predict_growth_rate, name='predict'),  
    path('inventory/', views.get_inventory, name='inventory'),


    path('settings/', views.settings_view, name='settings'), 
    path('add_patient/', views.add_patient, name='add_patient'),
    path('list_patients/', views.list_patients, name='list_patients'),

]