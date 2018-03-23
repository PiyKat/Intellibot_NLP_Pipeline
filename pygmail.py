from gmail import Gmail
import datetime
import time
from mail_extraction import extract_mail
#from event import create_event

def collect_mail(user_token,user_dict,user_seed):

    found = 0
    username = "meeting.scheduler@untroddenlabs.com"
    password = "123456hamza"

    g = Gmail()

    g.login(username,password = password)


    relevant_mail = g.inbox().mail(unread=True, sender=user_dict['meeting']['person_list'][-1])

    relevant_mail[-1].fetch()

    if str(user_token) in relevant_mail[-1].body:

        print("Message Found!")
        print ("Email Body : ", relevant_mail[-1].body)
        other_party_data = relevant_mail[-1].body.split("\r\n\r\n")[0]

        for words in other_party_data.split(" "):
            if words.lower() in ["yes","sure","fine","confirmed","book"]:
                temporary_dict = {}
                user_dict = user_dict['meeting']
                #for subdict in user_dict:
                for user_keys in user_dict.keys():
                    temporary_dict[user_keys.title()] = user_dict[user_keys]
                    #create_event(temporary_dict,user_dict)

                temporary_dict['Date'] = '2017-' + temporary_dict['Month'] + '-' + temporary_dict['Date']
                del temporary_dict['Month']

                return 1, temporary_dict
            else:
                return extract_mail(other_party_data)


        else:
            return 0, {}