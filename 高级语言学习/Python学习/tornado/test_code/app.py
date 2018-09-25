# -*- coding: utf-8 -*-
# Tornado Server Test Code

from tornado.web import RequestHandler, Application, RedirectHandler, StaticFileHandler
from tornado.ioloop import IOLoop
import json
import os

class Constant(object):
    '''Here is the constant object and value.'''

    @staticmethod
    def settings():
        return dict(
            cookie_secret =   "HEREISTHESECRETVALUE",
            login_url     =   "/login"
        )

class HelloHandler(RequestHandler):

    def get(self):
        self.write({"data":"hello world", "code":0, "message":"success."})

class DictHandler(RequestHandler):
    def get(self):
        try:
            data_keys = self.request.query_arguments.keys()
            data = {k:self.get_query_argument(k) for k in data_keys}
            data = dict(data=data, code=0, messgae="success.")
        except Exception:
            data = dict(code=1, message="failed.")
        self.write(data)

    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            data = dict(data=data, code=0, message="success.")
        except Exception as e:
            data = {"message":"failed Err:{}".format(e), "code":1}
        self.write(data)

class RestfulHandler(RequestHandler):

    def get(self, rest_id):
        self.write("This is {} rest.".format(rest_id))

def make_app():
    return Application([
        (r'/redirect_hello', RedirectHandler, dict(url=r'/hello')),                     # Here is a redirect handler.
        (r'/hello', HelloHandler),                                                      # Here is a normal get handler.
        (r'/dict', DictHandler),                                                        # Here is a handler to translate query/body arguments.
        (r'/rest/([0-9]+)', RestfulHandler),                                            # Here is a restful handler.
        (r'/pic/(.*)', StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "static"))),  # Here is a picture handler.
        (r'/photo/(.*)', RedirectHandler, dict(url=r'/pic/{0}'))                        # Here is a redirect handler with arguments.
    ], *Constant.settings())

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()