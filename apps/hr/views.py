from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    Department, Position, Employee, Dependent, Vacation, Attendance,
    Benefit, EmployeeBenefit, Training, EmployeeTraining,
    Evaluation, Document
)


@login_required
def hr_dashboard(request):
    """
    HR Dashboard with key metrics and overview
    """
    # Get basic statistics
    total_employees = Employee.objects.filter(active=True).count()
    total_departments = Department.objects.filter(active=True).count()
    employees_on_vacation = Employee.objects.filter(on_vacation=True).count()
    pending_vacation_requests = Vacation.objects.filter(status='REQUESTED').count()
    
    # Recent activities
    recent_employees = Employee.objects.filter(active=True).order_by('-created_at')[:5]
    recent_vacations = Vacation.objects.filter(status='APPROVED').order_by('-approval_date')[:5]
    upcoming_trainings = Training.objects.filter(
        start_date__gte=timezone.now(),
        status='PLANNED'
    ).order_by('start_date')[:5]
    
    # Department distribution
    department_stats = Department.objects.filter(active=True).annotate(
        employee_count=Count('employees')
    ).order_by('-employee_count')
    
    context = {
        'user': request.user,
        'page_title': 'HR Dashboard - ByteNest',
        'stats': {
            'total_employees': total_employees,
            'total_departments': total_departments,
            'employees_on_vacation': employees_on_vacation,
            'pending_vacation_requests': pending_vacation_requests,
        },
        'recent_employees': recent_employees,
        'recent_vacations': recent_vacations,
        'upcoming_trainings': upcoming_trainings,
        'department_stats': department_stats,
    }
    return render(request, 'hr/dashboard.html', context)


@login_required
def employees_list(request):
    """
    List all employees with filtering and search
    """
    employees = Funcionario.objects.filter(ativo=True).select_related('user', 'cargo', 'departamento')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(matricula__icontains=search_query) |
            Q(cpf__icontains=search_query)
        )
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        employees = employees.filter(departamento_id=department_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'vacation':
        employees = employees.filter(em_ferias=True)
    elif status_filter == 'license':
        employees = employees.filter(em_licenca=True)
    elif status_filter == 'active':
        employees = employees.filter(em_ferias=False, em_licenca=False)
    
    # Pagination
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get departments for filter dropdown
    departments = Departamento.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'user': request.user,
        'page_title': 'Employees - ByteNest',
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter,
        'status_filter': status_filter,
    }
    return render(request, 'hr/employees_list.html', context)


@login_required
def employee_detail(request, employee_id):
    """
    Employee detail view with all related information
    """
    employee = get_object_or_404(Funcionario, id=employee_id)
    
    # Get related data
    dependents = employee.dependentes.filter(ativo=True)
    vacations = employee.ferias.all().order_by('-data_solicitacao')[:10]
    recent_points = employee.pontos.all().order_by('-data')[:10]
    benefits = employee.beneficios_funcionario.filter(ativo=True)
    trainings = employee.treinamentos_funcionario.all().order_by('-treinamento__data_inicio')[:10]
    evaluations = employee.avaliacoes.all().order_by('-data_avaliacao')[:5]
    documents = employee.documentos.all().order_by('-data_upload')[:10]
    
    context = {
        'user': request.user,
        'page_title': f'{employee.nome} - Employee Details',
        'employee': employee,
        'dependents': dependents,
        'vacations': vacations,
        'recent_points': recent_points,
        'benefits': benefits,
        'trainings': trainings,
        'evaluations': evaluations,
        'documents': documents,
    }
    return render(request, 'hr/employee_detail.html', context)


@login_required
def departments_list(request):
    """
    List all departments with employee counts
    """
    departments = Departamento.objects.filter(ativo=True).annotate(
        employee_count=Count('funcionarios'),
        active_employees=Count('funcionarios', filter=Q(funcionarios__ativo=True))
    ).order_by('nome')
    
    context = {
        'user': request.user,
        'page_title': 'Departments - ByteNest',
        'departments': departments,
    }
    return render(request, 'hr/departments_list.html', context)


@login_required
def department_detail(request, department_id):
    """
    Department detail view with employees and statistics
    """
    department = get_object_or_404(Departamento, id=department_id)
    employees = department.funcionarios.filter(ativo=True).select_related('user', 'cargo')
    positions = department.cargos.filter(ativo=True)
    
    # Department statistics
    total_employees = employees.count()
    employees_on_vacation = employees.filter(em_ferias=True).count()
    employees_on_license = employees.filter(em_licenca=True).count()
    
    context = {
        'user': request.user,
        'page_title': f'{department.nome} - Department Details',
        'department': department,
        'employees': employees,
        'positions': positions,
        'stats': {
            'total_employees': total_employees,
            'employees_on_vacation': employees_on_vacation,
            'employees_on_license': employees_on_license,
        }
    }
    return render(request, 'hr/department_detail.html', context)


@login_required
def vacation_requests(request):
    """
    Vacation requests management
    """
    vacation_requests = Ferias.objects.all().select_related('funcionario__user').order_by('-data_solicitacao')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        vacation_requests = vacation_requests.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(vacation_requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': request.user,
        'page_title': 'Vacation Requests - ByteNest',
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'hr/vacation_requests.html', context)


@login_required
@require_http_methods(["POST"])
def approve_vacation(request, vacation_id):
    """
    Approve vacation request
    """
    vacation = get_object_or_404(Ferias, id=vacation_id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'approve':
                vacation.status = 'APROVADO'
                vacation.aprovado_por = request.user
                vacation.data_aprovacao = timezone.now()
                vacation.funcionario.em_ferias = True
                vacation.funcionario.save()
                vacation.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Vacation request approved successfully!'
                })
            elif action == 'reject':
                vacation.status = 'REJEITADO'
                vacation.aprovado_por = request.user
                vacation.data_aprovacao = timezone.now()
                vacation.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Vacation request rejected.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Error processing request.'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)


@login_required
def attendance_tracking(request):
    """
    Attendance tracking and point management
    """
    # Get current month's attendance
    current_month = timezone.now().replace(day=1)
    next_month = (current_month + timedelta(days=32)).replace(day=1)
    
    attendance_records = Ponto.objects.filter(
        data__gte=current_month,
        data__lt=next_month
    ).select_related('funcionario__user', 'funcionario__departamento').order_by('-data')
    
    # Filter by employee
    employee_filter = request.GET.get('employee', '')
    if employee_filter:
        attendance_records = attendance_records.filter(funcionario_id=employee_filter)
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        attendance_records = attendance_records.filter(funcionario__departamento_id=department_filter)
    
    # Pagination
    paginator = Paginator(attendance_records, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    employees = Funcionario.objects.filter(ativo=True).order_by('user__first_name')
    departments = Departamento.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'user': request.user,
        'page_title': 'Attendance Tracking - ByteNest',
        'page_obj': page_obj,
        'employees': employees,
        'departments': departments,
        'employee_filter': employee_filter,
        'department_filter': department_filter,
    }
    return render(request, 'hr/attendance_tracking.html', context)


@login_required
def training_management(request):
    """
    Training management and tracking
    """
    trainings = Treinamento.objects.all().order_by('-data_inicio')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        trainings = trainings.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(trainings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': request.user,
        'page_title': 'Training Management - ByteNest',
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'hr/training_management.html', context)


@login_required
def training_detail(request, training_id):
    """
    Training detail with participants
    """
    training = get_object_or_404(Treinamento, id=training_id)
    participants = training.participantes_treinamento.all().select_related('funcionario__user')
    
    context = {
        'user': request.user,
        'page_title': f'{training.nome} - Training Details',
        'training': training,
        'participants': participants,
    }
    return render(request, 'hr/training_detail.html', context)


@login_required
def performance_evaluations(request):
    """
    Performance evaluations management
    """
    evaluations = Avaliacao.objects.all().select_related(
        'funcionario__user', 'avaliador'
    ).order_by('-data_avaliacao')
    
    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        evaluations = evaluations.filter(tipo=type_filter)
    
    # Pagination
    paginator = Paginator(evaluations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': request.user,
        'page_title': 'Performance Evaluations - ByteNest',
        'page_obj': page_obj,
        'type_filter': type_filter,
    }
    return render(request, 'hr/performance_evaluations.html', context)


@login_required
def benefits_management(request):
    """
    Benefits management
    """
    benefits = Beneficio.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'user': request.user,
        'page_title': 'Benefits Management - ByteNest',
        'benefits': benefits,
    }
    return render(request, 'hr/benefits_management.html', context)


@login_required
def reports_analytics(request):
    """
    HR Reports and Analytics
    """
    # Employee statistics
    total_employees = Funcionario.objects.filter(ativo=True).count()
    employees_by_department = Departamento.objects.filter(ativo=True).annotate(
        employee_count=Count('funcionarios', filter=Q(funcionarios__ativo=True))
    ).order_by('-employee_count')
    
    # Attendance statistics
    current_month = timezone.now().replace(day=1)
    monthly_attendance = Ponto.objects.filter(
        data__gte=current_month
    ).aggregate(
        total_hours=Avg('horas_trabalhadas'),
        total_overtime=Avg('horas_extras')
    )
    
    # Training statistics
    training_stats = Treinamento.objects.aggregate(
        total_trainings=Count('id'),
        completed_trainings=Count('id', filter=Q(status='CONCLUIDO'))
    )
    
    # Performance statistics
    performance_stats = Avaliacao.objects.aggregate(
        average_rating=Avg('nota_geral'),
        total_evaluations=Count('id')
    )
    
    context = {
        'user': request.user,
        'page_title': 'HR Reports & Analytics - ByteNest',
        'stats': {
            'total_employees': total_employees,
            'monthly_attendance': monthly_attendance,
            'training_stats': training_stats,
            'performance_stats': performance_stats,
        },
        'employees_by_department': employees_by_department,
    }
    return render(request, 'hr/reports_analytics.html', context)
