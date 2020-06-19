import tweepy
import os

mode = 'DEPLOYED'
if mode =! 'DEPLOYED':
    import dotenv
    dotenv.load_dotenv()

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
Total Cases: {total_cases}
#COVID19Toronto #COVID19ON #COVID19Ontario #COVIDOntario #CoronavirusOntario #COVID19CA #CovidOntario #StopTheSpread
https://t.co/VWtEPaz0Ip
    '''
    )

    return api.update_status(message)
