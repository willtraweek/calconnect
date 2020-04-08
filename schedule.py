# schedule
import re
import json
import pendulum
import argparse
from httplib2 import Http
from apiclient.discovery import build
from datetime import datetime, time, timedelta
from credentials import creds

class Interval:
    # represent a time interval as start (inclusive) and end (exlcusive)
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __repr__(self):
        return '{} to {}'.format(self.start.isoformat(), self.end.isoformat())

    def before(self, other):
        return self.end <= other.start

    def after(self, other):
        return self.start >= other.end

    def overlaps(self, other):
        return not (self.before(other) or self.after(other))

    def from_calendar(cal):
        return Interval(pendulum.parse(cal['start']), pendulum.parse(cal['end']))

class Meeting:
    # meeting to be scheduled
    # attendees and slots are filled in by scheduling process
    def __init__(self, summary, minutes, invitees, attendees=None, slots=None):
        self.summary = summary
        self.minutes = minutes
        self.invitees = invitees   # who's on the invite, may includes groups
        self.attendees = attendees # actual people after expanding groups
        self.slots = slots

    def __repr__(self):
        return json.dumps({
            'summary': self.summary,
            'minutes': self.minutes,
            'invitees': list(self.invitees),
            'attendees': list(self.attendees),
            'slots': ['{}'.format(s) for s in self.slots]})

    def scheduled(self):
        return len(self.slots) == 1

    def copy(self):
        return Meeting(
            self.summary, 
            self.minutes, 
            self.invitees, 
            self.attendees, 
            set(self.slots))

def busy(emails, start_day, start_time, end_time, days):
    # map of intervals each person is busy according to their calendar
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    data = (
        service.freebusy()
        .query(
            body = {
                'timeMin': datetime.combine(start_day, start_time).isoformat(),
                'timeMax': datetime.combine(
                    start_day + timedelta(days=days), end_time
                ).isoformat(),
                'items': [{'id': e} for e in emails],
            }
        )
        .execute()
    )
    busy_times = {
        name: [Interval.from_calendar(x) for x in x['busy']]
        for name, x in data['calendars'].items()
    }
    print(busy_times)
    groups = (
        {g: x['calendars'] for g, x in data['groups'].items()}
        if 'groups' in data
        else {}
    )
    return busy_times, groups

def schedule_meeting(meeting, calendar, location=None, description=None):
    # schedule a meeting on the given calendar w/ given location & description
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    print('Meeting slots')
    print(meeting.slots)
    body = {
        'summary': meeting.summary,
        'location': location or '',
        'description': description or '',
        'start': {'dateTime': item(meeting.slots).start.isoformat()},
        'end': {'dateTime': item(meeting.slots).end.isoformat()},
        'attendees': [{'email': e} for e in meeting.invitees if e != calendar],
    }
    return service.events().insert(calendarId=calendar, body=body).execute()

def working_slots(start_day,
                  start_time,
                  end_time,
                  now,
                  days = 1,
                  minutes = 30,
                  increment = 15,
                  daysofweek = {0, 1, 2, 3, 4}):
    # get all slots during working hours in a given time range
    ss = []
    for d in range(days):
        day = start_day + timedelta(days=d)
        if day.weekday() in daysofweek:
            start = datetime.combine(day, start_time)
            end = datetime.combine(day, end_time)
            length = timedelta(minutes=minutes)
            incr = timedelta(minutes=increment)
            s = start
            while (s + length) <= end:
                e = s + length
                if s > now:
                    ss.append(Interval(s, e))
                s += incr
    return ss

def schedules(meetings):
    # generates all possible schedules
    if meetings is None: return None
    elif all(m.scheduled() for m in meetings.values()): yield meetings
    else:
        unscheduled = [m for m in meetings if len(meetings[m].slots) > 1]
        for m in sorted(unscheduled, key=lambda m: len(meetings[m].slots)):
            for s in sorted(meetings[m].slots, key=lambda s: s.start):
                copied = {m: meeting.copy() for m, meeting in meetings.items()}
                yield from schedules(assign(copied, m, s))

def assign(meetings, m, s):
    # assign slot s to meeting m, propagating consequences
    return meetings if eliminate(meetings, m, lambda x: x != s) else None

def eliminate(meetings, m, fn):
    # eliminate slots from meeting m and propagate consequences
    to_eliminate = {s for s in meetings[m].slots if fn(s)}
    if to_eliminate:
        meetings[m].slots -= to_eliminate
        left = len(meetings[m].slots)
        if left == 0: return None
        elif left == 1:
            s = item(meetings[m].slots)
            attendees = meetings[m].attendees
            other_meetings = {
                m for m in meetings if attendees & meetings[m].attendees
            } - {m}
            if not all(
                eliminate(meetings, m2, lambda x: x.overlaps(s))
                for m2 in other_meetings
            ):
                return None
    return meetings

def item(s):
    return next(iter(s))

def schedule(meetings, start_day, start_time, end_time, days, now):
    # find first possible schedule for set of meetings
    emails = set(a for m in meetings.values() for a in m.invitees)
    busy_times, groups = busy(emails, start_day, start_time, end_time, days)
    print(busy_times)
    # first fill in the basic slots for the desired length of meeting
    # and expand the attendees list
    for m, meeting in meetings.items():
        meeting.slots = set(
            working_slots(start_day, start_time, end_time, now, days, meeting.minutes)
        )
        meeting.attendees = expand(meeting.invitees, groups)
    # now that every meeting is set up we can eliminate busy times and
    # potentially take advantage of contstraint propagation
    for m, meeting in meetings.items():
        if not (eliminate_busy(meetings, m, busy_times)):
            return None
    return next(schedules(meetings), None)

def eliminate_busy(meetings, m, busy):
    # eliminate the slots where one of the attendees is busy
    meeting = meetings[m]
    for a in meeting.attendees:
        to_eliminate = busy_slots(sorted(meeting.slots, key=lambda x: x.start), busy[a])
        if not eliminate(meetings, m, lambda x: x in to_eliminate):
            return None
    return meetings

def expand(invitees, groups):
    # expand the invitees (which may include groups) into actual people
    expansion = set()
    for i in invitees: expansion |= set(groups[i]) if i in groups else {i}
    return expansion

def busy_slots(slots, busy):
    # find intervals in slots that overlap busy intervals
    def walk(slots, busy):
        while slots and busy:
            s = slots[0]
            b = busy[0]
            if s.before(b):  slots.pop(0)
            elif s.after(b): busy.pop(0)
            else:            yield slots.pop(0)
    return list(walk(slots[:], busy[:]))

def print_schedule(meetings):
    # print a human readable schedule
    for m in sorted(meetings.values(), key=lambda m: item(m.slots).start):
        s = item(m.slots)
        print(
            '{:30} {} to {}'.format(
                m.summary,
                s.start.strftime('%a, %b %d %I:%M %p'),
                s.end.strftime('%I:%M %p (%Z)'),
            )
        )

def schedule_meetings(meetings, calendar, location=None, description=None):
    # actually schedule the meetings on the given calendar at the given location
    for m in sorted(meetings.values(), key=lambda m: item(m.slots).start):
        r = schedule_meeting(m, calendar, location, description)
        print(json.dumps(r, indent=2))

def main():
    # set up credentials

    pacific = pendulum.timezone('US/Pacific')
    start_day = datetime.today() + timedelta(days=1)
    #print(start_day)
    start_time = time(9, 0, tzinfo=pacific)
    end_time = time(14, 0, tzinfo=pacific)
    days = 60
    now = datetime.now(tz=pacific)

    #def valid_date(s):
    #    try:
    #        return datetime.strptime(s, '%Y-%m-%d')
    #    except ValueError:
    #        msg = "Not a valid date: '{0}'.".format(s)
    #        raise argparse.ArgumentTypeError(msg)

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        'meetings',
        help='File containing meeting specs, one per line.',
        type=argparse.FileType(),
    )
    p.add_argument(
        '--schedule',
        dest='schedule',
        help='Actually schedule meetings. Otherwise just print a list of the times that would be scheduled.',
        action='store_true',
    )
    p.add_argument(
        '--calendar',
        dest='calendar',
        help='Email address of the calendar to create the meetings on.',
    )
    # p.add_argument(
    #     '--day',
    #     help='Date of meeting YYYY-MM-DD',
    #     #type=valid_date
    #     type=lambda d: datetime.strptime(d, '%Y-%m-%d'),
    # )

    args = p.parse_args()
    
    # if args.day: start_day = valid_date.datetime.date

    def to_meeting(line):
        pat = re.compile(r"^\[(\d+)\] *(.*?): *(.*)$")
        m = pat.match(line)
        return Meeting(m.group(2), int(m.group(1)), frozenset(re.split(r", *", m.group(3))))
    
    meetings = {id: to_meeting(line[:-1]) for id, line in enumerate(args.meetings)}
    meetings = schedule(meetings, start_day, start_time, end_time, days, now)

    if meetings is None: print('No way to schedule all meetings. Maybe time to become a goat farmer.')
    else:
        if not args.schedule:
            print(f'Calendar: {args.calendar}')
            print_schedule(meetings)
        else: schedule_meetings(meetings, args.calendar)

if __name__ == '__main__': main()

'''
https://developers.google.com/calendar/quickstart/python
    click enable api
    get credentials.json
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

pip install pendulum

python main.py -h
python main.py --schedule --calendar john.yohan.park@gmail.com meeting.txt
'''