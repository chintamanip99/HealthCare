from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient,Doctor,DoctorType
from django.core.mail import send_mail,BadHeaderError
import re

class PatientSerializer1(serializers.ModelSerializer):
	class Meta:
		model=Patient
		fields="__all__"

class UserAbstractSerializer(serializers.ModelSerializer):

	class Meta:
		model=User
		fields=['id','username','first_name','last_name','email']

class DoctorTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model=DoctorType
		fields="__all__"

class DoctorSerializer1(serializers.ModelSerializer):
	user=UserAbstractSerializer()
	doctortype=DoctorTypeSerializer()
	class Meta:
		model=Doctor
		fields="__all__"
			

class PatientSerializer(serializers.ModelSerializer):
	password2=serializers.CharField(write_only=True,required=True)
	age=serializers.CharField(write_only=True,required=True)
	email=serializers.CharField(write_only=True,required=True)
	phone=serializers.CharField(write_only=True,required=True)
	first_name=serializers.CharField(write_only=True,required=True)
	last_name=serializers.CharField(write_only=True,required=True)
	birthdate=serializers.CharField(write_only=True,required=True)
	gender=serializers.CharField(write_only=True,required=True)
	address=serializers.CharField(write_only=True,required=True)
	class Meta:
		model=User
		fields=['username','password','password2','age','email','phone','first_name','last_name','birthdate','gender','address']

	def save(self):
		username=self.validated_data['username']
		password=self.validated_data['password']
		password2=self.validated_data['password2']
		email=self.validated_data['email']
		phone=self.validated_data['phone']
		gender=self.validated_data['gender']
		birthdate=self.validated_data['birthdate']
		address=self.validated_data['address']
		age=int(self.validated_data['age'])
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if not re.search(regex,email):
			raise serializers.ValidationError({'email':'Email entered is invalid'})
		if password!=password2:
			raise serializers.ValidationError({'password':'Passwords doesnt match'})
		if age<=0:
			raise serializers.ValidationError({'age':'Age cant be negative or zero'})
		if age<65:
			raise serializers.ValidationError({'age':'Only 65+ can create an account'})			
		else:
			user=User.objects.create_user(
				email=email,
				username=username,
				password=password
			)
			if('first_name' in self.validated_data.keys()):
				user.first_name=self.validated_data['first_name']
			if('last_name' in self.validated_data.keys()):
				user.last_name=self.validated_data['last_name']
			user.save()
			patient=Patient.objects.create(
				user=user,
				age=age,
				phone=phone,
				birthdate=birthdate,
				gender=gender,
				address=address
			)
			patient.save()
			return patient

class DoctorSerializer(serializers.ModelSerializer):
	password2=serializers.CharField(write_only=True,required=True)
	email=serializers.CharField(write_only=True,required=True)
	phone=serializers.CharField(write_only=True,required=True)
	first_name=serializers.CharField(write_only=True,required=True)
	description=serializers.CharField(write_only=True,required=True)
	last_name=serializers.CharField(write_only=True,required=True)
	doctortype=serializers.IntegerField(write_only=True,required=True)
	class Meta:
		model=User
		fields=['doctortype','username','password','password2','email','phone','first_name','last_name','description']

	def save(self):
		username=self.validated_data['username']
		password=self.validated_data['password']
		password2=self.validated_data['password2']
		email=self.validated_data['email']
		phone=self.validated_data['phone']
		description=self.validated_data['description']
		doctortype=self.validated_data['doctortype']
		regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
		if not re.search(regex,email):
			raise serializers.ValidationError({'email':'Email entered is invalid'})
		if password!=password2:
			raise serializers.ValidationError({'password':'Passwords doesnt match'})		
		else:
			user=User.objects.create_user(
				email=email,
				username=username,
				password=password
			)
			if('first_name' in self.validated_data.keys()):
				user.first_name=self.validated_data['first_name']
			if('last_name' in self.validated_data.keys()):
				user.last_name=self.validated_data['last_name']
			user.save()
			doctor=Doctor.objects.create(
				user=user,
				phone=phone,
				description=description,
				doctortype=DoctorType.objects.get(id=doctortype)
			)
			doctor.save()
			return doctor