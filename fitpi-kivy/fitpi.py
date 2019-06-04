from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.network.urlrequest import UrlRequest
import datetime
import json
import urllib
import requests


class FitpiDashboard(BoxLayout):
    steps            = NumericProperty()
    calories         = NumericProperty()
    distance         = NumericProperty()
    activeminutes    = NumericProperty()
    stairs           = NumericProperty()

    def send_tweet(self, steps, calories, distance, activeminutes, stairs):
        message= f'Steps: {steps}, Calories: {calories}, Distance: {distance}, Active minutes: {activeminutes}, Floors: {stairs} measured from Kivy'
        twitter_url = f'https://n3yuv37w9j.execute-api.eu-central-1.amazonaws.com/prod/FitPiTwitterLambda'


        message_json = f'{{"message": "Steps: {steps}, Calories: {calories}, Distance: {distance}, Active minutes: {activeminutes}, Floors: {stairs} measured from Kivy"}}'
        params = urllib.parse.urlencode({'@message': message_json})
        headers = {'Content-type': 'application/json',  'Accept': 'text/plain'}

        req_body=json.dumps({"queryStringParameters": message_json})

        request = UrlRequest(twitter_url, on_success=self.posted, req_body=req_body, req_headers=headers)
        print(request)


        other = f'https://n3yuv37w9j.execute-api.eu-central-1.amazonaws.com/prod/FitPiTwitterLambda?message={message}'
        request = UrlRequest(other, self.got_json_fitbit)
        print(request)
        data = {'message':message} 

  
        r = requests.post(url = twitter_url, data = data) 
        print(r)

    def posted(self):
        print("Posted")

    def refresh(self):
        fitbit_url = f'https://n3yuv37w9j.execute-api.eu-central-1.amazonaws.com/prod/fitbitactivities?date={datetime.datetime.now().strftime("%Y-%m-%d")}'
        request = UrlRequest(fitbit_url, self.got_json_fitbit)

    def got_json_fitbit(self,request,data):
        data = json.loads(data.decode()) if not isinstance(data,dict) else data 
        print(data)
        self.steps = data['summary']['steps']
        self.calories = data['summary']['calories']['total']
        self.distance = data['summary']['distance']
        self.activeminutes = data['summary']['activityLevels'][0]['minutes']
        self.stairs = data['summary']['elevation']

class FitpiApp(App):
    def build(self):
        return FitpiDashboard()


if __name__ == '__main__':
    FitpiApp().run()