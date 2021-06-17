from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentSerializer,AddUpdateAppointmentSerializer
from .models import Appointment
from profiles.models import Patient,Doctor

from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import BasePermission
from django.core.mail import send_mail,BadHeaderError

class StandardResultsSetPagination(PageNumberPagination,APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

  #   def get_paginated_response(self,type,user):
  #   	if(type==0):
		# 	data=Appointment.objects.filter(docctor__user=user,is_over=False)
		# 	response = Response(data)
		# 	response['count'] = self.page.paginator.count
		# 	response['next'] = self.get_next_link()
		# 	response['previous'] = self.get_previous_link()
		# 	return response
		# if(type==1):
		# 	data=Appointment.objects.filter(patient__user=user)
		# 	response = Response(data)
		# 	response['count'] = self.page.paginator.count
		# 	response['next'] = self.get_next_link()
		# 	response['previous'] = self.get_previous_link()
		# 	return response

# Create your views here.
class Appointment1(generics.ListAPIView):
	permission_classes = [(IsAuthenticated)]
	parser_class = (FileUploadParser,MultiPartParser,FormParser,JSONParser)
	pagination_class=StandardResultsSetPagination
	queryset=Appointment.objects.all()
	serializer_class=AppointmentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields  = ['doctor__user__first_name','doctor__user__last_name','doctor__doctortype__doctortype']

	def get(self,request,type):
		try:
			Doctor.objects.get(user=request.user)
			return Response({'data':AppointmentSerializer(Appointment.objects.filter(doctor__user=request.user,is_over=False),many=True).data})
		except Doctor.DoesNotExist:
			try:
				Patient.objects.get(user=request.user)
				return Response({'data':AppointmentSerializer(Appointment.objects.filter(patient__user=request.user),many=True).data})
			except Patient.DoesNotExist:
				return Response({'data':[]})

	def post(self, request,type):
		print(request.user)
		serializer=AddUpdateAppointmentSerializer(data=request.data)
		if(serializer.is_valid()):
			appointment=serializer.save(request.user)
			return Response({'appointment_data':serializer.data,'appointment_request_success':'Appointment request sent to the doctor Successfully'})
		else:
			print(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request,type):
		if(type==0):
			patient=int(request.data['patient'])
			print(patient)
			datetime=request.data['datetime']
			meeting_link=request.data['meeting_link']
			appointment=Appointment.objects.get(doctor__user=request.user,patient__user=Patient.objects.get(id=patient).user)
			appointment.meeting_link=meeting_link
			appointment.is_booked=True
			appointment.datetime=datetime
			appointment.save()
			if(appointment.patient.user.email):
				try:
					if(not send_mail('Appointment Booking Notification from HealthCare PVT Ltd ',"Appointment booked with Doctor: Dr. "+appointment.doctor.user.first_name+" "+appointment.doctor.user.last_name+" , "+str(appointment.doctor.doctortype.doctortype)+"\n Date and Time: "+appointment.datetime+"\n Meeting Link: "+appointment.meeting_link,'cmp151999@gmail.com',[appointment.patient.user.email],fail_silently=True)>0):
						return Response({'appointment_finished_successfully':'Appointment Successfully booked'})
					else:
						return Response({'appointment_finished_successfully':'Appointment Successfully booked, notification sent on your Email address'})
				except BadHeaderError:
					return Response({'appointment_finished_successfully':'Appointment Successfully booked'})
			else:
				return Response({'appointment_finished_successfully':'Appointment Successfully booked'})

		if(type==1):
			patient=int(request.data['patient'])
			prescription=request.data['prescription']
			appointment=Appointment.objects.get(doctor__user=request.user,patient__user=Patient.objects.get(id=patient).user)
			appointment.prescription=prescription
			appointment.is_over=True
			appointment.save()
			if(appointment.patient.user.email):
				try:
					if(not send_mail('Prescription Notification from HealthCare PVT Ltd ',"Prescription from Doctor: Dr. "+appointment.doctor.user.first_name+" "+appointment.doctor.user.last_name+" , "+str(appointment.doctor.doctortype.doctortype)+"\n Appointment was on, Date and Time: "+appointment.datetime+"\n Prescription:\n "+appointment.prescription,'cmp151999@gmail.com',[appointment.patient.user.email],fail_silently=True)>0):
						return Response({'appointment_finished_successfully':'Appointment Successfully Finished'})
					else:
						return Response({'appointment_finished_successfully':'Appointment Successfully Finished, prescription sent on patient\'s Email address'})
				except BadHeaderError:
					return Response({'appointment_finished_successfully':'Appointment Successfully Finished'})
			else:
				return Response({'appointment_finished_successfully':'Appointment Successfully Finished'})
			