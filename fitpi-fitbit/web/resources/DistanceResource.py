class DistanceResource(Resource):
    def get(self):

        projection = '{"date": 1, "summary.distances.0.distance": 1}'
        distances = []

        for distance_record in fitbit_stats_db.find({}, {"date": 1, "summary.distances": 1}).sort('date', -1).limit(100):
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