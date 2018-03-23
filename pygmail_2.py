from gmail import Gmail
import datetime
import time
from mail_extraction import extract_mail
from alpha_calendar import create_event,dict_retrieval

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
        #print(len(other_party_data))
        #other_party_data = [word for word in other_party_data.split(" ") if other_party_data.isalnum()]
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
                create_event(user_dict,user_dict)
                return 1
            else:
                found,other_party_dict = extract_mail(other_party_data)

                if len(other_party_dict) > 0:
                    dict_retrieval(user_dict,other_party_dict,user_seed)

                return found

    else:
        return 0