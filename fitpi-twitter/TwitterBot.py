import json
import sys
import time
import requests
import datetime
from twython import Twython, TwythonError

#app keys to post on twitter @sabinpruna
apiKey = ''
apiSecret = ''
accessToken = ''
accessTokenSecret = ''

class TweeterBot:
    
    #initialize api to send tweets on instance construction
    def __init__(self):    
        self.api = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

    #given message from sensors in main.py , it will post a tweet @sabinpruna
    def send_tweet(self, data):
        try:
            tweet = data
            self.api.update_status(status = tweet)
            print("Tweeted:" + tweet)
        except TwythonError as error:
            #happens if current tweet is identical to last posted tweet
            #or too many requests to update were sent from same ip.
            print("Error:" + str(error))


def lambda_handler(event, context):
    print('Even is: ', event)
    
    bot = TweeterBot()
    message = str(event['queryStringParameters']['message'])
    message = message + " timestamp: " + str(datetime.datetime.now().strftime('%Y-%m-%d, %H:%M'))
    print('Message is: ', message)

    bot.send_tweet(message)

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
