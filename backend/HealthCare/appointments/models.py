from django.db import models
from profiles.models import Doctor,Patient
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail,BadHeaderError
# Create your models here.
class Appointment(models.Model):
	patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
	doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True)
	description=models.TextField(max_length=500,null=True,blank=True)
	prescription=models.TextField(max_length=500,null=True,blank=True)
	datetime=models.CharField(max_length=100,null=True,blank=True)
	meeting_link=models.URLField(max_length=2000,null=True,blank=True)
	is_booked=models.BooleanField(default=False,null=True,blank=True)
	is_over=models.BooleanField(default=False,null=True,blank=True)
	class Meta:
		unique_together = ('id','patient', 'doctor')
	def __str__(self):
		return "Name: "+self.patient.user.first_name+" "+self.patient.user.last_name+" Phone Number: "+self.patient.phone+" Email :"+self.patient.user.email 

@receiver(post_save,sender=Appointment)
def send_mail_to_patient(sender,instance,created,**kwargs):
	if not created:
		if(instance.patient.user.email and instance.is_over==False and instance.meeting_link and instance.is_booked and instance.datetime):
			try:
				if(not send_mail('Appointment Booking Notification from HealthCare PVT Ltd ',"Appointment booked with Doctor: Dr. "+instance.doctor.user.first_name+" "+instance.doctor.user.last_name+" , "+str(instance.doctor.doctortype.doctortype)+"\n Date and Time: "+instance.datetime+"\n Meeting Link: "+instance.meeting_link,'cmp151999@gmail.com',[instance.patient.user.email],fail_silently=True)>0):
					print('k')
				else:
					print('k')
			except BadHeaderError:
				print('k')
		else:
			print('k')
		if(instance.patient.user.email and instance.is_over==True and instance.prescription):
				try:
					if(not send_mail('Prescription Notification from HealthCare PVT Ltd ',"Prescription from Doctor: Dr. "+instance.doctor.user.first_name+" "+instance.doctor.user.last_name+" , "+str(instance.doctor.doctortype.doctortype)+"\n Appointment was on, Date and Time: "+instance.datetime+"\n Prescription:\n "+instance.prescription,'cmp151999@gmail.com',[instance.patient.user.email],fail_silently=True)>0):
						print('k')
					else:
						print('k')
				except BadHeaderError:
					print('k')
		else:
			print('k')