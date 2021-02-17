import json

import tweepy
import httplib2
import os
from EventMisp import EventMisp
from datetime import datetime
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
    body = {"returnFormat": "json", "last": "3h"}

    result = httpPost(API_URL, headers, body)

    response = json.loads(result)

    # f = open("testRequest.json", "a")
    # f.write(result.decode("utf-8"))
    # f.close()

    s = ""
    i = 0
    eventArray = []
    print("__________________________________________________________")
    while True:
        try:
            eventArray.append(EventMisp(response["response"][i]["Event"]["id"],
                                        response["response"][i]["Event"]["date"],
                                        response["response"][i]["Event"]["info"],
                                        datetime.fromtimestamp(int(response["response"][i]["Event"]["timestamp"])),
                                        response["response"][i]["Event"]["published"],
                                        response["response"][i]["Event"]["Orgc"]["name"]))

            '''idEvent = response["response"][i]["Event"]["id"]
            dateEvent = response["response"][i]["Event"]["date"]
            infoEvent = response["response"][i]["Event"]["info"]
            timestampUpdate = datetime.fromtimestamp(int(response["response"][i]["Event"]["timestamp"]))
            isPublished = response["response"][i]["Event"]["published"]
            creatorOrgName = response["response"][i]["Event"]["Orgc"]["name"]

            print(idEvent)
            print(dateEvent)
            print(infoEvent)
            print(timestampUpdate)
            print(isPublished)
            print(creatorOrgName)
            print("__________________________________________________________")'''

            eventArray[i].prettyPrint()
            i += 1
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
    # TODO Scheduler de 2mins
    # https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
    # TODO Vérifier si l'event est published
    # TODO Différencier le cas update du cas création (avec timestamp/date de création)
    # TODO Cas ou rien n'est publié pendant 1/2/3h
    # # Create a tweet
    # api.update_status("This is a test")
