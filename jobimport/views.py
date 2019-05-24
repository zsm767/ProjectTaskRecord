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
	#print( form.is_valid() )
	#print( form.is_bound )
	context = { 'filepath': filepath, 
				'form': form,
				'filename': filename,
			  }
	if request.method == 'POST':

		dataset = tablib.Dataset('')
		new_file = request.FILES['myfile']
		# checking for the file name, to create the appropriate resource object
		if 'employee' in new_file.name:
			dataset.headers = ('Employee', 'Name', 'job')
			employee_resource = EmployeeResource()
			
			imported_data = dataset.load( new_file.read() )
			# testing the imported data before actually uploading it
			result = employee_resource.import_data( dataset, dry_run=True, raise_errors=True )
			context.update( {'result': result.has_errors()} )
			
			if not result.has_errors():
				employee_resource.import_data( dataset, dry_run=False )
				return render( request, 'jobimport/success.html' )
				
		if 'codes' in new_file.name:
			dataset.headers = ('Task Code', 'Task Description', 'job' )
			code_resource = CodeResource()
			
			imported_data = dataset.load( new_file.read() )
			# testing the imported data before actually uploading it
			result = code_resource.import_data( dataset, dry_run=True, raise_errors=True )
			context.update( {'result': result.has_errors()} )
			
			if not result.has_errors():
				code_resource.import_data( dataset, dry_run=False )
				return render( request, 'jobimport/success.html' )

	return render( request, 'jobimport/file.html', context )
	

class IndexView( generic.ListView ):
	template_name = 'jobimport/index.html'
	context_object_name = 'latest_job_list'
	
	def get_queryset(self):
		#return the last X published jobs?
		return Jobs.objects.order_by( '-last_updated' )[:5]
	
	
# look into the difference between DetailView and ListView. Using ListView doesn't cause iteration errors 
# for reference, look in the difference between code on the employee_info.html and the jobdetails.html files.
""" Job-related views """
class JobDetailsView( generic.CreateView ): 
	model = Jobs
	template_name = 'jobimport/jobdetails.html'
	context_object_name = 'job_list'
	form_class = JobForm
	success_url = reverse_lazy( 'JobImport:success' )

	
class JobUpdateView( generic.UpdateView ): 
	model = Jobs
	fields = ('job_name', 'start_date',)
	template_name = 'jobimport/job_update.html'
	context_object_name = 'job_list'
	success_url = reverse_lazy( 'JobImport:success' )
	
	#testing something out
	def get_object(self, queryset=None):
		"""
			to-do: retrieve the most recent PK/ID from the job page.
			currently hardcoded to the most recent job, play around with it, possibly link this functionality to part of the 
			jobview page, to make it easier?
		"""
		obj = Jobs.objects.get(job_id=self.kwargs['job_id'])
		return obj


class JobDeleteView( generic.DeleteView ): 
	model = Jobs
	template_name = 'jobimport/job_delete.html'
	context_object_name = 'job_list'
	success_url = reverse_lazy( 'JobImport:success' )
	
	def get_object(self, queryset=None):
		"""
			to-do: retrieve the most recent PK/ID from the job page.
			currently hardcoded to the most recent job, play around with it, possibly link this functionality to part of the 
			jobview page, to make it easier?
		"""
		obj = Jobs.objects.get(job_id=self.kwargs['job_id'])
		return obj


class JobView( generic.ListView ): 
	model = Jobs
	template_name = 'jobimport/job_view.html'
	context_object_name = 'job_list'
	
	def get_queryset(self):
		return Jobs.objects.order_by( '-job_name' )
	
""" END: Job-related views """
	
class EmployeeInfoView( generic.ListView ):
	model = Employee
	template_name = 'jobimport/employee_info.html'
	context_object_name = 'employee'
	
	def get_queryset(self):
		return Employee.objects.all().filter(job__job_id=self.kwargs['pk'])
	
	
class TaskInfoView( generic.ListView ):
	model = TaskCodes
	template_name = 'jobimport/task_info.html'
	context_object_name = 'task'
	
	"""
	def get_context_data(self, **kwargs):
		test = TaskCodes.objects.get(job__job_id=2)
		# need to do something else here, kwargs is empty for whatever reason
	"""
	
	def get_queryset(self):
		return TaskCodes.objects.all().filter(job__job_id=self.kwargs['pk'])


class SuccessView( generic.ListView ):
	template_name = 'jobimport/success.html'
	
	def get_queryset(self):
		return 
	