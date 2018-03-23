def extract_mail(message_body):  # email_from, subject,
    import re
    temp = message_body.split('\n')
    temp = [x for x in temp if x is not '']

    other_party_dict = {}
    for variables in temp:
        data = re.split('(?<!\d):[\s]*', variables)

        try:
            other_party_dict[data[0]] = data[1].replace('\r', "")
        except:
            print("Data is not being split ?")

    print("Final Dictionary : ", other_party_dict)

    if len(other_party_dict.values()) != 0:
        return 1, other_party_dict
    else:
        return 0, {}