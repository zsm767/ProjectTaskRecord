from django.contrib import admin
from import_export import resources
from .models import *

# Register your models here.

class EmployeeResource( resources.ModelResource ):
	class Meta:
		model = Employee
		skip_unchanged = True		# sets it so that if no changes are detected on uploads, it skips over
		report_skipped = False		# controls whether skipped records appear in the import "Result" object
		
class JobResource( resources.ModelResource ):
	class Meta:
		model = Jobs
		skip_unchanged = True
		report_skipped = True

class CodeResource( resources.ModelResource ):
	class Meta:
		model = TaskCodes
		skip_unchanged = True
		report_skipped = True