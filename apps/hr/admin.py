from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, Position, Employee, Dependent, Vacation, Attendance,
    Benefit, EmployeeBenefit, Training, EmployeeTraining,
    Evaluation, Document
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'budget', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('active',)
    ordering = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'base_salary', 'contract_type', 'hierarchy_level', 'active')
    list_filter = ('department', 'contract_type', 'hierarchy_level', 'active')
    search_fields = ('name', 'description')
    list_editable = ('active',)
    ordering = ('department', 'hierarchy_level', 'name')


class DependentInline(admin.TabularInline):
    model = Dependent
    extra = 0


class EmployeeBenefitInline(admin.TabularInline):
    model = EmployeeBenefit
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'position', 'department', 'hire_date', 'current_salary', 'active')
    list_filter = ('department', 'position', 'contract_type', 'active', 'on_vacation', 'on_leave')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'employee_id', 'cpf')
    list_editable = ('active',)
    inlines = [DependentInline, EmployeeBenefitInline]
    fieldsets = (
        ('Personal Data', {
            'fields': ('user', 'cpf', 'rg', 'birth_date', 'gender', 'marital_status', 'phone', 'mobile')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code'),
            'classes': ('collapse',)
        }),
        ('Professional Data', {
            'fields': ('employee_id', 'position', 'department', 'hire_date', 'termination_date', 'current_salary', 'work_hours', 'contract_type')
        }),
        ('Banking Data', {
            'fields': ('bank', 'agency', 'account', 'pix'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('active', 'on_vacation', 'on_leave')
        }),
    )
    ordering = ('employee_id',)


@admin.register(Dependent)
class DependentAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee', 'relationship', 'birth_date', 'active')
    list_filter = ('relationship', 'active')
    search_fields = ('name', 'employee__user__first_name', 'employee__user__last_name')
    list_editable = ('active',)


@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'days_requested', 'status', 'request_date')
    list_filter = ('status', 'start_date', 'request_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    list_editable = ('status',)
    date_hierarchy = 'start_date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'hours_worked', 'overtime_hours')
    list_filter = ('date', 'employee__department')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'date'
    ordering = ('-date', 'employee')


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('name', 'benefit_type', 'value', 'active')
    list_filter = ('benefit_type', 'active')
    search_fields = ('name', 'description')
    list_editable = ('active',)


@admin.register(EmployeeBenefit)
class EmployeeBenefitAdmin(admin.ModelAdmin):
    list_display = ('employee', 'benefit', 'value', 'start_date', 'end_date', 'active')
    list_filter = ('benefit', 'active', 'start_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'benefit__name')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'start_date', 'end_date', 'duration_hours', 'status', 'max_participants')
    list_filter = ('status', 'start_date', 'instructor')
    search_fields = ('name', 'description', 'instructor')
    list_editable = ('status',)
    date_hierarchy = 'start_date'


@admin.register(EmployeeTraining)
class EmployeeTrainingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training', 'status', 'grade', 'certificate')
    list_filter = ('status', 'certificate', 'training')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'training__name')
    list_editable = ('status', 'grade', 'certificate')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'evaluation_type', 'period_start', 'period_end', 'evaluator', 'overall_grade', 'evaluation_date')
    list_filter = ('evaluation_type', 'evaluation_date', 'evaluator')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'evaluator__first_name')
    date_hierarchy = 'evaluation_date'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'name', 'upload_date')
    list_filter = ('document_type', 'upload_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'name')
    date_hierarchy = 'upload_date'
