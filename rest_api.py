import json
from datetime import datetime

import httplib2

from event_misp import EventMisp
from utils import MISP_KEY, TIME_REQUEST, API_URL


# Prepare a http POST with headersP and bodyP to url
def httpPost(url, headersP, bodyP):
    http = httplib2.Http()
    bodyP = json.dumps(bodyP)
    content = http.request(url,
                           method="POST",
                           headers=headersP,
                           body=bodyP)[1]
    return content


# Get all events within a amount of time set in TIME_REQUEST
def getEvents():
    headers = {'Authorization': MISP_KEY, 'Accept': 'application/json', 'Content-type': 'application/json'}
    body = {"returnFormat": "json", "last": TIME_REQUEST + "m"}

    # Send the request
    result = httpPost(API_URL, headers, body)

    # Get the result
    response = json.loads(result)

    i = 0
    events = []
    print("__________________")
    # While we have a new event
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
            # No more event to process
            break
        except Exception as exp:
            exit(exp)

    # Return a list of event
    return events
