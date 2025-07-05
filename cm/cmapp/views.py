from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from django.contrib import messages
from django.db.models import Q
from .models import Complaint, Staff, Technician


# -------------------------------
# Forms
# -------------------------------

class PublicComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['customer_name', 'phone1', 'phone2', 'address', 'product_type', 'complaint_details']

class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['phone', 'address']

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'expertise', 'phone', 'available']

class AssignForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['assigned_technician', 'status']

class TechnicianStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']

# -------------------------------
# Public Views
# -------------------------------

def index(request):
    return render(request, 'index.html')

def submit_complaint(request):
    if request.method == 'POST':
        form = PublicComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'thanks.html')
    else:
        form = PublicComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})

# -------------------------------
# Authentication Views
# -------------------------------

def login_unified(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif hasattr(user, 'staff'):
                return redirect('staff_dashboard')
            elif hasattr(user, 'technician'):
                return redirect('technician_dashboard')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password.',
                'username': username
            })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# -------------------------------
# Registration Views
# -------------------------------

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already taken."})

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        return redirect('login')

    return render(request, 'register.html')

# -------------------------------
# Admin Views
# -------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    complaints = Complaint.objects.all()
    staff_list = Staff.objects.all()
    technicians = Technician.objects.all()

    total_complaints = complaints.count()
    assigned = complaints.filter(assigned_technician__isnull=False).count()
    not_assigned = complaints.filter(assigned_technician__isnull=True).count()
    completed = complaints.filter(status='completed').count()

    return render(request, 'admin/admin_dashboard.html', {
        'complaints': complaints,
        'staff': staff_list,
        'technicians': technicians,
        'chart_data': {
            'total': total_complaints,
            'assigned': assigned,
            'not_assigned': not_assigned,
            'completed': completed,
        }
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_staff(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            is_staff=True
        )
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.user = user
            staff.save()
            return redirect('admin_dashboard')
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_technician(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return render(request, 'technician/add.html', {
                'form': TechnicianForm(request.POST),
                'error': 'Username already exists'
            })

        user = User.objects.create_user(username=username, password=password, email=email)

        form = TechnicianForm(request.POST)
        if form.is_valid():
            technician = form.save(commit=False)
            technician.user = user
            technician.save()
            return redirect('admin_dashboard')
    else:
        form = TechnicianForm()

    return render(request, 'technician/add.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def complaint_list(request):
    complaints = Complaint.objects.all()
    return render(request, 'complaints/list.html', {'complaints': complaints})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def assign_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = AssignForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = AssignForm(instance=complaint)
    return render(request, 'complaints/assign.html', {'form': form, 'complaint': complaint})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if staff.user:
        staff.user.delete()
    staff.delete()
    messages.success(request, "Staff deleted successfully.")
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_technician(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if technician.user:
        technician.user.delete()
    technician.delete()
    messages.success(request, "Technician deleted successfully.")
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    complaint.delete()
    messages.success(request, "Complaint deleted successfully.")
    return redirect('admin_dashboard')

# -------------------------------
# Staff Views
# -------------------------------

@login_required
def staff_dashboard(request):
    complaints = Complaint.objects.all().select_related('assigned_technician')
    return render(request, 'staff/staff_dashboard.html', {
        'complaints': complaints
    })

@login_required
def staff_assign_technician(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    success = False

    if request.method == 'POST':
        form = AssignForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            success = True  # Trigger popup in template

    else:
        form = AssignForm(instance=complaint)

    return render(request, 'complaints/assign.html', {
        'form': form,
        'complaint': complaint,
        'success': success
    })

# -------------------------------
# Technician Views
# -------------------------------

@login_required
def technician_dashboard(request):
    try:
        technician = Technician.objects.get(user=request.user)
        complaints = Complaint.objects.filter(assigned_technician=technician)
    except Technician.DoesNotExist:
        complaints = []

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint = get_object_or_404(Complaint, pk=complaint_id, assigned_technician=technician)
        form = TechnicianStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('technician_dashboard')

    complaint_forms = [(c, TechnicianStatusForm(instance=c)) for c in complaints]

    return render(request, 'technician/technician_dashboard.html', {
        'complaint_forms': complaint_forms
    })
