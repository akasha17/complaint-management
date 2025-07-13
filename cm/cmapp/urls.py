from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.submit_complaint, name='submit_complaint'),
    path('register/', views.register_user, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/assign/<int:pk>/', views.staff_assign_technician, name='staff_assign_technician'),
    path('technician/dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/<int:pk>/assign/', views.assign_complaint, name='assign_complaint'),
    path('staff/register/', views.register_staff, name='register_staff'),
    path('technician/add/', views.add_technician, name='add_technician'),
    # Delete Views
    path('dashboard/delete_staff/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('dashboard/delete_technician/<int:pk>/', views.delete_technician, name='delete_technician'),
    path('dashboard/delete_complaint/<int:pk>/', views.delete_complaint, name='delete_complaint'),

    path('login', views.login_unified, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
