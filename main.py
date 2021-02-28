import json

import tweepy
import httplib2
import schedule
import time
import os
from EventMisp import EventMisp, printEvents
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

TIME_REQUEST = os.getenv('TIME_REQUEST')


def httpPost(url, headersP, bodyP):
    http = httplib2.Http()
    bodyP = json.dumps(bodyP)
    content = http.request(url,
                           method="POST",
                           headers=headersP,
                           body=bodyP)[1]
    return content


def getEvents():
    headers = {'Authorization': MISP_KEY, 'Accept': 'application/json', 'Content-type': 'application/json'}
    body = {"returnFormat": "json", "last": TIME_REQUEST + "m"}
    result = httpPost(API_URL, headers, body)
    response = json.loads(result)
    i = 0
    events = []
    print("__________________")
    while True:
        try:
            events.append(EventMisp(response["response"][i]["Event"]["id"],
                                    datetime.fromtimestamp(
                                        int(response["response"][i]["Event"]["Attribute"][0]["timestamp"])),
                                    response["response"][i]["Event"]["info"],
                                    datetime.fromtimestamp(int(response["response"][i]["Event"]["timestamp"])),
                                    response["response"][i]["Event"]["published"],
                                    response["response"][i]["Event"]["Orgc"]["name"]))

            i += 1
        except IndexError:
            break
        except Exception as exp:
            exit(exp)
    return events


def getTweetPrefix(e):
    if e.timestampUpdate == e.firstUpdate:
        return ""
    else:
        return "Update! \n"


def getTweetSuffix(e):
    if (len(e.infoEvent) + len(e.creatorOrgName) + len(str(e.firstUpdate)) + 25) < 280:
        return f", has been attacked : {e.infoEvent}"
    elif "phishing" in e.infoEvent:
        return f", has been targeted by a phishing campaign"
    elif "malware" in e.infoEvent:
        return f", has been targeted by a malware attack"
    else:
        return f".\nNo more information could be given"


def addOrg(data, name):
    data['Orgs'].append({
        'name': name,
        'nbEvent': 1
    })


def testOrg(data, name, orgIfExist):
    if len(data['Orgs']) > 0:
        for org in data['Orgs']:
            if org['name'] == name:
                return True, org
    return False, {}


def updateOrg(orgExist, event, org, data):
    if orgExist:
        # if event.timestampUpdate == event.firstUpdate:
        org['nbEvent'] += 1
    else:
        addOrg(data, event.creatorOrgName)


def tweetEvents(apiTweet):
    print("___Tweet events___")
    events = getEvents()
    printEvents(events)
    # Create a tweet
    org = {}
    for e in events:
        if e.isPublished:

            with open('weekly.json') as json_file:
                weeklyData = json.load(json_file)
            orgExist, org = testOrg(weeklyData, e.creatorOrgName, org)
            updateOrg(orgExist, e, org, weeklyData)
            with open('weekly.json', 'w') as outfile:
                json.dump(weeklyData, outfile, ensure_ascii=False)

            try:
                apiTweet.update_status(
                    f"{getTweetPrefix(e)} {e.creatorOrgName}, the {e.firstUpdate} {getTweetSuffix(e)}")
            except tweepy.error.TweepError as twperr:
                print(twperr.reason)
                pass


def sortOrgDict(orgDict):
    return sorted(orgDict.items(), key=lambda item: item[1])


def weeklyTweet(apiTweet):
    print("___Weekly tweet___")

    with open('weekly.json') as json_file:
        weeklyData = json.load(json_file)
        tabOrg = {}
        for org in weeklyData['Orgs']:
            tabOrg[org['name']] = org['nbEvent']

    tabOrg = sortOrgDict(tabOrg)
    tabOrg.reverse()

    try:
        apiTweet.update_status("Weekly report : \n\n"
                               "The company that reported the most attacks is : " + tabOrg[0][0] + "\nWith : " + str(
                                tabOrg[0][1]) + " event" + ("s" if tabOrg[0][1] > 1 else "") + " reported this week!")

    except tweepy.error.TweepError as twperr:
        print(twperr.reason)
        pass


if __name__ == '__main__':
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

    # Create API object
    api = tweepy.API(auth)

    tweetEvents(api)
    # schedule.every(int(TIME_REQUEST)).minutes.do(tweetEvents, api)
    # schedule.every(2).seconds.do(weeklyTweet, api)
    schedule.every().weeks.at("10:30").do(weeklyTweet, api)

    while 1:
        schedule.run_pending()
        time.sleep(1)
