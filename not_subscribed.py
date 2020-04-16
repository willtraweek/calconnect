import json                 # reading in json file
# import pprint
# pp = pprint.PrettyPrinter() # pretty printing json data

from httplib2 import Http             # connect
from apiclient.discovery import build # to
from credentials import creds         # api

import pendulum                 # datetime + timezone
from datetime import timedelta  # add time


def get_invitees_emails(jsonFileName):
    data     = json.load(open('./' + jsonFileName)) # from json file
    return data['invitees']                         # extract invitee emails


def dateTime(_days=0, _hours=0):                    # get datetime with delay of days or hours
    t = (pendulum.now() + timedelta(days=_days, hours=_hours)).strftime('%Y-%m-%dT%H:%M:00%z')
    t = t[:22] + ':' + t[22:]
    return t


def get_schedule_for_next_30_days(invitees, api):
    next30Days = { 'timeMin': dateTime(),
                   'timeMax': dateTime(30), 
                   'items': [{'id': invitee} for invitee in invitees] }
    return api.freebusy().query(body=next30Days).execute()['calendars'] 


def get_invitees_with_empty_calendar(invitees, next30DaysSchedule):
    invitees_with_empty_cal = []
    for invitee in invitees:                             # get invitees with empty
        busy_times = next30DaysSchedule[invitee]['busy'] # schedule for the next 30 days
        if not busy_times: invitees_with_empty_cal.append(invitee)
    return invitees_with_empty_cal


def schedule_dummy_event(invitees_with_empty_cal, api):
    dummyEvent = {                                  # create a dummy event
        'summary': 'dummy',                         # that takes place
        'start'  : {'dateTime': dateTime(0,1)},     # 1 hour from now
        'end'    : {'dateTime': dateTime(0,2)},     # for 1 hour
        'attendees': invitees_with_empty_cal
    }
    api.events().insert(calendarId='primary', sendNotifications=False, body=dummyEvent).execute()


def get_schedule_for_next_24_hours(invitees_with_empty_cal, api):
    next24Hours = { 'timeMin': dateTime(), 
                    'timeMax': dateTime(1),
                    'items': [{'id': invitee} for invitee in invitees_with_empty_cal] }
    return api.freebusy().query(body=next24Hours).execute()['calendars']

def get_invitees_not_subscribed(invitees_with_empty_cal, next24HourSchedule):
    invitees_not_subscribed = []

    for invitee in invitees_with_empty_cal:
        busy_times = next24HourSchedule[invitee]['busy'] # if an invitee's schedule is still empty, 
        if not busy_times: invitees_not_subscribed.append(invitee) # this invitee is not subscribed
    
    return invitees_not_subscribed


def delete_dummy_event(api):
    events = api.events().list(calendarId='primary').execute()['items'] # get all events

    dummyIds = []                                   # gather dummy event ids
    for event in events: 
        if event['summary'] == 'dummy':
            dummyIds.append(event['id'])

    for dummyId in dummyIds:                        # delete events with those ids
        api.events().delete(calendarId='primary', eventId=dummyId, sendNotifications=False).execute()


# ****************  LE, THIS IS THE FUNCTION YOU WANT TO EXPORT!!! **************** 
def get_not_subscribed_users(jsonFileName):
    api                     = build('calendar', 'v3', http=creds.authorize(Http())) # google cal api
    invitees                = get_invitees_emails(jsonFileName)
    next30DaysSchedule      = get_schedule_for_next_30_days(invitees, api)
    invitees_with_empty_cal = get_invitees_with_empty_calendar(invitees, next30DaysSchedule)
    schedule_dummy_event(invitees_with_empty_cal, api) # dummy event occurs an hr from now
    next24HourSchedule      = get_schedule_for_next_24_hours(invitees_with_empty_cal, api)
    invitees_not_subscribed = get_invitees_not_subscribed(invitees_with_empty_cal, next24HourSchedule)
    delete_dummy_event(api)
    return invitees_not_subscribed

#def main():
#    get_not_subscribed_users('scheduledMeeting.json')

#if __name__ == '__main__': 
#    main()