from django.urls import path,include
from .views import Appointment1

app_name="appointments"

urlpatterns = [
	path('appointment/<int:type>',Appointment1.as_view(),name='appointment'),
]