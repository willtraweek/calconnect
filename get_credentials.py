#!/usr/bin/env python3

"Get OAuth credentials."

from oauth2client import client, tools

from credentials import creds, scopes, store

#testing from scheduler.py (needed from line 27 of the code)
from apiclient.discovery import build
import json
from datetime import datetime, time, timedelta
#import pendulum
from apiclient.discovery import build
from httplib2 import Http
from credentials import creds


if __name__ == '__main__':

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        tools.run_flow(flow, store)
    else:
        print('Already have credentials.')
#print (creds)
service = build("calendar", "v3", http=creds.authorize(Http()))
print(service)