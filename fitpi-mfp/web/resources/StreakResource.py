class StreakResource(Resource):
    def get(self):
        data =[]

        for step_record in mfp_db.find({}, {"date": 1}).sort('date', -1):
            del step_record["_id"]
            data.append(int(step_record["date"].replace('-', '')))
        
        current = int(time_helper.get_local_date().replace('-', ''))
       
        while current != data[0]:
           data.pop(0) 

        data.pop(0)

        counter = 1
        for date_entry in data:
            if current - date_entry == 1:
                counter = counter + 1
                current = date_entry 
            else:
                break
            
        json_returned = {}
        json_returned["streak"] = counter

        return jsonify(json_returned) 
