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

TIME_REQUEST = os.getenv('TIME_REQUEST')
WEEKLY_FILE_NAME = os.getenv('WEEKLY_FILE_NAME')


# Create an org to add it to the weekly file
def addOrg(data, name):
    data['Orgs'].append({
        'name': name,
        'nbEvent': 1
    })


# Test if an org already exist in the data
# Return if the org exist and the org if found
def testOrg(data, name):
    if len(data['Orgs']) > 0:
        for org in data['Orgs']:
            if org['name'] == name:
                return True, org
    return False, {}


# Update the number of event reported by an org
def updateOrg(orgExist, event, org, data):
    if orgExist:
        # if event.timestampUpdate == event.firstUpdate:
        org['nbEvent'] += 1
    else:
        addOrg(data, event.creatorOrgName)


# Sort a dict
def sortOrgDict(orgDict):
    return sorted(orgDict.items(), key=lambda item: item[1])


def deleteWeeklyFile():
    os.remove(WEEKLY_FILE_NAME)