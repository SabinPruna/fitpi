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