from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()


class Department(models.Model):
    """
    Model for company departments
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, 
                               null=True, blank=True, 
                               related_name='managed_departments')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Position(models.Model):
    """
    Model for job positions/roles
    """
    CONTRACT_TYPE_CHOICES = [
        ('CLT', 'CLT'),
        ('PJ', 'Legal Entity'),
        ('INTERNSHIP', 'Internship'),
        ('TEMPORARY', 'Temporary'),
        ('OUTSOURCED', 'Outsourced'),
    ]
    
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, 
                                  related_name='positions')
    description = models.TextField(blank=True, null=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contract_type = models.CharField(max_length=20, 
                                    choices=CONTRACT_TYPE_CHOICES, default='CLT')
    hierarchy_level = models.IntegerField(default=1, 
                                         validators=[MinValueValidator(1), 
                                                   MaxValueValidator(10)])
    requirements = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['department', 'hierarchy_level', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"


class Employee(models.Model):
    """
    Model for employees
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('STABLE_UNION', 'Stable Union'),
    ]
    
    # Personal data
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                               related_name='employee')
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, 
                                     choices=MARITAL_STATUS_CHOICES, 
                                     blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Professional data
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT, 
                                related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, 
                                  related_name='employees')
    hire_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    work_hours = models.IntegerField(default=40)  # hours per week
    contract_type = models.CharField(max_length=20, 
                                    choices=Position.CONTRACT_TYPE_CHOICES, 
                                    default='CLT')
    
    # Banking data
    bank = models.CharField(max_length=100, blank=True, null=True)
    agency = models.CharField(max_length=10, blank=True, null=True)
    account = models.CharField(max_length=20, blank=True, null=True)
    pix = models.CharField(max_length=100, blank=True, null=True)
    
    # Status
    active = models.BooleanField(default=True)
    on_vacation = models.BooleanField(default=False)
    on_leave = models.BooleanField(default=False)
    
    # Control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['user__first_name', 'employee_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
    
    @property
    def name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def company_time(self):
        if self.termination_date:
            return self.termination_date - self.hire_date
        return timezone.now().date() - self.hire_date


class Dependent(models.Model):
    """
    Model for employee dependents
    """
    RELATIONSHIP_CHOICES = [
        ('CHILD', 'Child'),
        ('SPOUSE', 'Spouse'),
        ('FATHER', 'Father'),
        ('MOTHER', 'Mother'),
        ('SIBLING', 'Sibling'),
        ('OTHER', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='dependents')
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    birth_date = models.DateField()
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Dependent'
        verbose_name_plural = 'Dependents'
        ordering = ['employee', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_relationship_display()}"


class Vacation(models.Model):
    """
    Model for vacation control
    """
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='vacations')
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='REQUESTED')
    notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                   null=True, blank=True, 
                                   related_name='approved_vacations')
    approval_date = models.DateTimeField(blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Vacation'
        verbose_name_plural = 'Vacations'
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.employee.name} - {self.start_date} to {self.end_date}"


class Attendance(models.Model):
    """
    Model for attendance control
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='attendance_records')
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True)
    lunch_out = models.TimeField(blank=True, null=True)
    lunch_in = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        ordering = ['-date', 'employee']
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee.name} - {self.date}"


class Benefit(models.Model):
    """
    Model for benefits
    """
    TYPE_CHOICES = [
        ('MEAL_VOUCHER', 'Meal Voucher'),
        ('FOOD_VOUCHER', 'Food Voucher'),
        ('TRANSPORT_VOUCHER', 'Transport Voucher'),
        ('HEALTH_PLAN', 'Health Plan'),
        ('DENTAL_PLAN', 'Dental Plan'),
        ('LIFE_INSURANCE', 'Life Insurance'),
        ('EDUCATION_AID', 'Education Aid'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    benefit_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Benefit'
        verbose_name_plural = 'Benefits'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class EmployeeBenefit(models.Model):
    """
    Model to relate employees with benefits
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='employee_benefits')
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE, 
                               related_name='benefit_employees')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Employee Benefit'
        verbose_name_plural = 'Employee Benefits'
        unique_together = ['employee', 'benefit']
    
    def __str__(self):
        return f"{self.employee.name} - {self.benefit.name}"


class Training(models.Model):
    """
    Model for training programs
    """
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_hours = models.IntegerField()  # in hours
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='PLANNED')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_participants = models.IntegerField(default=20)
    
    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Training Programs'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class EmployeeTraining(models.Model):
    """
    Model to relate employees with training programs
    """
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='employee_trainings')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, 
                                related_name='training_participants')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='ENROLLED')
    grade = models.DecimalField(max_digits=4, decimal_places=2, 
                               blank=True, null=True)
    certificate = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Training Participation'
        verbose_name_plural = 'Training Participations'
        unique_together = ['employee', 'training']
    
    def __str__(self):
        return f"{self.employee.name} - {self.training.name}"


class Evaluation(models.Model):
    """
    Model for performance evaluations
    """
    TYPE_CHOICES = [
        ('ANNUAL', 'Annual Evaluation'),
        ('PROBATION', 'Probation Period'),
        ('PROMOTION', 'Promotion Evaluation'),
        ('DEVELOPMENT', 'Development Evaluation'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='evaluations')
    evaluation_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, 
                                 related_name='conducted_evaluations')
    overall_grade = models.DecimalField(max_digits=4, decimal_places=2, 
                                       blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)
    improvement_points = models.TextField(blank=True, null=True)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
        ordering = ['-evaluation_date']
    
    def __str__(self):
        return f"{self.employee.name} - {self.get_evaluation_type_display()}"


class Document(models.Model):
    """
    Model for employee documents
    """
    TYPE_CHOICES = [
        ('CONTRACT', 'Employment Contract'),
        ('ADDENDUM', 'Contract Addendum'),
        ('TERMINATION', 'Termination Letter'),
        ('VACATION', 'Vacation Request'),
        ('MEDICAL_LEAVE', 'Medical Leave'),
        ('CERTIFICATE', 'Certificate'),
        ('OTHER', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                                related_name='documents')
    document_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.employee.name} - {self.name}"
