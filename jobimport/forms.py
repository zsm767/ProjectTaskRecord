# forms.py, for working on the upload/download functionality 
from django import forms 

class UploadFileForm( forms.Form ):
	title = forms.CharField( max_length = 25 )
	file = forms.FileField()
	
