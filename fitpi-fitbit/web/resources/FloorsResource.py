class FloorsResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.floors": 1}'
        floors = []

        for floor_record in fitbit_stats_db.find({}, {"date": 1, "summary.floors": 1}).sort('date', -1).limit(100):
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