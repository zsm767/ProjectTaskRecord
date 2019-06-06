import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now

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
	start_date = models.DateTimeField(default=timezone.now)
	last_updated = models.DateTimeField( 'Date Updated', auto_now=True )
	# document = models.ForeignKey( Document, on_delete=models.CASCADE )
	# testing out some things to correct the functionality
	# employee = models.ForeignKey( Employee, on_delete=models.CASCADE, null=False, related_name='job_emps')
	
	class Meta:
		ordering = ['job_id']
	
	def __str__(self):
		return self.job_name


class Employee( models.Model ):
	#class vars, etc.; relates directly to columns
	employee_name = models.CharField(max_length = 200)
	employee_id = models.CharField(max_length = 8, unique=True)
	job = models.ForeignKey( Jobs, on_delete=models.CASCADE, null=False, related_name='employee' )
	"""
	for future usage: job = models.ManyToManyField( Jobs )
	"""
	
	class Meta:
		ordering = ['employee_id']
	
	#default __str__ func for printing
	def __str__(self):
		return self.employee_name
		

class TaskCodes( models.Model ):
	code_id = models.PositiveSmallIntegerField(default = 0)
	code_desc = models.CharField(max_length = 50)
	phase = models.CharField(default = "00", max_length = 2)
	job = models.ForeignKey( Jobs, on_delete=models.CASCADE, null=False, related_name='tasks' )
	
	budget = models.DecimalField(default=00.00, max_digits=19, decimal_places=2)
	actual_budget = models.DecimalField(default=00.00, max_digits=19, decimal_places=2)
	
	footage = models.PositiveSmallIntegerField( default = 0 )
	actual_footage = models.PositiveSmallIntegerField( default = 0 )
	
	"""
	for future usage: job = models.ManyToManyField( Jobs )
	"""
	
	class Meta:
		ordering = ['code_id']
	
	def __str__(self):
		return self.code_desc
	
	#more class-unique funcs

""" 
	TO-DO: These don't need to be individual models, they can be moved to an existing model
	Considering that the data is stored in the task code file, and that the budget/footage has an associated task to it,
	it would make the most sense to put it there
	
	consider adding in the following:
	total_budget = models.DecimalField(default=00.00, max_digits=19, decimal_places=2)
	actual_budget = ...
	percentage_budget = ...
	
	total_footage = models.PositiveSmallIntegerField( default = 0 )
	actual_footage = ...
	percentage_footage = ...
"""

class Accumulator( models.Model ):
	acc_footage = models.PositiveSmallIntegerField( default = 0 )
	acc_budget = models.DecimalField(default=00.00, max_digits=19, decimal_places=2)
	task_codes = models.ForeignKey( TaskCodes, on_delete=models.CASCADE, null=False, related_name='accumlator' )
	
	class Meta:
		ordering = ['acc_footage']
	
	def __str__(self):
		return self.accumulated_footage
		
	"""
	def accumulate(self):
	# testing function for the accumulator for both the footage and budget
	
	"""