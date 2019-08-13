from django.test import TestCase
from .models import *
from .forms import *
from .views import *
# Create your tests here.


""" 
Test cases for the TaskUpdateView, TaskCodes, and TaskForm classes to help with validation testing
"""
def createTaskCode():
	return TaskCodes.objects.create() #need to change up this code


class TaskUpdateViewTests( TestCase ):
	def form_validation( self ):
		