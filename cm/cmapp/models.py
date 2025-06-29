from django.db import models
from django.contrib.auth.models import User

# Staff model (linked to Django User for login)
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()


# Technician model (linked to Django User for login)
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily allow null for migration
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.expertise})"


# Complaint model
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('solved', 'Solved'),
    ]

    customer_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    complaint_details = models.TextField()
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)

    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer_name} - {self.product_type} - {self.status}"
