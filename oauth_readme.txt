Copy Contents to a directory:
	INCLUDE THE FILE: client_secret.json
	** I can provide you with the files or enable google calendar API and get it yourself 
	** Don't put your secret credentials on github lol
Install:
	conda install -c auto auth.credential
	conda install -c conda-forge oauth2client
Run the get credentials file:
	python get_credentials.py

now the credentials can be accessed in any file:
import statment: from credentials import creds
use the variable: creds
USE THE SERVICE VARIABLE AFTER DOING THIS
service = build("calendar", "v3", http=creds.authorize(Http()))

SEE THE FILE scheudler.py for any further questions 

	




	