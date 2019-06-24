# forms.py, for working on the upload/download functionality 
from django import forms 
from .models import *

class FileForm( forms.ModelForm ):
	class Meta:
		model = File
		fields= ["name", "filepath"]
		
		
class JobForm( forms.ModelForm ):
	job_name = forms.CharField( label='Job name', max_length=25 )
	start_date = forms.DateTimeField( label='Start date', widget=forms.SelectDateWidget(), initial=timezone.now() )
	prefix = 'job'
	#testing something out...
	#employee_name = forms.MultipleChoiceField( label='Employee name', choices=Employee.objects.all(), widget=forms.SelectMultiple() )
	
	class Meta:
		model = Jobs
		fields = ["job_id", "job_name", "start_date",]
		
	
class TaskForm( forms.ModelForm ):
	code_id = forms.ModelChoiceField( label='Task Code Description', empty_label="Select a Task", queryset=TaskCodes.objects.all() )
	week_of = forms.DateField( label='Week of', widget=forms.SelectDateWidget(), initial=timezone.now(), required=False)
	actual_budget = forms.DecimalField( label='Actual Budget', min_value=00.00, max_digits=19, decimal_places=2 )
	prefix = 'task'
	
	"""some work needs to be done here to update the list of available task codes to edit...
	def __init__(self, *args, **kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['code_id'].queryset = TaskCodes.objects.all()"""	
		
	
	""" memo to self: if this still isn't working, be sure to move the post func back to the view.""" 	
	
	class Meta:
		model = TaskCodes
		fields = ["code_id","actual_budget",]
		exclude = ["code_desc", "phase", "job", "budget", "footage", "actual_footage", "acc_footage", "acc_budget",]
		