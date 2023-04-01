Write a Python program that uploads any code paste file I have to S3.
Here are some additional specifications:

* Generate a link that a user can use to view the file. 
* The bucket policy should allow any user with the link to view the file.
* The pre-signed URL link from S3 should not expire.
* Use a base bucket name of "code-pastes". Check if the bucket exists, and if it does not, create it. 
* Set the bucket policy to delete objects older than 1 year. 
* Add logging from the logger library and note what actions it is taking.
* Th logging setup should print all INFO messages and also log to a file called "/tmp/paste-to-s3.log". Print this log location at the end of the program.
* The program should include argparse arguments for the file to upload as the only argument.
* Append ISO 8601 date to the uploaded file name so it stays unique if the same file is uploaded again.
* Put the bucket actions in it's own method and the upload actions in it's own  method
* Use a separate method for creating the boto3 client setup
* Put the logging setup in it's own method
* Print the pre-signed url at the end of the program
* Add exception handling for all methods
* Document all methods with sphinx style docstrings. The docstring should have the description, parameters, and returns
