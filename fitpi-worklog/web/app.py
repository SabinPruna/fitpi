from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient, TEXT

from datetime import datetime, timezone, timedelta

import json


def generate_return_dict(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

client = MongoClient("mongodb://db:27017")
db = client.WorklogDB
log_db  = db["Logs"]

application = Flask(__name__)
api = Api(application)


class AddLog(Resource):
    def post(self, month, date, start, end, duration):
        #posted_data = request.get_json()
        data = {

        }

        data["month"] = month
        data["date"] = date
        data["start"] = start
        data["end"] = end
        data["duration"] = duration


        log_db.insert( data )

        return jsonify(generate_return_dict(200, "Log saved succesfully"))

class EditLog(Resource):
    def post(self, date):
        posted_data = request.get_json()

        log_db.update({'date': date}, posted_data)

        return jsonify(generate_return_dict(200, "Log edited succesfully"))

class RemoveLog(Resource):
    def post(self, date):
        posted_data = request.get_json()

        log_db.delete_one({'date': date})

        return jsonify(generate_return_dict(200, "Budget removed succesfully"))
        
class ListLogs(Resource):
    def get(self, month):
        
        logs = list(log_db.find({'month': month}))
        for log in logs:
            del log["_id"]

        return jsonify(logs)

class ListAllLogs(Resource):
    def get(self):
        
        logs = list(log_db.find({}).sort('date', -1))
        for log in logs:
            del log["_id"]

        return jsonify(logs)

class ListLogsFitbit(Resource):
    def get(self, month):

        logs = list(log_db.find({'month': month}))
        for log in logs:
            del log["_id"]

        return jsonify(logs)

        
api.add_resource(ListAllLogs, '/list')
api.add_resource(ListLogs, '/list/<string:month>')
api.add_resource(AddLog, '/addlog/<string:month>/<string:date>/<string:start>/<string:end>/<string:duration>')
api.add_resource(EditLog, '/editlog/<string:date>')
api.add_resource(RemoveLog, '/removelog/<string:date>')
api.add_resource(ListLogsFitbit, '/listfitbit/<string:month>')

if __name__=="__main__":
    application.run(host='0.0.0.0', port=5000)