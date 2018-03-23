def trigger(lem,tag):
    def P(list): return set(list).intersection(lem)
    w1 = ['mean','define','definition','about']
    if P(w1):
        print(api(tag))


def api(tag):
    import requests
    from pattern.search import search

    store = dict(tag)

    del store['define']
    query = store.keys()[0]
    r = requests.get("https://owlbot.info/api/v1/dictionary/"+query)
    return r.json()[0]['defenition']