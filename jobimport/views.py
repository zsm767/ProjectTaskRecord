import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import FileForm
from django.shortcuts import redirect
from django.conf import settings 
from django.views.decorators.http import require_POST

# Create your views here.
#def pagename( request, PK )

#index probably for a base page or something, primarily for testing things out
#think: what are the primary pages for this site going to have?
def showfile( request ):
	lastfile = File
	filepath = lastfile.filepath
	filename = lastfile.name
	
	form = FileForm( request.POST or None, request.FILES or None )
	if form.is_valid():
		form.save()
		
	context = { 'filepath': filepath, 
				'form': form,
				'filename': filename
			  }
	return render( request, 'jobimport/file.html', context)


@require_POST
def file_upload( request ):
	save_path = os.path.join( settings.MEDIA_ROOT, 'uploads', request.FILES['file'] )
	path = default.storage.save( save_path, request.FILES['file'] )
	return default_storage.path( path )
	

class IndexView( generic.ListView ):
	template_name = 'jobimport/index.html'
	context_object_name = 'latest_job_list'
	
	def get_queryset(self):
		#return the last X published jobs?
		return Jobs.objects.order_by( '-last_updated' )[:5]
	
	

class JobDetailsView( generic.DetailView ):
	model = Jobs
	template_name = 'jobimport/jobdetails.html'
	context = 'latest_job_details'
	
	def get_queryset(self):
		return Jobs.objects.order_by( '-start_date' )
	
	
class EmployeeInfoView( generic.DetailView ):
	model = Employee
	template_name = 'jobimport/employee_info.html'
	
	
class TaskInfoView( generic.DetailView ):
	model = TaskCodes 
	template_name = 'jobimport/task_info.html'
