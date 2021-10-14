from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

import instaloader

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self) -> None:
        return jsonify({'run': True})

      
class Random(Resource):
    def get(self) -> None:
        import random
        json_data = {"random": random.uniform(0.00000001, 0.001)}
        
        return jsonify(json_data)


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()
