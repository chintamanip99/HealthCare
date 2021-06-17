from django.urls import path,include
from .views import register_patient,register_doctor,Doctors
from rest_framework.authtoken.views import obtain_auth_token

app_name="profiles"

urlpatterns = [
	path("login_user/",obtain_auth_token,name="obtain_auth_token"),
	path("register_patient/",register_patient,name="register_patient"),
	path("register_doctor/",register_doctor,name="register_doctor"),
	path('doctors/',Doctors.as_view(),name='doctors'),
]