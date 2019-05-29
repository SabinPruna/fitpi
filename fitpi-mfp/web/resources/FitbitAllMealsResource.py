
class FitbitAllMealsResource(Resource):
    def get(self):
        data = []
        records = []

        for mfp_record in mfp_db.find({}, {"date": 1, "calories": 1}).sort('date', -1):
            del mfp_record["_id"]
            data.append(int(mfp_record["date"].replace('-', '')))
            records.append(mfp_record)
        
        current = int(time_helper.get_local_date().replace('-', ''))
       
        while current != data[0]:
           data.pop(0)
           records.pop(0) 
        data.pop(0)
        records.pop(0) 

        
        return jsonify(records) 
