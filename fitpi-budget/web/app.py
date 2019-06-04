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


def generate_return_dict(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

client = MongoClient("mongodb://localhost:27017")
db = client.BudgetDB
general_db = db["General"]
budget_db = db["Budget"]


general_db.insert({"wallet": 5000})

application = Flask(__name__)
api = Api(application)

scheduler = BackgroundScheduler(daemon=True, standalone=True) #, {'apscheduler.timezone': 'Europe/Bucharest'}
scheduler.start()

# api.add_resource(StreakResource, '/streak')

class AddBudget(Resource):
    def post(self):
        posted_data = request.get_json()

        budget_db.update({
        }, posted_data
        )

        return jsonify(generate_return_dict(200, "Budget saved succesfully"))

class EditBuget(Resource):
    def get(self, month):
        posted_data = request.get_json()

        budget_db.update({'month': month, 'name': posted_data["name"]}, posted_data)

        return jsonify(generate_return_dict(200, "Budget edited succesfully"))

class RemoveBudget(Resource):
    def post(self, month):
        posted_data = request.get_json()

        budget_db.delete_one({'name': posted_data["name"], 'month': month})

        return jsonify(generate_return_dict(200, "Budget removed succesfully"))

class AddTransaction(Resource):
    def get(self, month, budget):
        posted_data = request.get_json()
        
        budget_db.update({'month': month, 'name': budget}, {'$push': {'transactions': posted_data}} )


        return jsonify(generate_return_dict(200, "Transaction saved succesfully"))

class EditTransaction(Resource):
    def get(self, month, budget):
        posted_data = request.get_json()

        budget_db.update({'month': month, 'name': budget, 'transactions.name': posted_data["name"]}, {'$set': {'transactions.$': posted_data}} )


        return jsonify(generate_return_dict(200, "Transaction edited succesfully"))

class RemoveTransaction(Resource):
    def post(self, month, budget):
        posted_data = request.get_json()

        budget_db.update({'month': month, 'name': budget, 'transactions.name': posted_data["name"]}, {'$pull': {'transactions': posted_data}} )


        return jsonify(generate_return_dict(200, "Transaction removed succesfully"))

class ListBudgets(Resource):
    def get(self, month):
        
        budgets = list(budget_db.find({'month': month}))
        for budget in budgets:
            del budget["_id"]

        return jsonify(budgets)

class ListAllBudgets(Resource):
    def get(self):
        
        budgets = list(budget_db.find({}).sort('month', -1))
        for budget in budgets:
            del budget["_id"]

        return jsonify(budgets)

class ListBudgetsFitbit(Resource):
    def get(self, month):

        budgets_json_list = []

        budgets = list(budget_db.find({'month': month}, {'name': 1, 'transactions': 1}))
        for budget in budgets:
            del budget["_id"]
   

        for budget in budgets:
            transactions = list(budget["transactions"])
            sum = 0
            for trans in transactions:
                sum = sum + trans["amount"]
            
            budget_json = {}
            budget_json["name"] = budget["name"]
            budget_json["sum"] = sum
            budgets_json_list.append(budget_json)

        return jsonify(budgets_json_list)

class ListTransactionsFitbit(Resource):
    def get(self, month, budget):

        budget = budget_db.find({'month': month, "name": budget})[0]
    
        transactions = list(budget["transactions"])

        return jsonify(transactions)

api.add_resource(ListAllBudgets, '/list')
api.add_resource(ListBudgets, '/list/<string:month>')
api.add_resource(AddBudget, '/addbudget')
api.add_resource(EditBuget, '/editbudget/<string:month>')
api.add_resource(RemoveBudget, '/removebudget/<string:month>')

api.add_resource(AddTransaction, '/addtransaction/<string:month>/<string:budget>')
api.add_resource(EditTransaction, '/edittransaction/<string:month>/<string:budget>')
api.add_resource(RemoveTransaction, '/removetransaction/<string:month>/<string:budget>')

api.add_resource(ListBudgetsFitbit, '/listfitbit/<string:month>')
api.add_resource(ListTransactionsFitbit, '/listfitbittransaction/<string:month>/<string:budget>')

if __name__=="__main__":
    refresh_helper.create_monthly_budgets(application, budget_db) 
    scheduler.add_job(refresh_helper.create_monthly_budgets, 'interval',[application, budget_db] , id='refresh_helper.create_monthly_budgets', hours=10)
    application.run(host='0.0.0.0', port=5000)