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
	
	#testing something out...
	#employee_name = forms.MultipleChoiceField( label='Employee name', choices=Employee.objects.all(), widget=forms.SelectMultiple() )
	
	class Meta:
		model = Jobs
		fields = ["job_id", "job_name", "start_date",]
		
	
class TaskForm( forms.ModelForm ):
	code_id = forms.ModelChoiceField( label='Task Code Description', empty_label="Select a Task", queryset=TaskCodes.objects.all(), to_field_name="code_id" )
	week_of = forms.DateField( label='Week of', widget=forms.SelectDateWidget(), initial=timezone.now(), required=False)
	actual_budget = forms.DecimalField( label='Actual Budget', min_value=00.00, max_digits=19, decimal_places=2 )
	
	
	class Meta:
		model = TaskCodes
		fields = ["code_id","actual_budget",]
		

	def __init__(self, *args, **kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)
		# NOTE: hardcoding it from here works, for whatever reason. Be sure to check the **kwargs value, and how to get this 
		#working properly
		self.fields['code_id'].queryset = TaskCodes.objects.filter(job__job_id=2)
	"""
	
	
	def save(self, *args, **kwargs):
		tf = super(TaskForm, self).save(commit=False)
		#more to do here?
		if True:
			tf.save(self, *args, **kwargs)
		return tf
	
		TO-DO: more work here, need to force the update. Changing the above to commit=True still doesn't save the change.
		data = self.cleaned_data
		tc.objects.update() 
		Note: current issue invoplved the save() method above; with a type error. This is (possibly) due to the update_fields arg 
		being connected to the MODEL'S save() method, as opposed to the FORM'S. 
		
			Try:
				obj = form.save(commit=False) to get model instance, then call obj.save(update_fields=...)
	"""