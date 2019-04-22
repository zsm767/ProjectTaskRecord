from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import UploadFileForm

# Create your views here.
#def pagename( request, PK )

#index probably for a base page or something, primarily for testing things out
#think: what are the primary pages for this site going to have?
def upload_file( request ):
	if( request.method == 'POST' ):
		form = UploadFileForm( request.POST, request.FILES )
		if( form.is_valid() ):
			instance = ModelWithFileField( file_field=request.FILES['file'] )
			instance.save()
			return HttpResponseRedirect( '/success/url' ) #need to change this later
	else:
		form = UploadFileForm()
	return render( request, 'upload.html', {'form': form} ) #also need to change this 
	

class IndexView( generic.ListView ):
	template_name = 'jobimport/index.html'
	context_object_name = 'latest_job_list'
	
	def get_queryset(self):
		#return the last X published jobs?
		return Jobs.objects.order_by( '-pub_date' )[:5]
	
	

class JobDetailsView( generic.DetailView ):
	model = Jobs
	template_name = 'jobimport/jobdetails.html'
	
	
class EmployeeInfoView( generic.DetailView ):
	model = Employee
	template_name = 'jobimport/employee_info.html'
	
	
class TaskInfoView( generic.DetailView ):
	model = TaskCodes 
	template_name = 'jobimport/task_info.html'
