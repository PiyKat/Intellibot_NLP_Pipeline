from listen import prompt

def retrieve_ticker(company_name):

    import requests
    from yahoo_finance import Share

    #ticker_retr = "http://d.yimg.com/aq/autoc?query=" + company_name.lower() + "&region=US&lang=en-US&callback=YAHOO.util.ScriptNodeDataSource.callbacks"
    ticker_retr = "http://autoc.finance.yahoo.com/autoc?query="+company_name.lower()+"&region=EU&lang=en-US"

    get_data = requests.get(ticker_retr)
    ticker = get_data.json()['ResultSet']['Query']

    share = Share(ticker)
    share_price = share.get_price()
    prompt("The share price for "+company_name+" is "+ share_price)


def trigger(tag_list):

    stem = []
    company = []

    from nltk import SnowballStemmer
    s = SnowballStemmer("english")

    for (word,tag) in tag_list:

            if tag != "NNP":
                stem.append(s.stem(word))
            else:
                company.append(word.lower())

    company_name = "".join(company)

    def P(list): return set(list).intersection(stem)

    stock_call = ['stock','price','share']
    if P(stock_call):
        ticker = retrieve_ticker(company_name)