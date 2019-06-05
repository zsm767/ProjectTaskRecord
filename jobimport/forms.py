# forms.py, for working on the upload/download functionality 
from django import forms 
from .models import *

class FileForm( forms.ModelForm ):
	class Meta:
		model = File
		fields= ["name", "filepath"]
		
		
class JobForm( forms.ModelForm ):
	job_name = forms.CharField( label='Job name', max_length=25 )
	start_date = forms.DateTimeField( label='Start date', widget=forms.SelectDateWidget() )
	#testing something out...
	#employee_name = forms.MultipleChoiceField( label='Employee name', choices=Employee.objects.all(), widget=forms.SelectMultiple() )
	
	class Meta:
		model = Jobs
		fields = ["job_id", "job_name", "start_date",]
		
	"""
	def __init__(self, *args, **kwargs):
		self.actual_budget = kwargs.pop('actual_budget')
		self.actual_footage = kwargs.pop('actual_footage')
		super(JobForm, self).__init__(*args, **kwargs)
	"""
	
class TaskForm( forms.ModelForm ):
	week_of = forms.DateField( label='Week of', widget=forms.SelectDateWidget(), initial=timezone.now() )
	# should be changed to a dropdown, to select proper info, etc. 
	code_id = forms.CharField( label='Task Code ID', max_length=4 )
	actual_budget = forms.DecimalField( label='Actual Budget', min_value=00.00, max_digits=19, decimal_places=2 )
	actual_footage = forms.IntegerField( label='Actual Footage', min_value=0 )
	
	class Meta:
		model = TaskCodes
		fields = ["code_id","actual_budget", "actual_footage",]