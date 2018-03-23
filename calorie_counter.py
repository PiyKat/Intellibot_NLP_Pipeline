from listen import prompt

def calorie_counter(tag_list):

    from fatsecret import Fatsecret
    import re
    fs = Fatsecret("79d8c5015185494c9809255e77f06440","d3352b03ac2a476294206738d1db3405")

    for (word,tag) in tag_list:
        if tag == "IN":
            index = tag_list.index((word,tag))
            intent = tag_list[index-1][0]
            for (word,tag) in tag_list[index+1::]:
                if tag == "NN" or tag == "NNS" or tag == "NNP":
                    food = word
                    result = fs.foods_search(food,max_results=1)
                    print(result[0])
                    if intent == "calories":
                        calorie = result[0]['food_description'].split('-')[1].split('|')[0]
                        prompt(calorie)
                    elif intent == "nutrient":
                        nutrient_info = result[0]['food_description'].split("- ")[1]
                        prompt("Nutrient info is : " + nutrient_info)

            break

def trigger(stem,tag_list):

    def P(list): return set(list).intersection(stem)

    trigger_list = ['calories','nutrition','protein']

    if P(trigger_list):
        calorie_counter(tag_list)


tag_list = [(u'Tell', u'VB'), (u'me', u'PRP'), (u'the', u'DT'), (u'calories', u'NNS'), (u'in', u'IN'),(u'a',u'A'), (u'pizza', u'NNP')]
calorie_counter(tag_list)