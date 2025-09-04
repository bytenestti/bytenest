from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Dashboard
    path('', views.hr_dashboard, name='dashboard'),
    
    # Employees
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    
    # Departments
    path('departments/', views.departments_list, name='departments_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
    
    # Vacation Management
    path('vacations/', views.vacation_requests, name='vacation_requests'),
    path('vacations/<int:vacation_id>/approve/', views.approve_vacation, name='approve_vacation'),
    
    # Attendance
    path('attendance/', views.attendance_tracking, name='attendance_tracking'),
    
    # Training
    path('training/', views.training_management, name='training_management'),
    path('training/<int:training_id>/', views.training_detail, name='training_detail'),
    
    # Performance
    path('performance/', views.performance_evaluations, name='performance_evaluations'),
    
    # Benefits
    path('benefits/', views.benefits_management, name='benefits_management'),
    
    # Reports
    path('reports/', views.reports_analytics, name='reports_analytics'),
]
