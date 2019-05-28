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


def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson
