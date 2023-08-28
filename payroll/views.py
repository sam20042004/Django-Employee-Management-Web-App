from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import auth
from django.contrib.auth.forms import UserCreationForm
from .models import Leave, Employee,hrProfile,Contact
from django.views.generic import TemplateView,CreateView,DetailView
from .forms import *
from .filters import *
from .templatetags import extras
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model

User = get_user_model()


from django.template import loader
from django.core.mail import send_mail
from django.conf import settings









def HrProfile(request,pk):
    hrprofile=get_object_or_404(hrProfile,id=pk)
  
    context={
        'hr':hrprofile,
    }
    return render(request,'profile/hrProfile.html',context)


def profile(request):
    if request.user.is_hr:
        if request.method == 'POST':
            u_form=UserUpdateForm(request.POST, instance=request.user)
            hr_form = HrUpdateForm(request.POST,request.FILES,instance=request.user.hrprofile)
            if hr_form.is_valid() and u_form.is_valid():
                hr_form.save()
                u_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect("home") 
        else:

            hr_form = HrUpdateForm(instance=request.user.hrprofile) 
            u_form=UserUpdateForm(instance=request.user)

        context = {
            'hr_form': hr_form,
            'u_form': u_form
        }   
        return render(request, 'profile/edithr.html', context)
    else:
        if request.method == 'POST':
            emp_form = EmployeeUpdateForm(request.POST,request.FILES,instance=request.user.employee)
            if emp_form.is_valid():
                emp_form.save()
                messages.success(request, f'Your account has been updated!')
                return redirect("home") 
        else:
            emp_form = EmployeeUpdateForm(instance=request.user.employee) 
        context = {
            'emp_form': emp_form
        }   
        return render(request, 'profile/editemployee.html', context)
        



def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request, "Successfully logged in")
            return redirect("/")
        else:
            messages.info(request, "Invalid credentials")
            return redirect('payroll/login')
    else:
        return render(request,'payroll/login.html')

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def view_list(request):
    if request.user.is_hr:
        employees=Employee.objects.filter(parent_hr=request.user.hrprofile)
    else:
        employees=Employee.objects.filter(parent_hr=request.user.employee.parent_hr)

    myFilter1=search_employee(request.GET,queryset=employees)

    employees=myFilter1.qs
    paginated_list=Paginator(employees,2)
    page_number=request.GET.get('page')
    employee_page_obj=paginated_list.get_page(page_number)
    context={'employees':employees,'myFilter1':myFilter1,'employee_page_obj':employee_page_obj}
    return render(request,'payroll/employee_list.html',context)

def EmployeeProfile(request,pk):
    employee = Employee.objects.get(id=pk)
    return render(request,'profile/employeeProfile.html',{'employee':employee})


def HrSignup(request):
    if request.method == 'GET':
        form = HrCreationForm()
        return render(request,'registration/signup_form.html',{'form':form})
    else:
        form = HrCreationForm(request.POST)
        
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            company_name = form.cleaned_data["company_name"]
            year_of_registration = form.cleaned_data["year_of_registration"]
            address = form.cleaned_data["address"]
            phone_number = form.cleaned_data["phone_number"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            full_name = str(first_name)+" "+str(last_name)

            if password1 == password2:
                if User.objects.filter(username = username).exists():
                    messages.info(request,"username already taken")
                    return render(request,'registration/signup_form.html',{'form':form})
                elif User.objects.filter(email = email).exists():
                    messages.info(request,"email already taken")
                    return render(request,'registration/signup_form.html',{'form':form})
                else:
                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,is_hr=True)   
                    user.save()
                    hr = hrProfile(user = user,full_name=full_name,phone_number=phone_number,address=address,company_name=company_name,year_of_registration=year_of_registration)
                    hr.save()
                    html_message = loader.render_to_string('main/email_regis.html',{'name':full_name})
                    message = 'Mano'
                    send_mail('Greetings from Mano!',message,settings. EMAIL_HOST_USER,[str(email)],fail_silently=True,html_message=html_message)
     
                    messages.success(request,'company registered sucessfully')
                    print("company created")

                return redirect('login')
            else:
                messages.info(request,"enter same password for both fields")
                return render(request,'registration/signup_form.html',{'form':form})
        
        else :
            messages.info(request,"please make sure you have filled all the fields correctly")
            return render(request,'registration/signup_form.html',{'form':form})

def EmployeeSignup(request):
    if request.user.is_authenticated and request.user.is_hr:
        if request.method == 'GET':
            form = EmployeeCreationForm()
            return render(request,'registration/signup_employee.html',{'form':form})
        else:
            form = EmployeeCreationForm(request.POST)
            
            if form.is_valid():
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password1 = form.cleaned_data["password1"]
                password2 = form.cleaned_data["password2"]
                phone_number = form.cleaned_data["phone_number"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                full_name = str(first_name)+" "+str(last_name)
                post = form.cleaned_data["post"]
                department = form.cleaned_data["department"]
                epf_deduction = form.cleaned_data["epf_deduction"]
                esi_deduction = form.cleaned_data["esi_deduction"]
                allowances_per_month = form.cleaned_data["allowances_per_month"]
                base_salary = form.cleaned_data["base_salary"]

                if password1 == password2:
                    if User.objects.filter(username = username).exists():
                        messages.info(request,"username already taken")
                        return render(request,'registration/signup_employee.html',{'form':form})
                    elif User.objects.filter(email = email).exists():
                        messages.info(request,"email already taken")
                        return render(request,'registration/signup_employee.html',{'form':form})
                    else:
                        user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,is_employee=True)
                        user.save()
                        current_hr = request.user
                        parent_hr = current_hr.hrprofile
                        employee = Employee(user = user,full_name=full_name,phone_number=phone_number,parent_hr=parent_hr,epf_deduction=epf_deduction,esi_deduction=esi_deduction,department=department,post=post,allowances_per_month=allowances_per_month,base_salary=base_salary,)
                        employee.save()
                        html_message = loader.render_to_string('main/email_add.html',{'name':full_name,'company':parent_hr.company_name,'company_admin':parent_hr.full_name})
                        message = 'Mano'
                        send_mail('Greetings from Mano!',message,settings. EMAIL_HOST_USER,[str(email)],fail_silently=True,html_message=html_message)
                        messages.success(request,'employee added sucessfully')
                        print("employee added")
                    
                    return redirect('home')

                else:
                    messages.info(request,"enter same password for both fields")
                    return render(request,'registration/signup_employee.html',{'form':form})
            
            else :
                messages.info(request,"please make sure you have filled all the fields correctly")
                return render(request,'registration/signup_employee.html',{'form':form})
    
    else:

        messages.info(request,"please be logged in as a company admin to add employees")
        return redirect('login')



                        






def Stpage(request): #take leave dashboard by emplyee
    return render(request,'leave/stpage.html')

                
                
def StLeaveApp(request):

    form = StdLeaveAppForm(request.POST)
    
    employee = Employee.objects.filter(user=request.user).first()

    if form.is_valid():
        form.instance.user=employee.user
        form.save()

    context = {'form':form}

    return render(request,'leave/stApp.html',context)
            
        
def Tpage(request):

    context = locals()

    return render(request,'leave/tpage.html',context)


def ShowApp(request): 
    
    hr = hrProfile.objects.filter(user=request.user).first()
    
    
    
    app2 = Leave.objects.filter(id=request.POST.get('answer')).all()

    for items in app2:

        items.status = request.POST.get('status')
        items.save()

    app = Leave.objects.filter(to_hr = hr).all()
    
    context = { 'app':app }

    return render(request,'leave/ShowApp.html',context)
        

def StatusOfApp(request):

    employee = Employee.objects.filter(user=request.user).first()

    app = Leave.objects.filter(user=employee.user).all()

    context = { 'app':app }

    return render(request,'leave/AppStatus.html',context)
