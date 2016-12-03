#!/usr/bin/env python3

from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from random import random


class MisbehavingRequestHandler(RequestHandler):
    def initialize(self, p):
        self.p = p

    def get(self):
        if random() > self.p:
            return
        else:
            self.set_status(500)



if __name__ == '__main__':
    app = Application([
        (r'/test', MisbehavingRequestHandler, {'p': 0.80}),
        (r'/(.*)', StaticFileHandler, {'path': 'static', 'default_filename': 'index.html'})
    ],
    autoreload=True)
    app.listen(8881)
    IOLoop.current().start()