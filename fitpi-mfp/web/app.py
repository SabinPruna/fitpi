from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient, TEXT

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from configparser import ConfigParser

from datetime import datetime, timezone, timedelta
import requests

import json
import myfitnesspal
from helpers import time_helper, refresh_helper
from domain import MfpModel


def generate_return_dict(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson


config = ConfigParser()
config.read('config.ini')

client = MongoClient("mongodb://db:27017")
db = client.MFPServiceDB
mfp_db = db["MFP"]

username = config.get('config', 'mfp_username')
password = config.get('config', 'mfp_password')

client = myfitnesspal.Client(username, password)

# day = client.get_date(2019, 5, 29)
# stuff = mfp_db.find({'date': '2019-05-29'})[0]
# model = MfpModel.mfp_model_from_dict(stuff)



application = Flask(__name__)
api = Api(application)

scheduler = BackgroundScheduler(daemon=True, standalone=True) #, {'apscheduler.timezone': 'Europe/Bucharest'}
scheduler.start()

# @scheduler.scheduled_job('interval', minutes=30)
# refresh_helper.store_mfp(application, mfp_db, username, password) 



class StatsDateResource(Resource):
    def get(self, date):
        if mfp_db.find({'date': date}).count() == 0:
            refresh_helper.store_mfp_with_date(application, mfp_db, username, password, date) 
            stats = mfp_db.find({'date': date})[0]
        else:
            stats = mfp_db.find({'date': date})[0]

        del stats["_id"]
        return jsonify(stats) 

    def post(self, date):
        posted_data = request.get_json()

        mfp_db.update({
            'date': date
        }, posted_data
        )

        return jsonify(generate_return_dict(200, "Stats of day saved succesfully"))

class AllStatsResource(Resource):
    def get(self):
        data =[]
        for step_record in mfp_db.find({}).sort('date', -1):
            del step_record["_id"]
            data.append(step_record)
        
        return jsonify(data) 

    def post(self):
        posted_data = request.get_json()
        
        for data in posted_data:
             mfp_db.update({
                'date': data['date']
                 },  data)

        return jsonify(generate_return_dict(200, "Steps saved succesfully"))

class StreakResource(Resource):
    def get(self):
        data =[]

        for step_record in mfp_db.find({}, {"date": 1}).sort('date', -1):
            del step_record["_id"]
            data.append(int(step_record["date"].replace('-', '')))
        
        current = int(time_helper.get_local_date().replace('-', ''))
       
        while current != data[0]:
           data.pop(0) 

        data.pop(0)

        counter = 1
        for date_entry in data:
            if current - date_entry == 1:
                counter = counter + 1
                current = date_entry 
            else:
                break
            
        json_returned = {}
        json_returned["streak"] = counter

        return jsonify(json_returned) 

class FitbitAllMealsResource(Resource):
    def get(self):
        data = []
        records = []

        for mfp_record in mfp_db.find({}, {"date": 1, "calories": 1}).sort('date', -1):
            del mfp_record["_id"]
            data.append(int(mfp_record["date"].replace('-', '')))
            records.append(mfp_record)
        
        current = int(time_helper.get_local_date().replace('-', ''))
       
        while current != data[0]:
           data.pop(0)
           records.pop(0) 

        
        return jsonify(records) 

class FitbitMealResource(Resource):
    def get(self, date):

        record = mfp_db.find({"date": date}, {"date": 1, "calories": 1, "carbohydrates": 1, "fat": 1, "protein": 1, "sugar": 1})[0]
        del record["_id"]       
        return jsonify(record) 


api.add_resource(StreakResource, '/streak')
api.add_resource(AllStatsResource, '/allstats')
api.add_resource(StatsDateResource, '/stats/<string:date>')
api.add_resource(FitbitAllMealsResource, '/fitbitstats')
api.add_resource(FitbitMealResource, '/fitbitstats/<string:date>')

if __name__=="__main__":
    refresh_helper.store_mfp(application, mfp_db, username, password) 
    scheduler.add_job(refresh_helper.store_mfp, 'interval',[application, mfp_db, username, password] , id='refresh_helper.store_mfp', minutes=30)
    application.run(host='0.0.0.0', port=5000)