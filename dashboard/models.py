from django.db import models
from accounts.models import UserAccount
from django.db.models.fields.related import OneToOneField
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# 
# from oscar.models.fields.slugfield import SlugField

# Create your models here.

# ............***............ Company ............***............


class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='company', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    email = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return self.name

# ............***............ Organization ............***............


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_total_employee(self):
        total_employee = Employee.objects.filter(designation__department__name = self.name).count()
        return total_employee


class Designation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                   null= True, blank=True, related_name='designations')

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHERS', 'Others')
    ]
    JOB_TYPE = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERN', 'Intern'),
        ('PROBATIONARY', 'Probationary'),
        ('CONTRACTUAL', 'Contractual'),
    ]
    STATUS = [
        ('EMPLOYED', 'Employed'),
        ('FURLOUGHED', 'Furloughed'),
        ('TERMINATED', 'Terminated')
    ]
    employee_id = models.CharField(max_length=50, default='TS000')
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='employee', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='employees')
    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='employees')
    gender = models.CharField(choices=GENDER, default="MALE",
                              max_length=120)
    job_type = models.CharField(choices=JOB_TYPE, default="PROBATIONARY",
                                max_length=120)
    job_status = models.CharField(choices=STATUS, default="EMPLOYED",
                                  max_length=120)
    personal_phone_number = models.CharField(max_length=50,
                                             null=True, blank=True)
    personal_email = models.CharField(max_length=50,
                                      null=True, blank=True)
    contact_person = models.CharField(max_length=250,
                                      null=True, blank=True)
    linkedin_profile = models.CharField(max_length=250,
                                        null=True, blank=True)
    date_of_birth = models.DateTimeField(null=False, blank=False)
    physical_device_user_id = models.CharField(max_length=100, null=True,
                                               blank=True)
    work_mail = models.CharField(max_length=100, null=True, blank=True)
    work_phone_number = models.CharField(max_length=100, null=True,
                                         blank=True)
    user = models.OneToOneField(UserAccount, on_delete=models.SET_NULL,
                                null=True, blank=True)
    # payroll_structure = models.CharField(choices=PAYROLL_STRUCTURE, default="STANDARD",
    #                                      max_length=120)
    salary = models.IntegerField(default=00000, null=True, blank=True)
    joining_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        first_name = self.first_name
        last_name = self.last_name
        self.name = first_name+' ' + last_name
        self.save()
        return self.name

    def get_gender(self):
        if self.gender == 'MALE':
            return 'Male'
        elif self.gender == 'FEMALE':
            return 'Female'
        else:
            return 'Others'

    def get_job_type(self):
        if self.job_type == 'FULL_TIME':
            return 'Full Time'
        elif self.job_type == 'PART_TIME':
            return 'Part Time'
        elif self.job_type == 'INTERN':
            return 'Intern'
        elif self.job_type == 'PROBATIONARY':
            return 'Probationary'
        else:
            return 'Contractual'

    def get_job_status(self):
        if self.job_status == 'EMPLOYED':
            return 'Employed'
        elif self.job_status == 'FURLOUGHED':
            return 'Furloughed'
        else:
            return 'Terminated'

    def generate_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

# ............***............ Project ............***............

class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    submitted_date = models.DateTimeField(null=True, blank=True)
    team_leader = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='projects')
    employee = models.ManyToManyField(Employee, null=True, blank=True,
                                      related_name='employee_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Leave ............***............


class LeaveApplication(models.Model):
    LEAVE_TYPE = [
        ('CASUAL', 'Casual'),
        ('ANNUAL', 'Annual'),
        ('OTHERS', 'Others')
    ]
    DAY_TYPE = [
        ('FULL_DAY', 'Full Day'),
        ('HALF_DAY', 'Half Day'),
        ('OTHERS', 'Others')
    ]
    STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECT', 'Reject')
    ]
    title = models.CharField(max_length=250)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    leave_type = models.CharField(choices=LEAVE_TYPE, default="CASUAL",
                                  max_length=120)
    start_date = models.DateTimeField(max_length=50)
    end_date = models.DateTimeField(max_length=50)
    day_type = models.CharField(choices=DAY_TYPE, default="FULL_DAY",
                                max_length=120)
    status = models.CharField(choices=STATUS, default="PENDING",
                              max_length=120)
    remarks = models.TextField(null=True, blank=True)
    application = models.FileField(upload_to='leaves', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.leave_type

    def get_day_type(self):
        if self.day_type == 'FULL_DAY':
            return 'Full Day'
        elif self.day_type == 'HALF_DAY':
            return 'Half Day'
        else:
            return 'Others'

    def get_leave_type(self):
        if self.leave_type == 'CASUAL':
            return 'Casual'
        elif self.leave_type == 'ANNUAL':
            return 'Annual'
        else:
            return 'Others'

    def get_status(self):
        if self.status == 'PENDING':
            return 'Pending'
        elif self.status == 'APPROVED':
            return 'Approved'
        else:
            return 'Reject'


# ............***............ Expense ............***............


class ExpenseType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Expense(models.Model):

    STATUS =[
        ('PAID', 'Paid'),
        ('REMAINING', 'Remaining'),
    ]
    title = models.CharField(max_length=350)
    document_ref_id = models.CharField(max_length=50, null=True, blank=True)
    expense_type = models.ForeignKey(ExpenseType, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='expenses')
    status = models.CharField(choices=STATUS,
                              default='UNPAID', max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='expenses')
    payment_date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=850, null=True, blank=True)
    payment_method = models.CharField(max_length=150, null=True, blank=True)
    payment_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='expenses')
    total_amount = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)
    file = models.FileField(upload_to='invoice', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)


    def get_status(self):
        if self.status == 'PAID':
            return 'Paid'
        else:
            return 'Remaining'


# ............***............ Office Expense ............***............

class OfficeExpense(models.Model):
    STATUS = [
        ('PAID', 'Paid'),
        ('REMAINING', 'Remaining'),
    ]
    title = models.CharField(max_length=500)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0.0)
    unit_price = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)
    purchased_from = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS,
                              default='UNPAID', max_length=100)
    purchased_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='office_expenses')
    payment_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='office_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)

    def get_status(self):
        if self.status == 'PAID':
            return 'Paid'
        else:
            return 'Remaining'


# ............***............ Others Expense ............***............

class OthersExpense(models.Model):
    STATUS = [
        ('PAID', 'Paid'),
        ('REMAINING', 'Remaining'),
    ]
    title = models.CharField(max_length=500)
    total_price = models.FloatField(default=0.0)
    paid_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)
    purchased_from = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS,
                              default='UNPAID', max_length=100)
    expense_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='other_expenses')
    payment_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='other_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)

    def get_status(self):
        if self.status == 'PAID':
            return 'Paid'
        else:
            return 'Remaining'


# ............***............ Salary ............***............

class Salary(models.Model):
    STATUS = [
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('HOLD', 'Hold'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='salarys')
    disburse_date = models.DateField(null=True, blank=True)
    basic_salary = models.FloatField(default=0.0)
    deduction_amount = models.FloatField(default=0.0)
    disburse_amount = models.FloatField(default=0.0)
    disburse_method = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(choices=STATUS,
                              default='UNPAID', max_length=100)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.name

    class Meta:
        ordering = ('created_at',)

    def get_status(self):
        if self.status == 'PAID':
            return 'Paid'
        if self.status == 'UNPAID':
            return 'Unpaid'
        else:
            return 'Hold'

# ............***............ Income ............***............


class IncomeType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    STATUS =[
        ('PAID', 'Paid'),
        ('REMAINING', 'Remaining'),
    ]
    title = models.CharField(max_length=350)
    document_ref_id = models.CharField(max_length=50, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    income_type = models.ForeignKey(IncomeType, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='incomes')
    status = models.CharField(choices=STATUS,
                              default='UNPAID', max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='incomes')
    received_date = models.DateTimeField(null=True, blank=True)
    remarks = models.CharField(max_length=850, null=True, blank=True)
    payment_method = models.CharField(max_length=150, null=True, blank=True)
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='incomes')
    total_amount = models.FloatField(default=0.0)
    received_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)
    file = models.FileField(upload_to='invoice', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)

    def get_status(self):
        if self.status == 'PAID':
            return 'Paid'
        else:
            return 'Remaining'


# ............***............ Assets ............***............

class AssetType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS = [
        ('PENDING', 'Pending'),
        ('ACCEPT', 'Accept'),
        ('REVOKE', 'Revoke'),
        ('DECLINE', 'Decline'),
    ]
    asset_id = models.CharField(max_length=50, default='TS-AST-00000')
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    vendor = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default='PENDING',max_length=100)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='assets')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='assets')
    assign_to = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='assets')
    assign_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='assign_by_assets')
    revoke_by = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='revoke_by_assets')
    employee_list = models.ManyToManyField(Employee, null=True, blank=True,
                                           related_name='employee_list_assets')
    purchase_amount = models.IntegerField(default=00000)
    quality = models.CharField(max_length=250, null=True, blank=True)
    purchase_date = models.CharField(max_length=20,null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    assign_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asset_id
    
    def get_status(self):
        if self.status == 'PENDING':
            return 'Pending'
        elif self.status == 'ACCEPT':
            return 'Accept'
        elif self.status == 'REVOKE':
            return 'Revoke'
        elif self.status == 'DECLINE':
            return 'Decline'
        else:
            return 'Approved'


# ............***............ Vacancy ............***............

class Vacancy(models.Model):
    department = OneToOneField(Department, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='vacancys')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='vacancys')
    total_number_of_employee = models.IntegerField(default=0)
    vacancy_number_of_employee = models.IntegerField(default=0)

    def __str__(self):
        if self.department:
            return self.department.name
        return self.id

    def get_vacancy_number_of_employee(self):
        designation_qs = Designation.objects.filter(name = self.department.name).last()
        self.vacancy_number_of_employee = designation_qs.employees.count()
        self.save()
        return self.vacancy_number_of_employee

    def get_vacancy(self):
        return self.total_number_of_employee - self.vacancy_number_of_employee


# ............***............ Evaluation ............***............

class Evaluation(models.Model):
    title = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='evaluations')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Appointment Letter ............***............


class AppointmentLetter(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='appointment_letter', null=True, blank=True)
    employee = models.ForeignKey(Employee, null= True, blank=True,
                                 on_delete=models.SET_NULL, related_name='appointment_letters')

    def __str__(self):
        return self.title


# # ............***............ Payroll ............***............
#
#
class Payroll(models.Model):
    STATUS = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid')
    ]
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='payrolls')
    salary_month = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField(default=0)
    file = models.FileField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default='UNPAID', max_length=50)

    def __str__(self):
        return self.title

    def get_status(self):
        if self.status == 'UNPAID':
            return 'Unpaid'
        else:
            return 'Paid'

    def get_number_of_employee(self):
        department_qs = Department.objects.filter(name = self.department.name).last()
        number_of_employee = department_qs.employee.count()
        return number_of_employee


class SalaryChange(models.Model):
    STATUS = [
        ('PENDING', 'Pending'),
        ('ACCEPT', 'Accept')
    ]
    employee = models.ForeignKey(Employee, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='salary_changes')
    requester = models.ForeignKey(Employee, null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='requester_salary_changes')
    new_salary = models.IntegerField(default=00000)
    change_reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50,
                              choices=STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.employee:
            return self.employee.name
        return self.id

    def get_status(self):
        if self.status == 'PENDING':
            return 'Pending'
        return 'Accept'

# ............***........... Notice ............***............


class Notice(models.Model):
    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                null=True,blank=True, related_name='notices')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
