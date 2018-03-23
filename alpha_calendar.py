from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from event import create_event

import time
from random import randint
import re
from smtplib import SMTP
from pygmail import collect_mail

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# other_party_dict = {}
user_dict = {}


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


def main(time_min, time_max, other_party_date, other_party_time=None):

    count = 0
    daily_schedule = []
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    temp1 = other_party_time.split(":")
    temp1[0] = str(int(temp1[0]) + 1)
    trial_time = ":".join(temp1)


    eventsResult = service.events().list(
        calendarId='primary', timeMin=time_min, timeMax=time_max, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    # print('events',type(events))

    # else:
    # prefered_time_1 = other_party_date+'T' + other_party_time + ":00" + "+05:30"



    if not events:
        print('No upcoming events found.')
        count = 0
        return count, daily_schedule

    for event in events:
        # print(' events found')
        # print(event)
        # print('\n')
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])
        daily_schedule.append(start)
        daily_schedule.append(event['summary'])
        count = 1
        return count, daily_schedule





def dict_retrieval(user_dict, other_party_dict,user_seed):

    print(other_party_dict)
    temp1 = other_party_dict['Time'].split(":")
    temp1[0] = str(int(temp1[0]) + 1)
    trial_time = ":".join(temp1)
    # print(trial_time)

    date = '2017-' + user_dict['meeting']['month'] + '-' + user_dict['meeting']['date']
    if date == other_party_dict['Date']:
        if other_party_dict['Time'] == user_dict['meeting']['time']:

            # print("kbfsbdsjdhf")
            print("Create event function is called!")
            create_event(other_party_dict, user_dict)
        else:
            prefered_time_1 = str(other_party_dict['Date']) + 'T' + str(other_party_dict['Time']) + ":00" + "+05:30"
            prefered_time_2 = str(other_party_dict['Date']) + 'T' + str(trial_time) + ':00' + '+05:30'
            count, temp = main(prefered_time_1, prefered_time_2, other_party_dict['Date'], other_party_dict['Time'])
            if count == 0:

                print('event is being created')
                create_event(other_party_dict, user_dict,prefered_time_1, prefered_time_2)
            else:
                print('You already have a meeting. meetings are as follows')

                prefered_time_1 = str(other_party_dict['Date']) + 'T' + str(other_party_dict['Time']) + ":00" + "+05:30"
                prefered_time_2 = str(other_party_dict['Date']) + 'T' + '23:59:00' + '+05:30'

                count, temp = main(prefered_time_1, prefered_time_2, other_party_dict['Date'], other_party_dict['Time'])
                print(temp)
                free_slot_list = free_slot(temp)
                #reply_mail_send(user_dict,type="further",seed = user_seed)
                new_other_party_dict = reply_mail_send(user_dict, free_slot_list, seed = user_seed)
                create_event(new_other_party_dict,user_dict)
                #user_dict['meeting']['time'] = free_slot_list[0]


    else:
        prefered_time_1 = str(other_party_dict['Date']) + 'T' + str(other_party_dict['Time']) + ":00" + "+05:30"
        prefered_time_2 = str(other_party_dict['Date']) + 'T' + str(trial_time) + ':00' + '+05:30'
        count, temp_2 = main(prefered_time_1, prefered_time_2, other_party_dict['Date'], other_party_dict['Time'])
        if count == 0:

            print("event created on other party's time")
            create_event(other_party_dict, user_dict)
        else:
            print('Time slot is not empty. you have following meetings')

            prefered_time_1 = str(other_party_dict['Date']) + 'T' + str(other_party_dict['Time']) + ":00" + "+05:30"
            prefered_time_2 = str(other_party_dict['Date']) + 'T' + '23:59:00' + '+05:30'
            count, temp = main(prefered_time_1, prefered_time_2, other_party_dict['Date'], other_party_dict['Time'])
            print(temp)
            free_slot(temp)


def reply_mail_send(main_dict,slots,seed):

    print("Reaching to the reply mail thread!!!!!")

    to = main_dict['meeting']['person_list'][-1]
    gmail_user = 'meeting.scheduler@untroddenlabs.com'
    gmail_pwd = '123456hamza'
    smtpserver = SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()  # extra characters to permit edit
    smtpserver.login(gmail_user, gmail_pwd)

    user_seed = seed
    unique_token = randint(1, 1000000)

    header = "To:" + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Time Clash :( , Free Times :)' + "\n"
    print(header)
    message = header + '\n Unfortunately, the time you mentioned is clashing with his schedule :o ' + '\n' + 'The following are the free slots' + \
              'available. Just let us know the time for the date. Let me know when you would like a meeting' + '\n' + \
              ",".join(slots) + '\n \n' + 'Unique Token : ' + str(unique_token)

    smtpserver.sendmail(gmail_user, to, message)
    print('done!')
    smtpserver.quit()

    counter_var = 0

    while (counter_var == 0):

        try:

            counter_var, other_party_dict = collect_mail(unique_token, main_dict,user_seed)

            if counter_var == 1:
                print("Found the relevant mail")
                return other_party_dict
        except:

            time.sleep(10)
            continue




def free_slot(temp):

    time_slots = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00',
                  '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
                  '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    available = []
    for i in temp[::2]:
        # print('i',i)
        temp_2 = i
        temp_time = i.split("T")[1]
        time = temp_time.split(":")
        time.pop(-1)
        time.pop(-1)
        new_time = ":".join(time)
        # print(new_time)
        time = re.search("[/d]*:[/d]", temp_time)
        for p in time_slots:
            if p == new_time:
                t = time_slots.index(p)
                for x in time_slots[t + 1:]:
                    available.append(x)



                    # print(time)
                    # time = temp_time.split(":")
    print('time slots available:', available)
    return available