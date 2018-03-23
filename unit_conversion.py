from listen import prompt

def change_currency(tag_list):

    def symbols(tag_list):

        for (word, tag) in tag_list:
            if tag == "TO" and word == "to":
                loc = tag_list.index((word, tag))
                base = tag_list[loc - 1][0]
                symbol = tag_list[loc + 1][0]
                break
        print("{} {}".format(base, symbol))
        return base, symbol


    import requests

    base,symbol = symbols(tag_list)

    for (word,tag) in tag_list:
        if tag == "CD":
            get_rate = "http://api.fixer.io/latest?base="+base+"&symbols="+symbol
            curr_json = requests.get(get_rate)
            print(curr_json.json())
            rate = curr_json.json()['rates']['INR']
            converted_amount = rate*float(word)

    prompt("The converted value is " + str(converted_amount))
    prompt("That would be a million dollars! I only accept cash please :)")


def unit_convert(tag_list):

    from pint import UnitRegistry

    ureg = UnitRegistry()

    def symbols(tag_list):

        for (word, tag) in tag_list:
            if tag == "TO" and word == "to":
                loc = tag_list.index((word, tag))
                base_1 = tag_list[loc - 1][0]
                base_2 = tag_list[loc + 1][0]
                break
        print("{} {}".format(base_1, base_2))
        return base_1, base_2

    from_unit,to_unit = symbols(tag_list)

    for (word,tag) in tag_list:

        if tag == "CD":

            initial = int(word) * ureg.parse_expression(from_unit)
            try:
                convert = initial.to(ureg.parse_expression(to_unit))
            except:
                prompt("Either youre an idiot or the module is wrong :)")

    prompt("The converted value is " + str(convert.magnitude))



def trigger(stem,tag_list):

    def P(list): return set(list).intersection(stem)

    convert_list = ['convert']
    currency_list = ['INR','USD']
    #mass_list = ['kg','kilogram','gram','g']
    #length_list = ['inch','feet','meter','m','centimeter','cm','yard','km','kilometer']

    if P(convert_list):
        if P(currency_list):
            change_currency(tag_list)
        else:
            unit_convert(tag_list)