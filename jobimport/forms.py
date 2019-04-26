# forms.py, for working on the upload/download functionality 
from django import forms 
from .models import *

class UploadFileForm( forms.Form ):
	title = forms.CharField( max_length = 25 )
	file = forms.FileField()
	
