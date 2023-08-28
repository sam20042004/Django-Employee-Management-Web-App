import django_filters
from django_filters import CharFilter,ChoiceFilter
from django.contrib.auth.models import User
from .models import Employee


class search_user(django_filters.FilterSet):
    class Meta:
        model=User
        fields = ['username']
        


class search_employee(django_filters.FilterSet):
    Department=CharFilter(field_name='department',lookup_expr='icontains',label='Department')
    post=CharFilter(field_name='post',lookup_expr='icontains',label='Post')
    employee=CharFilter(field_name='full_name',lookup_expr='icontains',label='Employee')
    class Meta:
        model=Employee
        fields = ['employee','Department','post']
        
        
    