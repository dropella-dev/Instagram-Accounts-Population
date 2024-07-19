import requests
import random
def initiate_order(profile):
    try:
        url = "https://cloutsy.com/api/v2"
        key = "c68fff284c7f2b5e9537315108af0253"
        action = "add"
        querystring = {}
        querystring['key'] = key
        querystring['action'] = action
        querystring['link'] = profile
        querystring['service'] = "62"
        querystring['quantity'] = f"{random.randrange(100,350)}"
        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)
        if response.status_code == 200 and 'order' in response.json():
            print(f"Instagram Followers order initiated for {profile}")
        else:
            print(f"can't initiate order Instagram Followers for {profile}")
    except:
        print(f"can't initiate order Instagram Followers for {profile}")