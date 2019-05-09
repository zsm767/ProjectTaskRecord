# forms.py, for working on the upload/download functionality 
from django import forms 
from .models import *

class FileForm( forms.ModelForm ):
	class Meta:
		model = File
		fields= ["name", "filepath"]
		
class JobForm( forms.ModelForm ):
	class Meta:
		model = Jobs
		fields = ["job_id", "job_name", "start_date", "last_updated"]