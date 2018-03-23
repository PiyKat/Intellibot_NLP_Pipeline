from nltk import RegexpParser
from nltk.tag.stanford import StanfordPOSTagger
from scheduler_bot import conversation_scheduler


from listen import prompt
from send_mail_2 import send_mail

english_postagger = StanfordPOSTagger('../stanford-postagger/models/english-bidirectional-distsim.tagger',
                                      '../stanford-postagger/stanford-postagger.jar')

contacts = open("contact_data.txt")

other_party_dict = {}


def entity_ext(sentence, main_dict):
    prompt("It is always good to catch up with your new friends!")
    if len(main_dict) == 0:
        grammar = '''
                rel_day:{(<JJ>|<DT>|<VBG>)<NNP>}
                date :{(<IN><JJ><IN>?<NNP>)}
                day:{(<IN>(<NNP>|<NN>))}
                person:{((<NN>|<NNP>)<IN>?<NNP><CC>?<NNP>?)}

                        '''
        # Initial : {((<WP>|<WRB>|<VB>)(<DT|VBZ>)+<NN>+)}'''

        init_chunker = RegexpParser(grammar)
        initial_tree = init_chunker.parse(sentence)
        #initial_tree.draw()

        # print('entity extraction running')
        time = None

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        key = None
        day = None

        date = None
        month = None

        key_or_date = None
        day_or_month = None

        person_list = []

        location = None

        # print('leaves',initial_tree.leaves())
        # for word, tag in pos_sentence:
        for trees in initial_tree.subtrees(lambda x: x.label() == "day"):
            for (word, tag) in trees.leaves():
                if tag in ['NNP', 'NN'] and word not in days:
                    person_list.append(word)
                    temp_9 = contacts.read().split(',')
                    contacts.close()
                    for i in temp_9:
                        # print('value of i', i)
                        if i == word:
                            # print('if true')
                            t = temp_9.index(i)
                            print('email', temp_9[t + 1])
                            person_list.append(temp_9[t + 1])

                            # main_dict['meeting']['person_list'].append(temp)
                            # print('running')
                else:
                    continue

        for trees in initial_tree.subtrees(lambda x: x.label() == 'date'):
            for word, tag in trees.leaves():
                if tag == 'JJ':
                    key_or_date = word
                elif tag == 'NNP':
                    # print('asd')
                    day_or_month = word
                else:
                    continue

        for trees in initial_tree.subtrees(lambda x: x.label() == 'day'):
            for word, tag in trees.leaves():
                if tag == 'NNP' and word in days:
                    # print('asd232')
                    day_or_month = word
                else:
                    continue

        for trees in initial_tree.subtrees(lambda x: x.label() == 'rel_day'):
            for (word, tag) in trees.leaves():
                if tag == 'NNP':
                    day_or_month = word
                elif tag in ['VBG', 'JJ', 'DT']:
                    key_or_date = word
                else:
                    continue

        if key_or_date in ['next', 'coming', 'this']:
            key = key_or_date
        else:
            date = key_or_date

        if day_or_month in days:
            day = day_or_month
        else:
            month = day_or_month

        main_dict = {'meeting': {'person_list': person_list,
                                 'date': date,
                                 'month': month,
                                 'time': time,
                                 'location': location
                                 }}

        # print('main_dict after input', main_dict)
        null_list = []

        for attributes in main_dict['meeting'].keys():
            if main_dict['meeting'][attributes] == None or len(main_dict['meeting'][attributes]) == 0:
                null_list.append(attributes)
        # print('null list after input', null_list)
        completed = len(null_list)
        if completed != 0:

            completed, schedule_dict, string_check = conversation_scheduler(main_dict, null_list)

            if string_check:
                return completed, schedule_dict, string_check

    else:
        null_list = []

        for attributes in main_dict['meeting'].keys():
            if main_dict['meeting'][attributes] == None:
                null_list.append(attributes)

        completed, schedule_dict, string_check = conversation_scheduler(main_dict, null_list)

        if string_check:
            return completed, main_dict, string_check

    if completed == 0:
        # print("Final meeting dictionary : ", schedule_dict)
        # print("final dict",main_dict)
        send_mail(schedule_dict,type="init")
        return completed, "", {}


def intent_class(sentence, main_dict):
    # print('intent classification running')

    intent = None
    for word, tag in sentence:
        # print(word, tag)
        if word in ["meeting", "Meeting"] and tag == 'NN':
            intent = word
            break
        elif word in ['meet'] and tag == 'VB':
            intent = word
            break
        else:
            continue
    # print('intent',intent)



    return intent


def schedule_subroutine(sentence):  # main_dict from muffin
    # token_list = nltk.word_tokenize(sentence)
    # pos_sentence = english_postagger.tag(token_list)
    # print('postag', pos_sentence)

    main_dict = {}
    intent = intent_class(sentence, main_dict)
    if intent != None:
        entities = entity_ext(sentence, main_dict)
    else:
        print('input error')

# In case the code doesn't work, you have to pase the code here


def trigger(stem, pos_sentence):
    def P(list):
        return set(list).intersection(stem)
    w1 = ['book', 'schedul']
    w2 = ['meet']
    if P(w1):
        if P(w2):
            schedule_subroutine(pos_sentence)