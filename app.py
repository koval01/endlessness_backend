import logging

from flask import Flask, jsonify, g, Response, request
from flask_restful import Resource, Api
from flask_cors import CORS

from instaloader import Instaloader
from utils import PostProcess

from requests import get
from time import time

from cryptography.fernet import Fernet

app = Flask(__name__)
api = Api(app)
CORS(app)

instagram_load = Instaloader()
instagram_load.login("develop_account_kdv", "tiwjyg-9renva-jadwaV")

enc_key = b'r73QFT58DEGZIpGLUHW319V_brwT1pqMVcKa7cNDj_A='


class Status(Resource):
    @staticmethod
    def get() -> Response:
        return jsonify({'run': True})


class Image(Resource):
    @staticmethod
    def get() -> Response:
        url = request.args["l"]
        salt_link = Fernet(enc_key)
        link_get = eval(salt_link.decrypt(str.encode(str(url))).decode('utf-8'))

        if (link_get["time"] + 60) > time():
            r = get(
                link_get["url"], stream=True,
                headers={'user-agent': request.headers.get('user-agent')}
            )
            return Response(r.iter_content(chunk_size=10 * 1024),
                            content_type=r.headers['Content-Type'])


class Random(Resource):
    @staticmethod
    def get() -> Response:
        g.start = time()
        posts = []

        try:
            feed = instagram_load.get_explore_posts()
            for post in feed:
                posts.append({
                    "img_link": PostProcess.encoder({"url": post.url, "time": time()}, enc_key),
                    "likes_count": PostProcess.number_formatter(int(post.likes)),
                    "shortcode": post.shortcode,
                    "caption": PostProcess.clean_caption(post.caption),
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
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run()
