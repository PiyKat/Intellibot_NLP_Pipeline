import requests


def send_request():
    url = "http://35.154.184.57:1337/api/flightbot"
    headers = {'Content-type': 'application/json'}

    r = requests.post(url, data=open("json_file.json",'rb'), headers=headers)
    print(r.json())