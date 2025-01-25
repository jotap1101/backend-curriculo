from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']

@admin.register(DriversLicenseCategory)
class DriversLicenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state', 'created_at', 'updated_at']

admin.site.register(State)