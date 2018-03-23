from listen import prompt

def get_definition(tag_list):

    from nltk.corpus import wordnet as wn

    for (word,tag) in tag_list:
        if tag == "IN" and word == "of":
            def_word = tag_list[tag_list.index((word,tag))+1][0]
            words = wn.synsets(def_word)
            print(words)
            prompt(words[0].definition())


def trigger(stem,tag_list):

    def P(list): return set(list).intersection(stem)

    trigger_list = ['definition', 'define', 'meaning']

    if P(trigger_list):
        get_definition(tag_list)