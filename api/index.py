from flask import Flask
from flask_restful import Resource, Api
from api.helper_functions import get_data, date, clean_data
from io import BytesIO
import pandas as pd
import xlrd


app = Flask(__name__)
api = Api(app)

class seki(Resource):
    def get(self,table_id):
        f = get_data(table_id.upper())
        sheets = f.sheet_names
        df = f.parse(len(sheets)-1)
        cleaned_data = clean_data(df)
        res = cleaned_data.to_json(orient ='split')
        return res

api.add_resource(seki, '/<string:table_id>')

if __name__ == '__main__':
    app.run(debug=True)
