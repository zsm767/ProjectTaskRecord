#JobImport/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'JobImport'
urlpatterns = [
	path( '', views.IndexView.as_view(), name ='index' ),
	#to-do: add in paths once basic views are created 
	#something like path( '<int:job_id>/jobdetails', views.job_details, name='jobdetails' )
	path( '<int:pk>/jobdetails', views.JobDetailsView.as_view() ,name = 'job_details' ),
	path( '<int:pk>/jobview', views.JobView.as_view() ,name = 'job_view' ),
	path( '<int:pk>/jobupdate', views.JobUpdateView.as_view() ,name = 'job_update' ),
	path( '<int:pk>/jobdelete', views.JobDeleteView.as_view() ,name = 'job_delete' ),
	path( '<int:pk>/employee_info', views.EmployeeInfoView.as_view(), name = 'employee_info' ),
	path( '<int:pk>/task_info', views.TaskInfoView.as_view(), name = 'task_info' ),
	path( 'file_upload', views.showfile, name = 'file' ),
	path( 'success', views.SuccessView.as_view(), name = 'success' ),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)