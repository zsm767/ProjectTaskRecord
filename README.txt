2019-05-24
Update:
+File upload re-adjusted in order to function properly with FK values in the employee and task code tables
	-Next would be adding in test values and checking for functionality with footage, budget, 
	 and phase
		+Keep in mind, footage & budget might need to be in a separate table for 
		 accumulation reasons, but phase is already a valid col in the task code table

+The Employee and Task Information pages are now properly displaying the values/lists associated with the correct jobs (after like, two days of trying to figure it out) / job foreign key IDs

+Next update for the coming week is to tweak the frontend appearance; things have gotten a bit out of hand with the buttons changing shape, and the positioning is all over the place.
	-Possibly rework the CSS file, need to consider moving to separate files based off of the
	 div names. (look into this)

------------------------------------------------------------------------------------------------
2019-05-15
Update:

+CRUD properties for the Job objects/tables is working:
	-Individual pages for update, deletion, creation, and list view
		+Next steps would include moving the update/delete buttons to link with individual 
		 jobs listed on the view page (COMPLETED 5/15)

+After this, will need to work on the model settings getting the PKs/FKs for each model hooked up
	-Think about the relations needed between the tables

+After *that*, need to work on re-organizing the page layout to display things properly
2019-04-15
So far:

+PostgreSQL connectivity setup
	timbuk2 for tasker user
+JobImport application for the importing of the .csv files
	-I guess for now, create necessary tables / models in this for the project as a whole
	-Make sure to migrate once created
	-Continue through tutorial for views, etc.

------------------------------------------------------------------------------------------------
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

------------------------------------------------------------------------------------------------
2019-04-18
So far:

+Basic connectivity works w/ pages, just need to populate the current DB tables
	-Possibly manually update with test information
	-Look into file-reading for this, just for init information
	-Where's the code for this going to live? 
		+Possible location -> /.../ProjectTaskRecorder/ref or something like that
