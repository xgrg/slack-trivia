import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pandas as pd
import settings
from glob import glob
import random
import os.path as op
import json
from tornado.options import define, options
import logging as log
import argparse
from datetime import datetime

class My404Handler(tornado.web.RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self.set_status(404)
        self.redirect('/')


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")



class PostHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        s = j = json.dumps({ k: self.get_argument(k) for k in self.request.arguments })
        j = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*It's 80 degrees right now. %s*"%s
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Partly cloudy today and tomorrow"
                    }
                }
            ]
        }
        self.write(json.dumps(j))

        #wd = self.get_argument('pipeline', None)
        #self.write('Found %s !'%wd)

class MainHandler(BaseHandler):
    def get(self):
        j = json.dumps({ k: self.get_argument(k) for k in self.request.arguments })
        self.write('Found %s!'%j)

class Application(tornado.web.Application):
    def __init__(self, args):

        handlers = [
            (r"/", MainHandler),
            (r"/post/", PostHandler),]


        s = {
            "autoreload": True,
            "template_path": settings.TEMPLATE_PATH,
            "static_path": settings.STATIC_PATH,
            "debug": settings.DEBUG,
            "cookie_secret": settings.COOKIE_SECRET,
        }
        tornado.web.Application.__init__(self, handlers,
            default_handler_class=My404Handler, autoescape=None, **s)


def main(args):
    http_server = tornado.httpserver.HTTPServer(Application(args))
    http_server.listen(args.port)

    t = tornado.ioloop.IOLoop.instance()
    return http_server, t

def create_parser():
    parser = argparse.ArgumentParser(description='sample argument')
    parser.add_argument('--port', required=False, default=8890)
    return parser



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    server, t = main(args)
    t.start()
