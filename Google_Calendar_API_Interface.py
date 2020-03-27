import pickle   # to store credentials
import os.path  # to find picke file
from googleapiclient.discovery import build             # to build api obj
from google_auth_oauthlib.flow import InstalledAppFlow  # to create authentication flow
from google.auth.transport.requests import Request      # to make http requests to google api server
import pprint  # pretty print to make printed objects look easier to read
pp = pprint.PrettyPrinter(indent=1) # configure pretty print

# STEP 1: get credentials to access user's google calendar ----------------------------- 

creds = None # init creds

# case 1: valid token exists
if os.path.exists('token.pickle'): 
    with open('token.pickle', 'rb') as token: 
        creds = pickle.load(token)

# case 2: token has expired
elif creds and creds.expired and creds.refresh_token: 
    creds.refresh(Request())

# case 3: we don't have any token at all
else:
    # enable read & write to user's google calendar
    SCOPE = ['https://www.googleapis.com/auth/calendar'] 
    
    # create authorization flow between user's google account and this app
    flow = InstalledAppFlow.from_client_secrets_file(
        "./google_credentials/client_id.json",
        scopes = SCOPE
    )# end flow

    # http://localhost:8080/ redirects user to google login page
    creds = flow.run_local_server(host='localhost', port=8080)

    # save creds for future use
    with open('token.pickle', 'wb') as token: 
        pickle.dump(creds, token)

# STEP 2: using creds... ----------------------------------------------------------------- 

# 1. access user's calendar
service = build('calendar', 'v3', credentials = creds) # begin using google's calendar api service

# 2. filter information to extract user's upcoming events
page_token = None
while True:
  events = service.events().list(calendarId='primary', pageToken=page_token).execute()
  for event in events['items']:
    #pp.pprint(event)                           # prints every detail of event 
    pp.pprint(event['summary'])                 # event name
    pp.pprint(event['start']['dateTime'])       # event start time
    pp.pprint(event['end']['dateTime'])         # event end time
  page_token = events.get('nextPageToken')
  if not page_token:
    break

# 3. calculate times of availablity

'''
This is where I leave you to do your magic. Have fun Mitch! 

Use this source to explore the google calendar API & get what you want:

https://developers.google.com/calendar/v3/reference/events/list
'''