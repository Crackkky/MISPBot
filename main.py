import json

import tweepy
import httplib2
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET_TOKEN = os.getenv('ACCESS_SECRET_TOKEN')

MISP_KEY = os.getenv('MISP_KEY')

API_URL = os.getenv('API_URL')


def httpPost(url, headersP, bodyP):
    http = httplib2.Http()
    bodyP = json.dumps(bodyP)
    content = http.request(url,
                           method="POST",
                           headers=headersP,
                           body=bodyP)[1]
    return content


if __name__ == '__main__':
    headers = {'Authorization': MISP_KEY, 'Accept': 'application/json', 'Content-type': 'application/json'}
    body = {"returnFormat": "json", "last": "5h"}

    result = httpPost(API_URL, headers, body)

    response = json.loads(result)
    s = ""
    print(
        "_______________________________________________________________________________________________________________")
    for i in range(0, 27):
        try:
            s = response["response"][i]["Event"]["id"]
            print(s)
        except IndexError:
            break
        except Exception as exp:
            exit(exp)

    print('Done!')

    # # Authenticate to Twitter
    # auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    #
    # # Create API object
    # api = tweepy.API(auth)
    #
    # # Create a tweet
    # api.update_status("This is a test")
