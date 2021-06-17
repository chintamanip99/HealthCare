from django.shortcuts import render
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientSerializer,DoctorSerializer,DoctorSerializer1
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.timezone import now,localtime
import datetime
import random
from django.core.mail import send_mail,BadHeaderError
from .models import Patient,Doctor
from rest_framework.permissions import BasePermission
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from appointments.views import StandardResultsSetPagination
from rest_framework import filters

# Create your views here.
@api_view(['POST','GET','PUT'])
@permission_classes([])
def register_patient(request):

    if request.method=='POST':
        serializer=PatientSerializer(data=request.data)
        data={}
        if(serializer.is_valid()):
            patient=serializer.save()
            data['username']=patient.user.username
            data['email']=patient.user.email
            data['password']=patient.user.password
            token=Token.objects.get(user=patient.user).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data)

@api_view(['POST','GET','PUT'])
@permission_classes([])
def register_doctor(request):

    if request.method=='POST':
        serializer=DoctorSerializer(data=request.data)
        data={}
        if(serializer.is_valid()):
            doctor=serializer.save()
            data['username']=doctor.user.username
            data['email']=doctor.user.email
            data['password']=doctor.user.password
            token=Token.objects.get(user=doctor.user).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data)

class Doctors(generics.ListAPIView):
    permission_classes = [(IsAuthenticated)]
    pagination_class=StandardResultsSetPagination
    queryset=Doctor.objects.all()
    serializer_class=DoctorSerializer1
    filter_backends = [filters.SearchFilter]
    search_fields  = ['doctortype__doctortype']