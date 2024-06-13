from django.contrib import admin
from rate_employees.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'empid', 'enothi_id', 'ename', 'eemail', 'edesignation', 'edept', 'esection','edivision','edirectorate')
# Register your models here.
admin.site.register(Employee, EmployeeAdmin)