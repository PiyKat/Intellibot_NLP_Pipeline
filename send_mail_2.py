from smtplib import SMTP
from pygmail import collect_mail
import time
import random
from random import randint
from alpha_calendar import dict_retrieval

def send_mail(main_dict,type,slots = None,seed = None):

    print('mail_dict', main_dict)

    to = main_dict['meeting']['person_list'][-1]
    gmail_user = 'meeting.scheduler@untroddenlabs.com'
    gmail_pwd = '123456hamza'
    smtpserver = SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()  # extra characters to permit edit
    smtpserver.login(gmail_user, gmail_pwd)

    if type == "init":
        x = randint(1,30000)
        message_seed = random.seed(x)
        unique_token = randint(1, 1000000)

        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Meeting Time ! ' + "\n"
        print (header)
        msg = header + '\n muffin wants to meet you \n Location :' + str(main_dict['meeting']['location']) + '\n Time:' + \
              str(main_dict['meeting']['time']) + '\n Date :' + str(main_dict['meeting']['date']) + '\n Month: ' + \
              str(main_dict['meeting']['month']) + '\n \n' + 'Unique Token : ' + str(unique_token)

        smtpserver.sendmail(gmail_user, to, msg)
        print ('done!')
        smtpserver.quit()

        counter_var = 0
        starttime = time.time()

        while (counter_var == 0):

            try:

                counter_var,other_party_dict = collect_mail(unique_token, main_dict,message_seed)
                if len(other_party_dict) > 0:
                    dict_retrieval(main_dict, other_party_dict,message_seed)
                if counter_var == 1:
                    print("Found the relevant mail")
            except:

                time.sleep(10)
                continue

    elif type == "further":

        user_seed = seed
        unique_token = randint(1, 1000000)

        header = "To:" + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Time Clash :( , Free Times :)' + "\n"
        print(header)
        msg = header + '\n Unfortunately, the time you mentioned is clashing with his schedule :o ' + '\n' + 'The following are the free slots' \
        +'available. Just let us know the time for the date. Let me know when you would like a meeting' + '\n' + \
        slots +'\n \n' + 'Unique Token : ' + str(unique_token)

        smtpserver.sendmail(gmail_user, to, msg)
        print ('done!')
        smtpserver.quit()

        counter_var = 0
        starttime = time.time()

        while (counter_var == 0):

            try:

                counter_var, other_party_dict = collect_mail(user_seed, main_dict)
                dict_retrieval(main_dict,other_party_dict,user_seed = user_seed)
                if counter_var == 1:
                    print("Found the relevant mail")
            except:

                time.sleep(10)
                continue