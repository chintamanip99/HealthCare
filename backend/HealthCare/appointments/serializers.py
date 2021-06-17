from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Patient,Doctor,DoctorType
from .models import Appointment
from profiles.serializers import PatientSerializer,DoctorSerializer,PatientSerializer1,DoctorSerializer1
from django.core.mail import send_mail,BadHeaderError
import re

class AppointmentSerializer(serializers.ModelSerializer):
	patient=PatientSerializer1()
	doctor=DoctorSerializer1()
	class Meta:
		model=Appointment
		fields='__all__'

class AddUpdateAppointmentSerializer(serializers.ModelSerializer):
	patient1=serializers.IntegerField(write_only=True,required=False)
	doctor1=serializers.IntegerField(write_only=True,required=False)
	patient=serializers.IntegerField(write_only=True,required=False)
	doctor=serializers.IntegerField(write_only=True,required=False)
	description=serializers.CharField(write_only=True,required=False)
	prescription=serializers.CharField(write_only=True,required=False)
	datetime=serializers.CharField(write_only=True,required=False)
	meeting_link=serializers.URLField(write_only=True,required=False)
	class Meta:
		model=Appointment
		fields=['patient','doctor','description','prescription','datetime','meeting_link','patient1','doctor1']

	def save(self,user):
		patient=self.validated_data['patient']
		doctor=self.validated_data['doctor']
		description=self.validated_data['description']
		appointment=Appointment.objects.create(
			patient=Patient.objects.get(user=user),
			doctor=Doctor.objects.get(user__id=doctor),
			description=description,
			)
		appointment.save()
		if(appointment.doctor.user.email):
				try:
					if(not send_mail('Appointment Request Notification from HealthCare',"Appointment request from Patient: "+appointment.patient.user.first_name+" "+appointment.patient.user.last_name+"\nAge: "+str(appointment.patient.age)+"\nHealth Complaint: "+appointment.description,'cmp151999@gmail.com',[appointment.doctor.user.email],fail_silently=True)>0):
						print("not done")
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
				except BadHeaderError:
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})

		if(appointment.patient.user.email):
				try:
					if(not send_mail('Appointment Request Notification from HealthCare',"Appointment request sent to Doctor: Dr. "+appointment.doctor.user.first_name+" "+appointment.doctor.user.last_name+" , "+str(appointment.doctor.doctortype.doctortype),'cmp151999@gmail.com',[appointment.patient.user.email],fail_silently=True)>0):
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
				except BadHeaderError:
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
		return appointment

		def update(self,user):
			print("ran untill this11111111 "+user.username)
			patient1=self.validated_data['patient1']
			meeting_link=self.validated_data['meeting_link']
			datetime=self.validated_data['datetime']
			print("ran untill this")
			appointment=Appointment.objects.get(
				patient=Patient.objects.get(id=patient1),
			)
			appointment.meeting_link=meeting_link
			appointment.is_booked=True
			appointment.datetime=datetime
			appointment.save()
			if(appointment.patient.user.email):
				try:
					if(not send_mail('Appointment Booking Notification from HealthCare PVT Ltd ',"Appointment booked with Doctor: Dr. "+appointment.doctor.user.first_name+" "+appointment.doctor.user.last_name+" , "+str(appointment.doctor.doctortype.doctortype)+"\n Date and Time: "+appointment.datetime+"\n Meeting Link: "+appointment.meeting_link,'cmp151999@gmail.com',[appointment.patient.user.email],fail_silently=True)>0):
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
				except BadHeaderError:
					raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
			return appointment

		def update1(self,user):
			patient=self.validated_data['patient']
			prescription=self.validated_data['prescription']
			appointment=Appointment.objects.get(
				patient=Patient.objects.get(id=patient),
				doctor=Doctor.objects.get(user=user),
			)
			appointment.prescription=prescription
			appointment.is_over=True
			appointment.save()
			if(appointment.patient.user.email):
				try:
					if(not send_mail('Prescription Notification from HealthCare PVT Ltd ',"Prescription from Doctor: Dr. "+appointment.doctor.user.first_name+" "+appointment.doctor.user.last_name+" , "+str(appointment.doctor.doctortype.doctortype)+"\n Appointment was on, Date and Time: "+appointment.datetime+"\n Prescription:\n "+appointment.prescription,'cmp151999@gmail.com',[appointment.patient.user.email],fail_silently=True)>0):
						raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
				except BadHeaderError:
					raise serializers.ValidationError({'emailsent':'Email Sending Failed'})
			return appointment