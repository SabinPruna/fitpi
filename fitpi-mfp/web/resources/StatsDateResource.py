
class StatsDateResource(Resource):
    def get(self, date):
        if mfp_db.find({'date': date}).count() == 0:
            refresh_helper.store_mfp_with_date(application, mfp_db, username, password, date) 
            stats = mfp_db.find({'date': date})[0]
        else:
            stats = mfp_db.find({'date': date})[0]

        del stats["_id"]
        return jsonify(stats) 

    def post(self, date):
        posted_data = request.get_json()

        mfp_db.update({
            'date': date
        }, posted_data
        )

        return jsonify(generate_return_dict(200, "Stats of day saved succesfully"))
