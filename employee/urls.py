from django.urls import path
from .views import *

urlpatterns = [
    path('', GetEmployees.as_view(), name='get_employees'),
    path('create/', CreateEmployee.as_view(), name='create_employee'),
    path('<uuid:pk>/detail/', DetailEmployee.as_view(), name='detail_employee'),
    path('<uuid:pk>/update/', UpdateEmployee.as_view(), name='update_employee'),
    path('<uuid:pk>/delete/', DeleteEmployee.as_view(), name='delete_employee'),
]