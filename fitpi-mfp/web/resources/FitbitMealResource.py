class FitbitMealResource(Resource):
    def get(self, date):

        record = mfp_db.find({"date": date}, {"date": 1, "calories": 1, "carbohydrates": 1, "fat": 1, "protein": 1, "sugar": 1})[0]
        del record["_id"]       
        return jsonify(record) 

