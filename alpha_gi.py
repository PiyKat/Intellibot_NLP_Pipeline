def trigger(ret,stem,tag):
    def P(list): return set(list).intersection(stem)
    info = ['weather','temperatur','time','tempratur']
    if P(info):
        query=P(info)
        query=list(query)[0]
        print(api(ret,stem,tag,query))


def api(ret,stem,tag,query):
    from nltk import RegexpParser
    grammar = ''' loc : {<NNP>+} '''
    chunker = RegexpParser(grammar)
    parse_tree = chunker.parse(tag)
    for tree in parse_tree.subtrees(filter=lambda x: x.label() == "loc"):
        location = " ".join([word for (word, tag) in tree.leaves()])
    gi_dict = gi_result(location)

    output = {'weather':gi_dict['current']['condition']['text'],
              'temperature':gi_dict['current']['temp_c'],
              'time':gi_dict['location']['localtime'].split()[1]}
    return output[query]

def gi_result(location):
    from requests import get
    if len(location) > 1:
        location = "_".join(location.split(" "))
    url = "http://api.apixu.com/v1/current.json?key=6d8d449d15954907b4483703172502&q=" + location
    r = get(url)
    return r.json()