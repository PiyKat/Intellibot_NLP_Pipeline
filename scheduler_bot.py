import pyttsx


engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 40)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def conversation_scheduler(main_dict, null_list):
    from listen import listen,prompt
    info_check = 1
    filled_list = []
    count = 0

    contacts = open("contact_data.txt")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    #print("Do you want to enter more details?")
    prompt("Do you want to enter more details?")
    ask = listen('yesno')
    if ask == "yes" or ask == "Yes":
        for attribute in null_list:
            if attribute == "person_list":

                temp = (raw_input("who do you want to setup meeting with: "))
                print('person name input', temp)
                temp_2 = contacts.read().split(',')
                contacts.close()
                for i in temp_2:
                    # print('value of i', i)
                    if i == temp:
                        print('if true')
                        t = temp_2.index(i)
                        print('email', temp_2[t + 1])

                        main_dict['meeting']['person_list'].append(temp)
                        # print('running')
                        main_dict['meeting']['person_list'].append(temp_2[t + 1])
                        filled_list.append(attribute)
                        count += 1
                        print('count', count)
                        break

                    else:
                        continue
                if count == 0:
                    temp_3 = str(raw_input('please provide the email id of %s : ' % temp))
                    f = open("contact_data.txt", "a+")
                    f.write(",%s, %s, " % (temp, temp_3))
                    main_dict['meeting']['person_list'].append(temp)
                    main_dict['meeting']['person_list'].append(temp_3)
                    filled_list.append(attribute)
                    f.close()
                    count += 1

                if count == 0:
                    return info_check, main_dict, temp

            elif attribute == 'date':

                prompt('Please specify on which date you want to conduct the meeting: ')
                date = listen('num')
                if date not in [str(i) for i in range(1, 32)]:
                    return info_check, main_dict, date
                else:
                    main_dict["meeting"][attribute] = date
                    filled_list.append(attribute)


            elif attribute == "month":

                prompt('Please specify in which month you want to conduct the meeting: ')
                month = listen('num')
                # monthdict = {'January':01,'February':02,'March':03,'April':04,'May':05,'June':06,'July':07,u'August':'08',"September":'09',"October":10,"November":11,"December":12}
                # month = int(monthdict[monthword])
                # if month not in ["January","February","March","April","May","June","July","August", "September", "October", "November", "December"]:
                if month not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:  # or
                    return info_check, main_dict, month
                else:
                    main_dict["meeting"][attribute] = month
                    filled_list.append(attribute)


            elif attribute == 'time':

                prompt('Please specify at what time you want to conduct the meeting: ')
                timeword = listen('num')
                time = timeword + ':00'
                main_dict["meeting"][attribute] = time
                filled_list.append(attribute)


            elif attribute == 'location':

                prompt('Please specify at the location where you want to conduct the meeting: ')
                location = listen()
                main_dict["meeting"][attribute] = location
                filled_list.append(attribute)

    for remove in filled_list:
        null_list.remove(remove)

    if len(null_list) == 0:
        info_check = 0

    if info_check != 0:
        print("There is still some work to be done!")
        print("Check for the main dictionary : ", main_dict)
        print('final null list', null_list)
        return conversation_scheduler(main_dict, null_list)
    else:
        # print("The information is complete")
        # print(main_dictionary)
        return info_check, main_dict, ""