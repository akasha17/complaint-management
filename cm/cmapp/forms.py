from django import forms
from .models import Complaint

class TechnicianStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
class PublicComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'customer_name', 'phone1', 'phone2', 'address',
            'product_type', 'complaint_details'
        ]
