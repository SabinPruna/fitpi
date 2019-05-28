from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient, TEXT

import bcrypt

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from configparser import ConfigParser

from datetime import datetime, timezone, timedelta
import requests

import json


from helpers import time_helper
from domain import Stats, Activity

#import web.time_helper as time_helper
#import web.domain.Stats as stats

config = ConfigParser()
config.read('config.ini')

application = Flask(__name__)
api = Api(application)

client = MongoClient("mongodb://db:27017")
db = client.FitbitServiceDB
fitbit_stats_db = db["Fitbit"]
fitbit_activity_db = db["Activities"]

fitbit_stats_db.create_index('date')
fitbit_activity_db.create_index('date')

# initialize scheduler with your preferred timezone
scheduler = BackgroundScheduler(daemon=True, standalone=True) #, {'apscheduler.timezone': 'Europe/Bucharest'}
scheduler.start()

@scheduler.scheduled_job('interval', minutes=10)
def store_activites():
    with application.app_context():
        fitbit_secret_token = config.get('config', 'fitbit_secret_token')
        stats_query_string = f'https://api.fitbit.com/1/user/-/activities/date/{time_helper.get_local_date()}.json'
        secret_header = {'Authorization': 'Bearer {}'.format(fitbit_secret_token)}
        response = requests.get(stats_query_string, headers=secret_header)    
         
        weight_query_string = f'https://api.fitbit.com/1/user/-/body/log/weight/goal.json'
        weight_response = requests.get(weight_query_string, headers=secret_header)

        sleep_goal_query_string = f'https://api.fitbit.com/1/user/-/sleep/goal.json'
        sleep_goal_response = requests.get(sleep_goal_query_string, headers=secret_header)

        sleep_query_string = f'https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate={time_helper.get_local_date()}&sort=desc&offset=0&limit=1'
        sleep_response = requests.get(sleep_query_string, headers=secret_header)

        #data = response.json()
        json_data = json.loads(response.text)
        weight_json_data = json.loads(weight_response.text)
        sleep_goal_json_data = json.loads(sleep_goal_response.text)
        sleep_json_data = json.loads(sleep_response.text)

        json_data['date'] = time_helper.get_local_date()
        json_data['startWeight'] = weight_json_data['goal']['startWeight']
        json_data['weight'] = weight_json_data['goal']['weight']
        json_data['sleepGoalMinutes'] = sleep_goal_json_data['goal']['minDuration']
        json_data['sleepMinutes'] = sleep_json_data['sleep'][0]['timeInBed']
        json_data['sleepMinutesAwake'] = sleep_json_data['sleep'][0]['minutesAwake']


        fitbit_stats_db.update({'date': f'{json_data["date"]}'}, json_data , upsert = True)

        result = Stats.stats_from_dict(json_data)

        activity_query_string = f'https://api.fitbit.com/1/user/-/activities/list.json?afterDate={time_helper.get_local_date()}&sort=desc&offset=0&limit=1'
        secret_header = {'Authorization': 'Bearer {}'.format(fitbit_secret_token)}
        
        response = requests.get(activity_query_string, headers=secret_header)
       
        json_data = json.loads(response.text)
        json_data['date'] = time_helper.get_local_date()

        if fitbit_activity_db.find({'date': f'{json_data["date"]}'}).count():
                fitbit_activity_db.update({'date': f'{json_data["date"]}'}, json_data)
        else:
                fitbit_activity_db.insert(json_data)

        result = Activity.activity_from_dict(json_data)
        print(result)
        
def store_activites_with_date(date):
    with application.app_context():
        fitbit_secret_token = config.get('config', 'fitbit_secret_token')
        stats_query_string = f'https://api.fitbit.com/1/user/-/activities/date/{date}.json'
        secret_header = {'Authorization': 'Bearer {}'.format(fitbit_secret_token)}
        response = requests.get(stats_query_string, headers=secret_header)    
         
        weight_query_string = f'https://api.fitbit.com/1/user/-/body/log/weight/goal.json'
        weight_response = requests.get(weight_query_string, headers=secret_header)

        sleep_goal_query_string = f'https://api.fitbit.com/1/user/-/sleep/goal.json'
        sleep_goal_response = requests.get(sleep_goal_query_string, headers=secret_header)

        sleep_query_string = f'https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate={date}&sort=desc&offset=0&limit=1'
        sleep_response = requests.get(sleep_query_string, headers=secret_header)

        #data = response.json()
        json_data = json.loads(response.text)
        weight_json_data = json.loads(weight_response.text)
        sleep_goal_json_data = json.loads(sleep_goal_response.text)
        sleep_json_data = json.loads(sleep_response.text)

        json_data['date'] = date
        json_data['startWeight'] = weight_json_data['goal']['startWeight']
        json_data['weight'] = weight_json_data['goal']['weight']
        json_data['sleepGoalMinutes'] = sleep_goal_json_data['goal']['minDuration']
        json_data['sleepMinutes'] = sleep_json_data['sleep'][0]['timeInBed']
        json_data['sleepMinutesAwake'] = sleep_json_data['sleep'][0]['minutesAwake']


        fitbit_stats_db.update({'date': f'{json_data["date"]}'}, json_data , upsert = True)

        result = Stats.stats_from_dict(json_data)

        activity_query_string = f'https://api.fitbit.com/1/user/-/activities/list.json?afterDate={date}&sort=desc&offset=0&limit=1'
        secret_header = {'Authorization': 'Bearer {}'.format(fitbit_secret_token)}
        
        response = requests.get(activity_query_string, headers=secret_header)
       
        json_data = json.loads(response.text)
        json_data['date'] = date

        if fitbit_activity_db.find({'date': f'{json_data["date"]}'}).count():
                fitbit_activity_db.update({'date': f'{json_data["date"]}'}, json_data)
        else:
                fitbit_activity_db.insert(json_data)

        result = Activity.activity_from_dict(json_data)

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))


def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson



class StatsResource(Resource):
    def get(self, date):
        parsed_date = datetime.strptime(date, '%Y-%m-%d')

        if fitbit_stats_db.find({'date': date}).count() == 0:
            store_activites_with_date(date)
            stats = fitbit_stats_db.find({'date': date})[0]
        else:
            stats = fitbit_stats_db.find({'date': date})[0]

        del stats["_id"]
        return jsonify(stats) 

    def post(self):
        posted_data = request.get_json()

        fitbit_stats_db.update({
            'date': posted_data['date']
        }, posted_data
        )

        return jsonify(generateReturnDictionary(200, "Stats saved succesfully"))

class ActivitiesResource(Resource):
    def get(self, date):
        parsed_date = datetime.strptime(date, '%Y-%m-%d')

        if fitbit_activity_db.find({'date': date}).count() == 0:
            store_activites_with_date(date)
            activities = fitbit_activity_db.find({'date': date})[0]
        else:
            activities = fitbit_activity_db.find({'date': date})[0]

        del activities["_id"]
        return jsonify(activities) 

    def post(self):
        posted_data = request.get_json()

        fitbit_activity_db.update({
            'date': posted_data['date']
        }, posted_data
        )

        return jsonify(generateReturnDictionary(200, "Activities saved succesfully"))

class StepsResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.steps": 1}'
        steps = []

        for step_record in fitbit_stats_db.find({}, {"date": 1, "summary.steps": 1}).sort('date', -1):
            del step_record["_id"]
            steps.append(step_record)
        
        return jsonify(steps) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'summary.steps': int(data["summary"]["steps"])}})

        return jsonify(generateReturnDictionary(200, "Steps saved succesfully"))

class DistanceResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.distances.0.distance": 1}'
        distances = []

        for distance_record in fitbit_stats_db.find({}, {"date": 1, "summary.distances": 1}).sort('date', -1):
            del distance_record["_id"]
            distances.append(distance_record)
        
        return jsonify(distances) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, {'$set': {'summary.distances': data["summary"]["distances"]}})

        return jsonify(generateReturnDictionary(200, "Distances saved succesfully"))

class FloorsResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.floors": 1}'
        floors = []

        for floor_record in fitbit_stats_db.find({}, {"date": 1, "summary.floors": 1}).sort('date', -1):
            del floor_record["_id"]
            floors.append(floor_record)
        
        return jsonify(floors) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'summary.floors': int(data["summary"]["floors"])}})

        return jsonify(generateReturnDictionary(200, "Floors saved succesfully"))

class ActiveMinutesResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.lightlyActiveMinutes": 1, "summary.veryActiveMinutes": 1}'
        minutes = []

        for minutes_record in fitbit_stats_db.find({}, {"date": 1, "summary.lightlyActiveMinutes": 1, "summary.veryActiveMinutes": 1}).sort('date', -1):
            del minutes_record["_id"]
            minutes.append(minutes_record)
        
        return jsonify(minutes) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'summary.lightlyActiveMinutes': int(data["summary"]["lightlyActiveMinutes"]), 'summary.veryActiveMinutes': int(data["summary"]["veryActiveMinutes"])}})

        return jsonify(generateReturnDictionary(200, "Active Minutes saved succesfully"))

class SleepResource(Resource):
    def get(self):

        projection = '{"date": 1, "sleepMinutes": 1, "sleepMinutesAwake": 1}'
        sleep = []

        for sleep_record in fitbit_stats_db.find({}, {"date": 1, "sleepMinutes": 1, "sleepMinutesAwake": 1}).sort('date', -1):
            del sleep_record["_id"]
            sleep.append(sleep_record)
        
        return jsonify(sleep) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'sleepMinutes': int(data["sleepMinutes"]), 'sleepMinutesAwake': int(data["sleepMinutesAwake"])}})

        return jsonify(generateReturnDictionary(200, "Sleep saved succesfully"))

class WeightResource(Resource):
    def get(self):

        projection = '{"date": 1, "weight": 1, "startWeight": 1}'
        weight = []

        for weight_record in fitbit_stats_db.find({}, {"date": 1, "weight": 1, "startWeight": 1}).sort('date', -1):
            del weight_record["_id"]
            weight.append(weight_record)
        
        return jsonify(weight) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'weight': int(data["weight"]), 'startWeight': int(data["startWeight"])}})

        return jsonify(generateReturnDictionary(200, "Weight saved succesfully"))


class HeartRateResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.restingHeartRate": 1}'
        hr = []

        for step_record in fitbit_stats_db.find({}, {"date": 1, "summary.restingHeartRate": 1}).sort('date', -1):
            del step_record["_id"]
            hr.append(step_record)
        
        return jsonify(hr) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'summary.restingHeartRate': int(data["summary"]["restingHeartRate"])}})

        return jsonify(generateReturnDictionary(200, "Steps saved succesfully"))

class CaloriesResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.caloriesOut": 1}'
        calories = []

        for step_record in fitbit_stats_db.find({}, {"date": 1, "summary.caloriesOut": 1}).sort('date', -1):
            del step_record["_id"]
            calories.append(step_record)
        
        return jsonify(calories) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             fitbit_stats_db.update({
                'date': data['date']
                 }, 
                 {'$set': {'summary.caloriesOut': int(data["summary"]["caloriesOut"])}})

        return jsonify(generateReturnDictionary(200, "Steps saved succesfully"))

api.add_resource(StatsResource, '/stats/<string:date>', '/stats')
api.add_resource(ActivitiesResource, '/activities/<string:date>', '/activities')
api.add_resource(StepsResource, '/steps')
api.add_resource(DistanceResource, '/distance')
api.add_resource(FloorsResource, '/floors')
api.add_resource(ActiveMinutesResource, '/activeMinutes')
api.add_resource(SleepResource, '/sleep')
api.add_resource(WeightResource, '/weight')
api.add_resource(HeartRateResource, '/hr')
api.add_resource(CaloriesResource, '/calories')

if __name__=="__main__":
    store_activites()
    #scheduler.add_job(store_activites, 'cron', id='store_activities', minute=1)
    application.run(host='0.0.0.0', port='5000')

