# forms.py, for working on the upload/download functionality 
from django import forms 
from .models import *

class FileForm( forms.ModelForm ):
	#testing something out...
	jobs = Jobs.objects.all()
	job_id = forms.ModelChoiceField( queryset=jobs, label='Choose a job to link this to:' )
	class Meta:
		model = File
		fields= ["name", "filepath"]
		
class JobForm( forms.ModelForm ):
	job_name = forms.CharField( label='Job name', max_length=25 )
	start_date = forms.DateTimeField( label='Start date', widget=forms.SelectDateWidget() )
	class Meta:
		model = Jobs
		fields = ["job_id", "job_name", "start_date"]