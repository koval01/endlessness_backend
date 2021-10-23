import logging
import instaloader
import os
import threading

from flask import Flask, jsonify, g, Response, request
from flask_restful import Resource, Api
from flask_cors import CORS
from utils import PostProcess

from requests import get
from time import time

from random import shuffle

from cryptography.fernet import Fernet

app = Flask(__name__)
api = Api(app)
CORS(app)

enc_key = bytes(os.environ.get("ENC_KEY"), 'utf-8')

instagram_load = instaloader.Instaloader()
instagram_load.login(
    os.environ.get("IG_LOGIN"),
    os.environ.get("IG_PASSWORD"),
)
feed = instagram_load.get_explore_posts()
local_feed = []


def parser() -> None:
    global local_feed
    print("Parser started!")
    for post in feed:
        local_feed.append({
            "img_link": PostProcess.encoder({"url": post.url, "time": time()}, enc_key),
            "shortcode": post.shortcode,
        })


class Status(Resource):
    @staticmethod
    def get() -> Response:
        return jsonify({'run': True, "buff": len(local_feed)})


class Image(Resource):
    @staticmethod
    def get() -> Response:
        try:
            url = request.args["l"]
            salt_link = Fernet(enc_key)
            link_get = eval(salt_link.decrypt(str.encode(str(url))).decode('utf-8'))

            if (link_get["time"] + 35) > time():
                r = get(
                    link_get["url"], stream=True,
                    headers={'user-agent': request.headers.get('user-agent')}
                )
                return Response(r.iter_content(chunk_size=10 * 1024),
                                content_type=r.headers['Content-Type'])
        except Exception as e:
            logging.error("Error get image by enc key, details - %s" % e)
            return jsonify({"success": False})


class Random(Resource):
    @staticmethod
    def get() -> Response:
        try:
            global local_feed

            local_feed_ = local_feed[:]
            shuffle(local_feed_)
            posts = local_feed_[-15:]

            if len(local_feed) > 1500:
                local_feed = local_feed[-1500:]

            return jsonify({
                "success": len(posts) != 0,
                "posts": posts,
                "count": len(posts),
            })
        except Exception as e:
            logging.error("Error get random posts, details - %s" % e)
            return jsonify({"success": False})


api.add_resource(Status, '/')
api.add_resource(Random, '/random')
api.add_resource(Image, '/image')

threading.Thread(target=parser).start()
threading.Thread(target=app.run).start()
