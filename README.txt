2019-04-15
So far:

+PostgreSQL connectivity setup
	timbuk2 for tasker user
+JobImport application for the importing of the .csv files
	-I guess for now, create necessary tables / models in this for the project as a whole
	-Make sure to migrate once created
	-Continue through tutorial for views, etc.

2019-04-18
So far:

+Basic connectivity works w/ pages, just need to populate the current DB tables
	-Possibly manually update with test information
	-Look into file-reading for this, just for init information
	-Where's the code for this going to live? 
		+Possible location -> /.../ProjectTaskRecorder/ref or something like that

2019-05-8
Update:

+File upload is working now; just note:
	-Will need to change columns in the following files:
		+Employee -> employee_id
		+Name -> employee_name
		+Task Code -> code_id
		+Task Description -> code_description
	-Creating "filename_test.xslx" versions with these updates, might make a template file

+Next: clean up the pages, move things around for a better presentation.