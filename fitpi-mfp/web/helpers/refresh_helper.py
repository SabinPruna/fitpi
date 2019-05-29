import myfitnesspal
import json
from helpers import time_helper
import datetime


def store_mfp(application, db_client, user, password):
    with application.app_context():
       client = myfitnesspal.Client(user, password)
       numbers = time_helper.get_local_date_numbers()
       day = client.get_date(numbers[0], numbers[1], numbers[2])

       daily_stats = day.totals

       data = json.loads(json.dumps(daily_stats))
       
       weight = client.get_measurements('Weight', datetime.date(numbers[0], numbers[1], numbers[2]))
       value = list(weight.items())[0][-1]
       data["weight"] = json.dumps(value)
       data["date"] = time_helper.get_local_date()
       
       breakfast = day.meals[0]
       lunch = day.meals[1]
       dinner = day.meals[2]
       snacks = day.meals[3]
       
       totals = breakfast.totals
       entries = breakfast.entries
       
       breafast_json = {}
       breafast_json["totals"] = totals
       breafast_json["entries"] = []
       
       for entry in entries:
           breafast_json["entries"].append(entry.get_as_dict())
       
       data["breakfast"] = breafast_json
       
       
       totals = lunch.totals
       entries = lunch.entries
       
       lunch_json = {}
       lunch_json["totals"] = totals
       lunch_json["entries"] = []
       
       for entry in entries:
           lunch_json["entries"].append(entry.get_as_dict())
       
       data["lunch"] = lunch_json
       
       totals = dinner.totals
       entries = dinner.entries
       
       dinner_json = {}
       dinner_json["totals"] = totals
       dinner_json["entries"] = []
       
       for entry in entries:
           dinner_json["entries"].append(entry.get_as_dict())
       
       data["dinner"] = dinner_json
       
       totals = snacks.totals
       entries = snacks.entries
       
       snacks_json = {}
       snacks_json["totals"] = totals
       snacks_json["entries"] = []
       
       for entry in entries:
           snacks_json["entries"].append(entry.get_as_dict())
       
       data["snacks"] = snacks_json
       
       
       db_client.update({'date': f'{data["date"]}'}, data , upsert = True)
       
def store_mfp_with_date(application, db_client, user, password, date_given):
    with application.app_context():
       client = myfitnesspal.Client(user, password)
       numbers = date_given.split("-")
       day = client.get_date(numbers[0], numbers[1], numbers[2])

       daily_stats = day.totals

       data = json.loads(json.dumps(daily_stats))
       
       weight = client.get_measurements('Weight', datetime.date(int(numbers[0]), int(numbers[1]), int(numbers[2])))
       value = list(weight.items())[0][-1]
       data["weight"] = json.dumps(value)
       data["date"] = date_given
       
       breakfast = day.meals[0]
       lunch = day.meals[1]
       dinner = day.meals[2]
       snacks = day.meals[3]
       
       totals = breakfast.totals
       entries = breakfast.entries
       
       breafast_json = {}
       breafast_json["totals"] = totals
       breafast_json["entries"] = []
       
       for entry in entries:
           breafast_json["entries"].append(entry.get_as_dict())
       
       data["breakfast"] = breafast_json
       
       
       totals = lunch.totals
       entries = lunch.entries
       
       lunch_json = {}
       lunch_json["totals"] = totals
       lunch_json["entries"] = []
       
       for entry in entries:
           lunch_json["entries"].append(entry.get_as_dict())
       
       data["lunch"] = lunch_json
       
       totals = dinner.totals
       entries = dinner.entries
       
       dinner_json = {}
       dinner_json["totals"] = totals
       dinner_json["entries"] = []
       
       for entry in entries:
           dinner_json["entries"].append(entry.get_as_dict())
       
       data["dinner"] = dinner_json
       
       totals = snacks.totals
       entries = snacks.entries
       
       snacks_json = {}
       snacks_json["totals"] = totals
       snacks_json["entries"] = []
       
       for entry in entries:
           snacks_json["entries"].append(entry.get_as_dict())
       
       data["snacks"] = snacks_json
       
       db_client.update({'date': f'{data["date"]}'}, data , upsert = True)