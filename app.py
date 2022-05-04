# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# import library flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

# inisiasi object
app = Flask(__name__)
api = Api(app)
CORS(app)

# inisiasi variabel kosong bertipe dict
identitas = {}

# membuat class resource
class ContohResource(Resource):
    def get(self):
        # response = {
        #     "msg": "Hello World, this is my first Restful"
        # }
        return identitas

    def post(self):
        name = request.form["nama"]
        age = request.form["umur"]
        
        identitas["nama"] = name
        identitas["umur"] = age
        
        response = {
            "msg": "Data Berhasil Ditambahkan"
        }
        return response

# setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)