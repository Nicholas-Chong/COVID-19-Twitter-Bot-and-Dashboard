'''----------------------------------------------------------------------------
Name:        Twitter Bot (bot.py)
Purpose:     A script that sends out a tweet containing general coronavirus 
             statistics from the Government of Ontario. Script is called 
             through heroku scheduler at 11:00AM every day.

Author:      Nicholas Chong
Created:     2020-06-19 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import urllib.request
import pprint
import json
from . import tweets 
import logging
from datetime import datetime

def main(today):
    logging.info('Sending daily update tweet')

    if str(today.date) != str(datetime.today().date()):
        return logging.error('The record date does not match todays date')

    # Send out the daily update tweet
    tweets.daily_update(
        today.date, 
        today.net_new_cases, 
        today.total_cases,
        today.net_new_tests,
    )

    logging.info('Tweet sent')


if __name__ == '__main__':
    main()
