# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# inisiasi object
app = Flask(__name__)
api = Api(app)
CORS(app)

# membuat class resource
class ContohResource(Resource):
    def get(self):
        response = {
            "msg": "Hello World, this is my first Restful"
        }
        return response

# setup resource
api.add_resource(ContohResource, "/api", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True)