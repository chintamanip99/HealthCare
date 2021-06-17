from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class DoctorType(models.Model):
	doctortype=models.CharField(max_length=100,null=True,blank=True)
	def __str__(self):
		return self.doctortype+" "+str(self.id)

class Doctor(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	phone=models.CharField(max_length=12,null=True,blank=True)
	description=models.TextField(max_length=500,null=True,blank=True)
	doctortype=models.ForeignKey(DoctorType,on_delete=models.CASCADE,null=True,blank=True)
	def __str__(self):
		return self.user.username+" "+str(self.user.id)

class Patient(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	age=models.IntegerField(null=True,default=65,blank=False)
	phone=models.CharField(max_length=12,null=True,blank=False)
	birthdate=models.CharField(max_length=100,null=True,blank=False)
	gender=models.CharField(max_length=100,null=True,blank=False)
	address=models.CharField(max_length=1000,null=True,blank=False)
	def __str__(self):
		return self.user.first_name+" "+self.user.last_name

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)
