import time

import schedule

from tweet import getAPITweepy, tweetEvents, weeklyTweet
from utils import TIME_REQUEST

if __name__ == '__main__':
    api = getAPITweepy()
    tweetEvents(api)

    schedule.every(int(TIME_REQUEST)).minutes.do(tweetEvents, api)
    schedule.every().sunday.at("12:00").do(weeklyTweet, api)

    while 1:
        schedule.run_pending()
        time.sleep(1)
