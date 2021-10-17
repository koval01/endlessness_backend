import logging

from flask import Flask, jsonify, g, Response
from flask_restful import Resource, Api
from flask_cors import CORS

from instaloader import Instaloader
from utils import PostProcess

from time import time

app = Flask(__name__)
api = Api(app)
CORS(app)

instagram_load = Instaloader()
instagram_load.login("develop_account_kdv", "tiwjyg-9renva-jadwaV")


class Status(Resource):
    @staticmethod
    def get() -> Response:
        return jsonify({'run': True})


class Random(Resource):
    @staticmethod
    def get() -> Response:
        g.start = time()
        posts = []

        try:
            feed = instagram_load.get_explore_posts()
            for post in feed:
                posts.append({
                    "img_link": post.url,
                    "likes_count": PostProcess.number_formatter(int(post.likes)),
                    "shortcode": post.shortcode,
                    "caption": post.caption,
                })
                if len(posts) >= 9:
                    break
        except Exception as e:
            logging.error(e)

        return jsonify({
            "success": len(posts) != 0,
            "time": round(time() - g.start, 3),
            "posts": posts,
            "count": len(posts),
        })


api.add_resource(Status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()
