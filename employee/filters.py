from django_filters import rest_framework
from .models import Employee

class EmployeeFilter(rest_framework.FilterSet):
    is_active = rest_framework.BooleanFilter(field_name='is_active')
    is_staff = rest_framework.BooleanFilter(field_name='is_staff')
    is_superuser = rest_framework.BooleanFilter(field_name='is_superuser')

    class Meta:
        model = Employee
        fields = ['is_active', 'is_staff', 'is_superuser']