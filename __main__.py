import sys
import os
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from gcalendar_skill import *

"""Shows basic usage of the Google Calendar API.

Creates a Google Calendar API service object and outputs a list of the next
10 events on the user's calendar.
"""
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

now = dt.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
eventsResult = service.events().list(
    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
events = eventsResult.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    d = dt.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
    starttime = dt.datetime.strftime(d, '%H %M')
    print(event['summary'] + ' at ' + starttime)