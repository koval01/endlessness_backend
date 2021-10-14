from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from instaloader import Instaloader

app = Flask(__name__)
api = Api(app)
CORS(app)

instload = Instaloader()
instload.login("develop_account_kdv", "tiwjyg-9renva-jadwaV")


class status(Resource):
    def get(self) -> None:
        return jsonify({'run': True})

      
class Random(Resource):
    def get(self) -> None:
        feed = instload.get_explore_posts()
        posts = []
        for post in feed:
            posts.append({
                "img_link": post.url,
                "type_post": post.typename,
                "caption": post.caption,
                "likes_count": post.likes,
                "shortcode": post.shortcode,
                "id": post.mediaid,
            })
            if len(posts) > 10: break
        return jsonify(posts)


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()
