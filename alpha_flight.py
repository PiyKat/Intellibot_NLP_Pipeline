def trigger(ret,stem,tag):
    def P(list): return set(list).intersection(stem)
    w1 = ['book','schedul','reserv']
    w2=['flight']
    if P(w1):
        if P(w2):
            flight_subroutine(tag)

    elif ret==True or ret==False:
        return False
    else:
        return ret


def flight_subroutine(tag):
    from nltk import RegexpParser
    import re



    grammar = '''
            date : {<IN>?(<CD>|<OD>|<JJ>)<IN>?(<NNP>)+}
                        }<IN>{
            from-to :{<IN>?<NNP>*<TO>?<NNP>*}
                        }<IN>|<TO>{
            class : {<IN><DT>?<NN|JJ>}
                        }<IN>|<DT>{
            passengers : {(<CD>)(<NN>|<NNS>|<JJ>)<CC><CD>(<NN>|<NNS>)}
                        }<CC>|<NN>|<NNS>|<JJ>{
                '''


    chunker = RegexpParser(grammar)
    parse_tree = chunker.parse(tag)

    source_name = None
    destination_name = None
    source_country = None
    source_code = None
    destination_country = None
    destination_code = None
    flight_class = None
    adult = None
    children = None
    date = None
    month = None

    for trigger_word in ["adult","adults"]:
        for (word,label) in parse_tree.leaves():
            if word == trigger_word:
                adult = parse_tree[parse_tree.index((word,label))-1][0][0]

    for trigger_word in ["child","children"]:
        for (word,label) in parse_tree.leaves():
            if word == trigger_word:
                children = parse_tree[parse_tree.index((word,label))-1][0][0]

    for trees in parse_tree.subtrees(lambda x : x.label() == "class"):
        flight_class = trees.leaves()[0][0]

    for (word,tag) in parse_tree.leaves():

        if word == "to" or word =="To":
            if type(parse_tree[parse_tree.index((word,tag)) + 1].leaves()) == list and parse_tree[parse_tree.index((word,tag)) + 1].label() == "from-to":
                destination_dict = extract_code(" ".join([keyword for (keyword,tag_2) in parse_tree[parse_tree.index((word,tag)) + 1]]))
                destination_code = destination_dict['code']
                destination_name = destination_dict['name']
                destination_country = destination_dict['country_code']
            elif type(parse_tree[parse_tree.index((word,tag)) + 1].leaves()) == tuple:
                #destination = parse_tree[parse_tree.index((word,tag)) + 1][0][0]
                destination_dict = extract_code(parse_tree[parse_tree.index((word,tag)) + 1][0][0])
                destination_code = destination_dict['code']
                destination_name = destination_dict['name']
                destination_country = destination_dict['country_code']
            else:
                destination = None
            try :
                if type(parse_tree[parse_tree.index((word,tag)) - 1].leaves()) == list and parse_tree[parse_tree.index((word,tag)) - 1].label() == "from-to":
                    source_dict = extract_code(" ".join([keyword for (keyword,tag_2) in parse_tree[parse_tree.index((word,tag)) - 1]]))
                    source_code = source_dict['code']
                    source_name = source_dict['name']
                    source_country = source_dict['country_code']

                elif type(parse_tree[parse_tree.index((word,tag)) - 1].leaves()) == tuple:
                    #source = parse_tree[parse_tree.index((word,tag)) - 1][0][0]
                    source_dict = extract_code(parse_tree[parse_tree.index((word,tag)) - 1][0][0])
                    source_code = source_dict['code']
                    source_name = source_dict['name']
                    source_country = source_dict['country_code']
            except:
                print("It's reaching here")

        if word == "from" or word == "From":
            try :

                if type(parse_tree[parse_tree.index((word,tag)) + 1].leaves()) == list and parse_tree[parse_tree.index((word,tag)) + 1].label() == "from-to":
                    source_dict = extract_code(" ".join([keyword for (keyword,tag_2) in parse_tree[parse_tree.index((word,tag)) + 1]]))
                    source_code = source_dict['code']
                    source_name = source_dict['name']
                    source_country = source_dict['country_code']
                    #source = " ".join([keyword for (keyword,tag_2) in parse_tree[parse_tree.index((word,tag)) + 1]])#parse_tree[parse_tree.index((word,tag)) + 1]
                elif type(parse_tree[parse_tree.index((word,tag)) + 1].leaves()) == tuple:
                    #source = parse_tree[parse_tree.index((word,tag)) + 1][0][0]
                    source_dict = extract_code(parse_tree[parse_tree.index((word,tag)) + 1][0][0])
                    source_code = source_dict['code']
                    source_name = source_dict['name']
                    source_country = source_dict['country_code']
            #else:

            except :
                print("You are reaching here")


    for trees in parse_tree.subtrees(lambda x: x.label() == "date"):
        for (word,tag) in trees.leaves():
            if tag == "CD" or tag == "JJ":
                date = re.sub("[A-Za-z]*","",word)
            elif tag == "NNP":
                month = word


    main_dictionary = {'flight':{'flight_class':flight_class,'source':source_name,
                                 'source_country':source_country,
                                 'source_code':source_code,
                                 'destination':destination_name,
                                 'destination_country':destination_country,
                                 'destination_code':destination_code,
                                 'date':date,
                                 'month':month,
                                 'adults':adult,
                                 'children':children
                                 }
                       }
    print(main_dictionary)
    null_list = []
    for attributes in main_dictionary['flight'].keys():
        if main_dictionary['flight'][attributes] == None:
            null_list.append(attributes)
    completed = len(null_list)
    if completed != 0:
        completed, flight_dictionary, string_check = conversation_agent(main_dictionary, null_list)

    if completed == 0:
        print("Final flight dictionary : ", main_dictionary)
        json_conversion(main_dictionary)
        return completed,"",{}







def json_conversion(subroutine_dictionary):
    import json
    import alpha_flight_send
    import random

    json_dictionary = {"user_id": random.randint(0,2147483000),
     "user_email": "harpreet@untroddenlabs.com",
     "source": subroutine_dictionary["flight"]["source"],
    "destination": subroutine_dictionary["flight"]["destination"],
    "source_code":subroutine_dictionary['flight']['source_code'],
    "source_country":subroutine_dictionary["flight"]['source_country'],
    "destination_code":subroutine_dictionary['flight']['destination_code'],
    "destination_country":subroutine_dictionary['flight']['destination_country'],
     "trip_type": "none",
     "is_request_informational": {"status": "none", "past_flight_journeys": "none", "upcoming_flight_journeys": "none"},
     "is_repeat_booking": "none", "repeat_booking_date": "none", "class": subroutine_dictionary['flight']['flight_class'],
     "max_desired_number_of_stops": "none", "max_desired_price": "none", "currency": "none", "payment_mode": "none",
     "duration_of_journey": "none", "seat_preference": "none", "food_preferences": "none", "extra_baggage": "none",
     "preferred_airlines": "none", "seats": {"adults": subroutine_dictionary['flight']['adults'], "children": subroutine_dictionary['flight']['children'],
                                             "infants": 0}, "passenger_details": {
        "adults": {"adult1": {"name": "None", "age": "none"}, "adult2": {"name": "none", "age": "none"}},
        "infants": {"infant1": {"name": "none", "age": "none"}}}, "multicity": {"1": "none", "2": "none", "3": "none"},
     "date": subroutine_dictionary['flight']['date'], "month": subroutine_dictionary['flight']['month'], "time_of_day": "none", "sort_by": "none"}








    # json_dictionary = {
    #     "user_id" : random.randint(1,99999999999999999),
    #     "source": subroutine_dictionary["flight"]["source"],
    #     "destination": subroutine_dictionary["flight"]["destination"],
    #     "source_code":subroutine_dictionary['flight']['source_code'],
    #     "source_country":subroutine_dictionary["flight"]['source_country'],
    #     "destination_code":subroutine_dictionary['flight']['destination_code'],
    #     "destination_country":subroutine_dictionary['flight']['destination_country'],
    #     "trip_type":"none",
    #     "is_request_informational": {
    #         "status": "none",
    #         "past_flight_journeys": "none",
    #         "upcoming_flight_journeys": "none"
    #     },
    #     "is_repeat_booking" : "none" ,
    #     "repeat_booking_date" : "none" ,
    #     "class": subroutine_dictionary['flight']['source'],
    #     "max_desired_number_of_stops": "none",
    #     "max_desired_price" : "none" ,
    #     "currency" : "none" ,
    #     "payment_mode" : "none",
    #     "duration_of_journey": "none",
    #     "seat_preference" : "none",
    #     "food_preferences" : "none",
    #     "extra_baggage" : "none",
    #     "preferred_airlines" : "none",
    #     "seats": {
    #         "adults": subroutine_dictionary['flight']['adults'],
    #         "children": subroutine_dictionary['flight']['children'],
    #         "infants": 0
    #     },
    #     "passenger_details": {
    #         "adults": {
    #             "adult1" : {
    #                 "name" : "None",
    #                 "age" : "none"
    #             },
    #             "adult2" : {
    #                 "name" : "none",
    #                 "age" : "none"
    #             }
    #         },
    #         "infants":  {
    #             "infant1" : {
    #                 "name" : "none",
    #                 "age" : "none"
    #             }
    #         }
    #     },
    #     "multicity": {
    #         "1": "none",
    #         "2": "none",
    #         "3": "none"
    #     },
    #     "date": subroutine_dictionary['flight']['date'],
    #     "month" : subroutine_dictionary['flight']['month'],
    #     "time_of_day": "none",
    #     "sort_by" : "none"
    # }

    with open('json_file.json',"w") as fp:
        json.dump(json_dictionary,fp)

    alpha_flight_send.send_request()




def extract_code(city):
    from iata_codes.cities import IATACodesClient
    client = IATACodesClient('fa25086e-caf2-4d20-b7e8-32d88b8e2c73')
    x = client.get(name=city)
    if len(x) > 1000:
        return None
    else:
        return x[0]


def conversation_agent(main_dictionary,null_list):

    from listen import listen,prompt
    import pattern.en as p

    info_check = 1
    filled_list = []

    for attribute in null_list:

        if attribute == "month":
            prompt("Which month should your flight be scheduled for : ")
            month = listen('month')
            if month not in ["January","February","March","April","May","June","July","August","September","October","November","December"]:
                return info_check,main_dictionary,month
            else:
                main_dictionary["flight"][attribute] = month
                filled_list.append(attribute)

        if attribute == "date":
            prompt("Which date would you like your flight to be : ")
            date = listen('num')
            if date not in [str(i) for i in range(1,32)]:
                return info_check,main_dictionary,date  # continue

            else:
                main_dictionary["flight"][attribute] = date
                filled_list.append(attribute)

        elif attribute == "adults":

            prompt("How many adults in the flight : ")
            adult_2 = listen('num')
            if adult_2.split(" ")[0].isdigit() or p.number(adult_2.split(" ")[0]):
                main_dictionary["flight"][attribute] = adult_2
                filled_list.append(attribute)

            else:
                return info_check,main_dictionary,adult_2

        elif attribute == "children":
            prompt("How many children? : ")
            children = listen('num')
            if children.isdigit():
                main_dictionary["flight"][attribute] = children
                filled_list.append(attribute)
            else:
                return info_check,main_dictionary,children
                #worker_allocation(children)

        elif attribute == "flight_class":
            prompt("Any flight class you'd like to mention : ")
            flight_class = listen("class")

            if flight_class not in ["economy","Economy","Business","business"]:
                #worker_allocation(flight_class)
                return info_check,main_dictionary,flight_class
            else:
                main_dictionary["flight"][attribute] = flight_class
                filled_list.append(attribute)

        elif attribute == "source":
            prompt("Enter the source of the flight : ")
            source=listen()
            if extract_code(source) is None:
                #worker_allocation(source)
                return info_check,main_dictionary,source
            else:
                source_dict = extract_code(source)
                #source_code = extract_code(source)
                main_dictionary["flight"][attribute] = source_dict['name']
                main_dictionary['flight']['source_country'] = source_dict['country_code']
                main_dictionary['flight']['source_code'] = source_dict['code']
                filled_list.append(attribute)
                filled_list.append('source_country')
                filled_list.append('source_code')

        elif attribute == "destination":
            print("Enter the destination of the flight : ")
            destination = listen()
            if extract_code(destination) is None:
                return info_check,main_dictionary,source
                #worker_allocation(destination)
            else:
                dest_dict = extract_code(destination)
                main_dictionary["flight"][attribute] = dest_dict['name']
                main_dictionary['flight']['destination_country'] = dest_dict['country_code']
                main_dictionary['flight']['destination_code'] = dest_dict['code']
                filled_list.append(attribute)
                filled_list.append('destination_country')
                filled_list.append('destination_code')

    for remove in filled_list:
        null_list.remove(remove)

    if len(null_list) == 0:
        info_check = 0

    if info_check != 0:
        print("There is still some work to be done!")
        print("Check for the main dictionary : ",main_dictionary)
        return conversation_agent(main_dictionary,null_list)
    else:
        print("The information is complete")
        #print(main_dictionary)
        return info_check,main_dictionary,""