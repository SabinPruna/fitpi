
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
