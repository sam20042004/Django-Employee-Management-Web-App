from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm
from .models import ( User,Employee,hrProfile,Leave )


class HrSignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields=['first_name','last_name','username','email','password1','password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hr = True
        user.save()
        hr = hrProfile.objects.create(user=user)
        return user


class EmployeeSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['first_name','last_name','username','email','password1','password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_employee = True
        user.save()
        employee = Employee.objects.create(user=user)
        return user

class UserUpdateForm(forms.ModelForm):
	
  email = forms.EmailField()
  first_name=forms.CharField()
  last_name=forms.CharField()	
  class Meta:
      model = User
      fields = ['username', 'email','first_name','last_name']

class EmplyeeUpdateForm(forms.ModelForm):
	profile_pic = forms.ImageField(widget=forms.FileInput,)
	class Meta:
		model = Employee
		fields = ['profile_pic','phone_number','address']


YEARS= [x for x in range(1940,2021)]

class HrCreationForm(forms.Form):
    phone_number = forms.CharField(max_length=12)
    address=forms.CharField(max_length=255)
    company_name = forms.CharField(max_length=255)
    year_of_registration = forms.DateField()
    username = forms.CharField(max_length=255)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'retype password'
        self.fields['email'].widget.attrs['placeholder'] = 'company mail-id'
        self.fields['year_of_registration'].widget.attrs['placeholder'] = 'year of registration (mm/dd/yyyy)'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'phone number'
        self.fields['address'].widget.attrs['placeholder'] = 'HQ address'
        self.fields['company_name'].widget.attrs['placeholder'] = 'Company name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'admin first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'admin last name'



class EmployeeCreationForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=12)
    post = forms.CharField(max_length=50)
    department = forms.CharField(max_length=50)
    epf_deduction = forms.IntegerField()
    esi_deduction = forms.IntegerField()
    allowances_per_month = forms.IntegerField()
    base_salary = forms.IntegerField()
    username = forms.CharField(max_length=255)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'employee username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype password'
        self.fields['email'].widget.attrs['placeholder'] = 'employee mail-id'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'employee phone number'
        self.fields['post'].widget.attrs['placeholder'] = 'employee post/job'
        self.fields['department'].widget.attrs['placeholder'] = 'department of employee'
        self.fields['epf_deduction'].widget.attrs['placeholder'] = 'EPF deduction (if any)'
        self.fields['esi_deduction'].widget.attrs['placeholder'] = 'ESI deduction (if any)'
        self.fields['allowances_per_month'].widget.attrs['placeholder'] = 'Allowances (if any)'
        self.fields['base_salary'].widget.attrs['placeholder'] = 'Base salary of employee'
        self.fields['first_name'].widget.attrs['placeholder'] = 'employee first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'employee last name'

class StdLeaveAppForm(forms.ModelForm):
    class Meta:
        model = Leave

        fields = ('reason', 'date','to_hr')

        widgets = {

            'reason': forms.TextInput,
            'to_hr':forms.TextInput(attrs={'class':'form-control','placeholder':'username','id':'to_hrr','type':'hidden'}),

        }

class UserUpdateForm(forms.ModelForm):
	
  email = forms.EmailField()
	
  class Meta:
      model = User
      fields = ['username', 'email']


class HrUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = hrProfile
        fields = '__all__'
        exclude=['user']


class EmployeeUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = Employee
        fields = '__all__'
        exclude=['user','parent_hr','department','post','epf_deduction','allowances_per_month','base_salary','esi_deduction']