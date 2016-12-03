#!/usr/bin/env python

import time
from functools import partial
from typing import Callable

import numpy as np
from tornado.httpclient import AsyncHTTPClient, HTTPResponse, HTTPError
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application, RequestHandler, StaticFileHandler


async def probe_http(url: str) -> bool:
    httpclient = AsyncHTTPClient(connect_timeout=1, request_timeout=1)  # TODO: make this configurable
    start = time.time()
    try:
        response = await httpclient.fetch(url)  # type: HTTPResponse
    except HTTPError as error:
        return False
    except Exception as error:
        return False
    finally:
        delta = time.time() - start
        httpclient.close()

    return True


async def probe(url: str, learn: Callable[[bool], None]):
    res = await probe_http(url)
    learn(res)


# algorithm by Hienrich Hartmann
def learn(p_transition: float, data, res: bool):
    vec = data['vec']
    N = len(vec) - 1
    for p, _ in enumerate(vec):
        q = 1 - p/N if res else p/N
        vec[p] = q * ((1 - p_transition) * vec[p] + p_transition * (1 - vec[p]))

    # normalize
    vec /= sum(vec)
    data['vec'] = vec
    data['iteration'] += 1


class DataHandler(RequestHandler):
    def initialize(self, data):
        self.data = data

    def get(self):
        self.write({'vec': list(self.data['vec']), 'iteration': self.data['iteration'], 'stddev': np.std(self.data['vec'])})


def init(url: str, p_transition: float, probe_interval: int):
    data = {'vec': np.ones(101), 'iteration': 0}
    learn_func = partial(learn, p_transition, data)
    PeriodicCallback(partial(probe, url, learn_func), probe_interval).start()
    app = Application([
        (r'/data', DataHandler, dict(data=data)),
        (r'/(.*)', StaticFileHandler, dict(path='static', default_filename='index.html'))
    ],
    autoreload=True)
    app.listen(8888)


if __name__ == '__main__':
    # TODO: make this configurable via UI
    url = 'http://localhost:8881/test'
    init(url,
         p_transition=0.0001,
         probe_interval=200  # ms
         )
    IOLoop.current().start()
