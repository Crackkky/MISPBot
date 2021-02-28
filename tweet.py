import json

import tweepy

from event_misp import printEvents
from rest_api import getEvents
from utils import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_SECRET_TOKEN, testOrg, updateOrg, sortOrgDict, \
    WEEKLY_FILE_NAME, deleteWeeklyFile


# Return the Tweepy API to connect to twitter
def getAPITweepy():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

    # Create and return API object
    return tweepy.API(auth)


# Return the prefix of a tweet if one is needed
def getTweetPrefix(e):
    if e.timestampUpdate == e.firstUpdate:
        return ""
    else:
        return "Update! \n"


# Return the suffix of a tweet depending its size
def getTweetSuffix(e):
    if (len(e.infoEvent) + len(e.creatorOrgName) + len(str(e.firstUpdate)) + 25) < 280:
        return f", has been attacked : {e.infoEvent}"
    elif "phishing" in e.infoEvent:
        return f", has been targeted by a phishing campaign"
    elif "malware" in e.infoEvent:
        return f", has been targeted by a malware attack"
    else:
        return f".\nNo more information could be given"


# Tweet all events obtained from getEvents() and store data in weekly.json
def tweetEvents(apiTweet):
    print("___Tweet events___")
    events = getEvents()
    printEvents(events)
    org = {}

    for e in events:
        if e.isPublished:

            # Open the file and test if the org that published the event already exist
            with open(WEEKLY_FILE_NAME) as json_file:
                weeklyData = json.load(json_file)
            orgExist, org = testOrg(weeklyData, e.creatorOrgName)

            # If so, update its score, else add it and write the result in the file
            updateOrg(orgExist, e, org, weeklyData)
            with open(WEEKLY_FILE_NAME, 'w') as outfile:
                json.dump(weeklyData, outfile, ensure_ascii=False)

            # Tweet the event
            try:
                apiTweet.update_status(
                    f"{getTweetPrefix(e)} {e.creatorOrgName}, the {e.firstUpdate} {getTweetSuffix(e)}")
            except tweepy.error.TweepError as twperr:
                print(twperr.reason)


# Tweet the weekly report depending the weekly file
def weeklyTweet(apiTweet):
    print("___Weekly tweet___")

    # Open the file and create a dict of the data
    with open(WEEKLY_FILE_NAME) as json_file:
        weeklyData = json.load(json_file)
        tabOrg = {}
        for org in weeklyData['Orgs']:
            tabOrg[org['name']] = org['nbEvent']

    # Sort the dict
    tabOrg = sortOrgDict(tabOrg)
    tabOrg.reverse()

    # Tweet the result
    try:
        apiTweet.update_status("Weekly report : \n\n"
                               "The company that reported the most attacks is : " + tabOrg[0][0] + "\nWith : " + str(
                                tabOrg[0][1]) + " event" + ("s" if tabOrg[0][1] > 1 else "") + " reported this week!")

    except tweepy.error.TweepError as twperr:
        print(twperr.reason)

    deleteWeeklyFile()
