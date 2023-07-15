from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from payroll.models import Contact
from django.urls import reverse_lazy, reverse
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from payroll.models import Contact



def home(request):
	if request.user.is_authenticated and request.user.is_hr:
		return HttpResponseRedirect((reverse('HrProfile',kwargs={'pk':request.user.hrprofile.id})))
	elif request.user.is_authenticated and request.user.is_employee:
		return HttpResponseRedirect((reverse('EmployeeProfile',kwargs={'pk':request.user.employee.id})))

	return render(request,'main/home.html')
	

	
def contact(request):
	# name=request.post['name']
   if(request.method=='POST'):
      name=request.POST['name']
      email=request.POST['email']
      content=request.POST['content']
      contact=Contact(name=name,email=email,content=content)
      contact.save() 
      html_message = loader.render_to_string('main/email_contact.html',{'name':name})
      message = 'Hi '+str(name)+'. Greetings from Filox. Thank you for submitting your query/feedback. In case of a query, we will get back to you as soon as possible. Also, this is a auto-generated mail. So please refrain from replying to this mail.'
      send_mail('We heard you!!',message,settings. EMAIL_HOST_USER,[str(email)],fail_silently=True,html_message=html_message)
      messages.success(request,"Your query is sent successfully !!!")

   return render (request,"main/contact.html")

def payment(request):
	return render(request,'main/payment.html')

