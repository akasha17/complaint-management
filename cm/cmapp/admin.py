# # admin.py

# from django.contrib import admin
# from .models import Staff, Technician, Complaint

# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display = ['user', 'phone', 'address']

# @admin.register(Technician)
# class TechnicianAdmin(admin.ModelAdmin):
#     list_display = ['name', 'expertise', 'phone', 'available']

# @admin.register(Complaint)
# class ComplaintAdmin(admin.ModelAdmin):
#     list_display = ['customer_name', 'product_type', 'status', 'assigned_staff', 'assigned_technician', 'date_reported']
#     list_filter = ['status']
#     search_fields = ['customer_name', 'product_type']
