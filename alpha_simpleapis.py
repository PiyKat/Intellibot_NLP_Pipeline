def trigger(lem):
    def P(list): return set(list).intersection(lem)
    w1=['joke','fact']
    if P(w1):
        w = P(w1)
        w = list(w)[0]
        print(api(w))


def api(w):
    import requests
    if w == 'joke':
        r = requests.get('http://tambal.azurewebsites.net/joke/random')
        return (r.json()['joke'])
    elif w == 'fact':
        r = requests.get('http://numbersapi.com/random')
        return r.content