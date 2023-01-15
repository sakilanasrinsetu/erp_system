from django.contrib import admin
from dashboard.models import *

# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = Company


admin.site.register(Company, CompanyAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

    class Meta:
        model = Department


admin.site.register(Department, DepartmentAdmin)


class DesignationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department']

    class Meta:
        model = Designation


admin.site.register(Designation, DesignationAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee_id','name', 'designation','job_type', 'company']

    class Meta:
        model = Employee


admin.site.register(Employee, EmployeeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','title']

    class Meta:
        model = Project


admin.site.register(Project, ProjectAdmin)


class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ['id','employee','status']

    class Meta:
        model = LeaveApplication


admin.site.register(LeaveApplication, LeaveApplicationAdmin)


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']

    class Meta:
        model = ExpenseType


admin.site.register(ExpenseType, ExpenseTypeAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'document_ref_id']

    class Meta:
        model = Expense


admin.site.register(Expense, ExpenseAdmin)


class OthersExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','title']

    class Meta:
        model = OfficeExpense


admin.site.register(OfficeExpense, OthersExpenseAdmin)


class OthersExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','title']

    class Meta:
        model = OthersExpense


admin.site.register(OthersExpense, OthersExpenseAdmin)


class SalaryAdmin(admin.ModelAdmin):
    list_display = ['id','employee']

    class Meta:
        model = Salary


admin.site.register(Salary, SalaryAdmin)


class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']

    class Meta:
        model = IncomeType


admin.site.register(IncomeType, IncomeTypeAdmin)


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id','title']

    class Meta:
        model = Income


admin.site.register(Income, IncomeAdmin)


class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['id','name']

    class Meta:
        model = AssetType


admin.site.register(AssetType, AssetTypeAdmin)


class AssetAdmin(admin.ModelAdmin):
    list_display = ['id','asset_id','name']

    class Meta:
        model = Asset


admin.site.register(Asset, AssetAdmin)


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id']

    class Meta:
        model = Vacancy


admin.site.register(Vacancy, VacancyAdmin)


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['id','title','employee']

    class Meta:
        model = Evaluation


admin.site.register(Evaluation, EvaluationAdmin)


class AppointmentLetterAdmin(admin.ModelAdmin):
    list_display = ['id','title','employee']

    class Meta:
        model = AppointmentLetter


admin.site.register(AppointmentLetter, AppointmentLetterAdmin)


class SalaryChangeAdmin(admin.ModelAdmin):
    list_display = ['id','employee','requester','new_salary','status']

    class Meta:
        model = SalaryChange


admin.site.register(SalaryChange, SalaryChangeAdmin)


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at']

    class Meta:
        model = Notice


admin.site.register(Notice, NoticeAdmin)