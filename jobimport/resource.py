# resource.py in the jobimport folder
from import_export import resources
from .models import *

# follows naming convention of "class [ModelName]Resource( resources.ModelResource [,optional args...] ):"
# starting w/ Employee, since that's separated into its own table / not reliant on multiple models
class EmployeeResource( resources.ModelResource ):
	class Meta:
		model = Employee
		skip_unchanged = True		# sets it so that if no changes are detected on uploads, it skips over
		report_skipped = False		# controls whether skipped records appear in the import "Result" object