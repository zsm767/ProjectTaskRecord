import os
import tablib
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Sum
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.conf import settings 
from django.views.decorators.http import require_POST
from tablib import Dataset
from .resource import *


# Create your views here.
# def pagename( request, PK )

# index probably for a base page or something, primarily for testing things out
# think: what are the primary pages for this site going to have?
""" testing something out for the exporting of data (trying to have it be on the same page as file upload...)"""
def export( request ):
	# default testing with the Task Code file, would need some kind of selection for data set
	code_resource = CodeResource()
	dataset = code_resource.export()
	response = HttpResponse( dataset.csv, content_type='text/csv' )
	response['Content-Disposition'] = 'attachment; filename="task_codes.csv"'
	return response

""" temp function specifically for the employee export functionality, will need to be condensed into once func/class later"""	
def employee_export( request ):
	employee_resource = EmployeeResource()
	dataset = employee_resource.export()
	response = HttpResponse( dataset.csv, content_type='text/csv' )
	response['Content-Disposition'] = 'attachment; filename="employees.csv"'
	return response


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
				
		# note: change 'footage' to 'units' later
		if 'codes' in new_file.name:
			dataset.headers = ('Task Code', 'Task Description', 'job', 'footage', 'budget', )
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
	
	

""" Job-related views """
class JobDetailsView( generic.CreateView ): 
	model = Jobs
	template_name = 'jobimport/jobdetails.html'
	context_object_name = 'job_list'
	form_class = JobForm
	success_url = 'jobview'

	
class JobUpdateView( generic.UpdateView ): 
	model = Jobs
	#fields = ('job_name', 'start_date',)
	form_class = JobForm
	second_form_class = TaskForm
	template_name = 'jobimport/job_update.html'
	context_object_name = 'job_list'
	success_url = 'jobview'
	
	
	def get_context_data(self, **kwargs):
		context = super(JobUpdateView, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(initial={'job_id': context['Jobs'].job_id})
			
		if 'form2' not in context:
			context['form2'] = self.second_form_class()
			context['form2'].fields['code_desc'].queryset = TaskCodes.objects.filter(job__job_id=self.kwargs['job_id'])
		return context
		
	
	def get_object(self, queryset=None):
		obj = Jobs.objects.get(job_id=self.kwargs['job_id'])
		return obj


	def form_valid(self, form):
		""" overriding this to save the object if the form is valid. """
		self.object = form.save()
		return super(JobUpdateView, self).form_valid(form)
		

	def form_invalid(self, **kwargs):
		return self.render_to_response(self.get_context_data(**kwargs))
		
	
	def post(self, request, *args, **kwargs):
		# getting the user instance
		self.object = self.get_object()
		# figuring out which form is being submitted, using the form's submit button
		if 'form' in request.POST:
			form_class = self.get_form_class()
			form_name = 'form'
		else:
			form_class = self.second_form_class
			form_name = 'form2'
		# getting the form
		form = self.get_form(form_class)
		# validating the form
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(**{form_name: form})
			

class JobDeleteView( generic.DeleteView ): 
	model = Jobs
	template_name = 'jobimport/job_delete.html'
	context_object_name = 'job_list'
	success_url = 'jobview'
	
	def get_object(self, queryset=None):
		obj = Jobs.objects.get(job_id=self.kwargs['job_id'])
		return obj


class JobView( generic.ListView ): 
	model = Jobs
	template_name = 'jobimport/job_view.html'
	context_object_name = 'job_list'
	
	def get_queryset(self):
		return Jobs.objects.order_by( 'job_id' )
	
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
	
	
class AccumulatorView( generic.ListView ):
	model = TaskCodes
	template_name = 'jobimport/accumulator.html'
	context_object_name = 'accumulator'
	footage_sum = TaskCodes.objects.all().aggregate(sum = Sum('acc_footage'))
	budget_sum = TaskCodes.objects.all().aggregate(sum = Sum('acc_budget'))
	""" 
	alternatively:
	model = TaskCodes
	template_name and context_object_name remain the same
	footage_sum = Accumulator.objects.all().aggregate(sum = Sum('acc_footage'))
	budget_sum = Accumulator.objects.all().aggregate(sum = Sum('acc_budget'))
	context.update( 'footage_sum': footage_sum, 'budget_sum': budget_sum)
	"""
	#testing this out, might not work 
	def get_context_data(self, **kwargs):
		context = super(AccumulatorView, self).get_context_data(**kwargs)
		context.update({'footage_sum': self.footage_sum, 'budget_sum': self.budget_sum})
		return context
	
	
	def get_queryset(self):
		return TaskCodes.objects.all()