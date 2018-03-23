from __future__ import print_function
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_event(other_party_dict, user_dict,prefered_time_1 = None,prefered_time_2 = None):

    print("I've reached to the printing ")

    credentials = get_credentials()
    print("Credentials are clear")

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    temp1 = other_party_dict['Time'].split(":")
    print(temp1)
    temp1[0] = str(int(temp1[0]) + 1)
    trial_time = ":".join(temp1)

    event = {
        'summary': 'TESTING TESTING 1 2 3',
        'location': 'Untrodden Labs Office',
        'description': 'Man let us get it over with',
        'start': {
            'dateTime': other_party_dict['Date'] + 'T' + other_party_dict['Time'] + ':00',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': other_party_dict['Date'] + 'T' + trial_time + ':00',
            'timeZone': 'Asia/Kolkata',
        },
        # 'recurrence': [
        #  'RRULE:FREQ=DAILY;COUNT=1'
        # ],
        'attendees': [
            {  # 'email': 'gagan@untroddenlabs.com'},   # fetch the other party email here
                'email': user_dict['meeting']['person_list'][-1]
            }
            # {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))