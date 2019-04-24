import datetime

from django.db import models
from django.utils import timezone
#from jobimport.models import [ModelNames] || import jobimport.models
# Create your models here.
class Employee( models.Model ):
	#class vars, etc.; relates directly to columns
	employee_name = models.CharField(max_length = 200)
	employee_id = models.CharField(max_length = 8)
	#unique id?
	
	#default __str__ func for printing
	def __str__(self):
		return self.employee_name
		

class TaskCodes( models.Model ):
	code_id = models.PositiveSmallIntegerField(default = 0)
	code_desc = models.CharField(max_length = 50)
	phase = models.CharField(default = "00", max_length = 2)
	
	def __str__(self):
		return self.code_desc
	#more class-unique funcs


class Jobs( models.Model ):
	job_id = models.PositiveSmallIntegerField(default = 0)
	job_name = models.CharField(max_length = 50)
	start_date = models.DateTimeField()
	last_updated = models.DateTimeField( 'Date Updated' )
	
	def __str__(self):
		return self.job_name