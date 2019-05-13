import os
import tablib
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.conf import settings 
from django.views.decorators.http import require_POST
from tablib import Dataset
from .resource import *


# Create your views here.
#def pagename( request, PK )

#index probably for a base page or something, primarily for testing things out
#think: what are the primary pages for this site going to have?
def showfile( request ):
	# note: will need to change some of the names around, due to this only working with one upload model/type
	lastfile = File.objects.last()
	filepath = lastfile.filepath
	filename = lastfile.name
	
	form = FileForm( request.POST or None, request.FILES or None )
	if form.is_valid():
		form.save()
		
	context = { 'filepath': filepath, 
				'form': form,
				'filename': filename,
			  }
	
	if request.method == 'POST':
		dataset = tablib.Dataset('')
		new_file = request.FILES['myfile']
		# checking for the file name, to create the appropriate resource object
		if 'employee' in new_file.name:
			dataset.headers = ('Employee', 'Name')
			employee_resource = EmployeeResource()
			
			imported_data = dataset.load( new_file.read() )
			# testing the imported data before actually uploading it
			result = employee_resource.import_data( dataset, dry_run=True, raise_errors=True )
			context.update( {'result': result.has_errors()} )
			
			if not result.has_errors():
				employee_resource.import_data( dataset, dry_run=False )
				return render( request, 'jobimport/success.html' )
				
		if 'codes' in new_file.name:
			dataset.headers = ('Task Code', 'Task Description')
			code_resource = CodeResource()
			
			imported_data = dataset.load( new_file.read() )
			# testing the imported data before actually uploading it
			result = code_resource.import_data( dataset, dry_run=True, raise_errors=True )
			context.update( {'result': result.has_errors()} )
			
			if not result.has_errors():
				code_resource.import_data( dataset, dry_run=False )
				return render( request, 'jobimport/success.html' )

	return render( request, 'jobimport/file.html', context )

	

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
	
	
# look into the difference between DetailView and ListView. Using ListView doesn't cause iteration errors 
# for reference, look in the difference between code on the employee_info.html and the jobdetails.html files.
class JobDetailsView( generic.CreateView ): 
	model = Jobs
	template_name = 'jobimport/jobdetails.html'
	context_object_name = 'job_list'
	form_class = JobForm
	success_url = reverse_lazy( 'JobImport:success' )
	
	def get_queryset(self):
		return Jobs.objects.order_by( '-job_name' )
	
	""" to-do: add in code for processing the data from the form?
		something like this:
	def 
	"""
	
class EmployeeInfoView( generic.ListView ):
	model = Employee
	template_name = 'jobimport/employee_info.html'
	context_object_name = 'employee'
	
	def get_queryset(self):
		return Employee.objects.order_by( '-employee_id' )
	
	
class TaskInfoView( generic.ListView ):
	model = TaskCodes 
	template_name = 'jobimport/task_info.html'
	context_object_name = 'task'
	
	def get_queryset(self):
		return TaskCodes.objects.order_by( '-code_id' )


class SuccessView( generic.ListView ):
	template_name = 'jobimport/success.html'