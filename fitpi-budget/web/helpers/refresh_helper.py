import myfitnesspal
import json
from helpers import time_helper
import datetime

def create_monthly_budgets(application, db_client):
    with application.app_context():
        current_month = time_helper.get_local_date_month()

        if db_client.find({'month': current_month}).count() == 0:  
            necessities_budget_json = {}
            necessities_budget_json["name"] = "Necessities"
            necessities_budget_json["budget"] = 1600
            necessities_budget_json["current"] = 0
            necessities_budget_json["month"] = current_month
            necessities_budget_json["transactions"] = []

            rent = {}
            rent["name"] = "Rent"
            rent["amount"] = 678
            rent["date"] = time_helper.get_local_date()
            necessities_budget_json["transactions"].append(rent)

            luxury_budget_json = {}
            luxury_budget_json["name"] = "Luxury"
            luxury_budget_json["budget"] = 750        
            luxury_budget_json["current"] = 0
            luxury_budget_json["month"] = current_month
            luxury_budget_json["transactions"] = []

            cinema = {}
            cinema["name"] = "Cinema"
            cinema["amount"] = 13.5
            cinema["date"] = time_helper.get_local_date()
            luxury_budget_json["transactions"].append(cinema)

            savings_budget_json = {}
            savings_budget_json["name"] = "Savings"
            savings_budget_json["budget"] = 500          
            savings_budget_json["current"] = 0
            savings_budget_json["month"] = current_month
            savings_budget_json["transactions"] = []

            db_client.insert(necessities_budget_json)
            db_client.insert(luxury_budget_json)
            db_client.insert(savings_budget_json)

def calculate_spending(application, db_client):
    with application.app_context():
        #db_client.update({}, {'$set': {'current':{ '$sum': '$transactions.amount'} }})
        print("updated")

    