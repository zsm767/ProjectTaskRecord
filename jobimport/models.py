import datetime

from django.db import models
from django.utils import timezone
#from jobimport.models import [ModelNames] || import jobimport.models
# Create your models here.
class File( models.Model ):
	name = models.CharField(max_length = 30)
	filepath = models.FileField(upload_to='files/', null=True, verbose_name="")
	
	def __str__(self):
		return self.name + ": " + str(self.filepath)
	
	
class Jobs( models.Model ):
	job_id = models.PositiveSmallIntegerField(default = 1, unique=True)
	job_name = models.CharField(max_length = 50)
	start_date = models.DateTimeField()
	last_updated = models.DateTimeField( 'Date Updated', auto_now=True )
	#document = models.ForeignKey( Document, on_delete=models.CASCADE )
	
	def __str__(self):
		return self.job_name


class Employee( models.Model ):
	#class vars, etc.; relates directly to columns
	employee_name = models.CharField(max_length = 200)
	employee_id = models.CharField(max_length = 8, unique=True)
	job = models.ForeignKey( Jobs, on_delete=models.CASCADE, null=False, related_name='employee' )
	#unique id?
	
	class Meta:
		ordering = ['employee_id']
	
	#default __str__ func for printing
	def __str__(self):
		return self.employee_name
		

class TaskCodes( models.Model ):
	code_id = models.PositiveSmallIntegerField(default = 0)
	code_desc = models.CharField(max_length = 50)
	phase = models.CharField(default = "00", max_length = 2)
	job = models.ForeignKey( Jobs, on_delete=models.CASCADE, null=False, related_name='task' )
	
	class Meta:
		ordering = ['code_id']
	
	def __str__(self):
		return self.code_desc
	#more class-unique funcs