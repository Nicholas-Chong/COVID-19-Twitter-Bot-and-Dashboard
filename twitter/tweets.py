'''----------------------------------------------------------------------------
Name:        Twitter Bot Tweets Config (tweets.py)
Purpose:     To setup a connection with the Twitter API, as well as create a
             function that sends out the tweet.

Author:      Nicholas Chong
Created:     2020-06-19 (YYYY/MM/DD)
----------------------------------------------------------------------------'''

import tweepy
import os
import logging

auth = tweepy.OAuthHandler(
    os.getenv('API_KEY'), 
    os.getenv('API_SECRET_KEY'),
)

auth.set_access_token(
    os.getenv('ACCESS_TOKEN'), 
    os.getenv('ACCESS_TOKEN_SECRET'),
)

api = tweepy.API(auth)

def daily_update(date, new_cases, total_cases, tests_completed):
    message = str(
    f'''
[{date}]
New Cases: {new_cases}
Tests Completed: {tests_completed}
% Positivity: {round(new_cases/tests_completed*100, 2)}
Total Cases: {total_cases}
#COVID19Toronto #COVID19Ontario #Coronavirus
Like and retweet to inform others!
http://www.ontariocovid-19.com
    '''
    )

    return api.update_status(message)
