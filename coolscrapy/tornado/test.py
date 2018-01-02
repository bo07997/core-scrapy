import textwrap
from scrapy import cmdline
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import redis
from tornado.options import define, options
import logging
import time
import json
import threading
import os
from time import ctime,sleep
define("port", default=8000, help="run on the given port", type=int)
Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
_log = logging.getLogger(__name__)


class searchHandler(tornado.web.RequestHandler):

    def craw(self, search_name, p):
        cmd = 'scrapy crawl mySpider_search -a p={0} -a search_book_name={1}'.format(p, search_name)
        try:
            cmdline.execute(cmd.split())
        except Exception as err:
            _log.error(err)
            return
    def get(self):
        search_name = self.get_argument('name', '')
        p = self.get_argument('p', '1')
        thread_craw = threading.Thread(self.craw(search_name, p))
        thread_craw.setDaemon(True)
        thread_craw.start()
        start_time = time.time()
        while(True):
            if Redis.exists(search_name + "-" + p):
                value = json.loads(Redis.get(search_name + "-" + p))
                self.render("search_result.html", books=value)
                break
            else:
                time.sleep(0.5)
            if time.time() - start_time > 25:
                _log.info("Oh NO, time out!")
                break



class ChapterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class MyFile(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/search", searchHandler),
            (r"/chapter", ChapterHandler),
            (r"/", IndexHandler),
        ]


        settings = {
            'template_path': 'templates',
            "static_path": os.path.join(os.path.dirname(__file__), "templates"),

        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()