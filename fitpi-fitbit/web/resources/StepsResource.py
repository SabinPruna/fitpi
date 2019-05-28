class StepsResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.steps": 1}'
        steps = []

        for step_record in fitbit_stats_db.find({}, {"date": 1, "summary.steps": 1}).sort('date', -1).limit(100):
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