# calconnect

## Deployment:
Automated CI/CD pipelines have been set up using Amazon CodeCommit, CodePipeline, and Elastic Beanstalk.

A push to master will automatically update the calconnect-prod server.  These changes will be reflected at this url: [http://calconnect.us-east-1.elasticbeanstalk.com/](http://calconnect.us-east-1.elasticbeanstalk.com/)

A push to dev will automatically update the calconnect-dev server.  These changes will be reflected at this url: [http://calconnect-dev.us-east-1.elasticbeanstalk.com/](http://calconnect-dev.us-east-1.elasticbeanstalk.com/)git checkuo
=======
# scheduler

Code for scheduling multiple meetings on Google calendar, finding a
schedule for all the meetings taking into account everyone's current
calendar and the need to not schedule conflicting meetings.

Once you've got a `client_secrets.json` from the Google API console you can run:

```
./get_credentials
```

to go through the OAuth dance via your web browser to let the app access your
calendar. Instructions for obtaining a `client_secrets.json` are at
https://support.google.com/googleapi/answer/6158849.

Put your `client_secrets.json` and `credentials.json` in a folder one directory back 
(outside the workspace) in a folder named `cred`. This will prevent you from putting 
these credentials into github if you push.

Then run:

```
./schedule example_meetings.txt
```

to see when it would schedule the meetings where `example_meetings.txt` is a
file containing one meeting per line in the format:

```
[30] A meeting name: harry@example.com, sally@example.com
[60] Another meeting name: sally@example.com, linda@example.com, bobby@example.com
```

The number in brackets is the duration in minutes of the meeting, the
text up to the colon is the title of the meeting, and everything after
the colon is a comma-delimited list of attendees.

Run:

```
./schedule example_meetings.txt --calendar your_email@gmail.com
```

to actually schedule them on people's calendars.

------------------------------------------------------------

UPDATES TO CODE:
Now to run the entire program call the function process_data(data, credentials) 
    This function will call a subsystem process to run the entire scheduling process
    
    VARIABLES
        data {
            'host': '''host email'''
            'emails' : []
            'start' : datetime
            'duration' : time in minutes
            'description' : '''short description'''
        }
        
        credentials
            json file containing oauth information
