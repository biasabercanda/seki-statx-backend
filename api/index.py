from flask import Flask, Response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from api.helper_functions import get_data, date, clean_data

app = Flask(__name__)
api = Api(app)
CORS(app)


@app.route('/')
def root():
    return jsonify({
        "name": "SEKI StatX API",
        "status": "online",
        "usage": "GET /<table_id> (e.g. /TABEL1_1)",
        "source": "Bank Indonesia SEKI"
    })


class seki(Resource):
    def get(self, table_id):
        try:
            f = get_data(table_id.upper())
            sheets = f.sheet_names
            if not sheets:
                return {"error": f"No sheets found for table '{table_id}'"}, 404
            df = f.parse(len(sheets) - 1)
            cleaned_data = clean_data(df)
            res = cleaned_data.to_json(orient='split')
            return Response(res, mimetype='application/json')
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": f"Failed to process table '{table_id}': {str(e)}"}, 500


class forecast(Resource):
    def post(self):
        return {"message": "Forecast endpoint placeholder"}, 200


api.add_resource(seki, '/<string:table_id>')
api.add_resource(forecast, '/forecast')

if __name__ == '__main__':
    app.run(debug=True)
