from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['first_name', 'last_name']
    filter_horizontal = ['groups', 'user_permissions']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    readonly_fields = ['last_login', 'date_joined']
    ordering = ['first_name', 'last_name']
    filter_horizontal = ['groups', 'user_permissions']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    list_display = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['first_name', 'last_name', 'username', 'email']
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    list_per_page = 10
    list_max_show_all = 100
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    save_on_top = True
    save_as = True
    save_as_continue = True
    save_as_continue = True
    show_full_result_count = True