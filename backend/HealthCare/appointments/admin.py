from django.contrib import admin
from appointments.models import Appointment
from django.core.mail import send_mail,BadHeaderError
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    fields = ('patient', 'description', 'prescription','datetime','meeting_link','is_booked','is_over')
    def get_queryset(self, request):
        query = super(AppointmentAdmin, self).get_queryset(request)
        filtered_query = query.filter(doctor__user=request.user,is_over=False)
        return filtered_query

    def post_save(self, instance):
    	print("hhjgkubyt is called")
    	if(instance.patient.user.email and instance.meeting_link and instance.is_booked):
    		try:
    			if(not send_mail('Appointment Booking Notification from HealthCare PVT Ltd ',"Appointment booked with Doctor: Dr. "+instance.doctor.user.first_name+" "+instance.doctor.user.last_name+" , "+str(instance.doctor.doctortype.doctortype)+"\n Date and Time: "+instance.datetime+"\n Meeting Link: "+instance.meeting_link,'cmp151999@gmail.com',[instance.patient.user.email],fail_silently=True)>0):
    				print('k')
    			else:
    				print('k')
    		except BadHeaderError:
    			print('k')
    	else:
    		print('k')

admin.site.register(Appointment,AppointmentAdmin)