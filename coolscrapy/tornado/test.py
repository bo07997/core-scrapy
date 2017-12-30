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
define("port", default=8000, help="run on the given port", type=int)
Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
_log = logging.getLogger(__name__)


class searchHandler(tornado.web.RequestHandler):

    def get(self):
        book_name = "斗破苍穹"
        crawler_name = 'mySpider_search'
        p = 1
        cmd = 'scrapy crawl mySpider_search -a p={0} -a search_book_name={1}'.format(p, book_name)
        cmdline.execute(cmd.split())
        start_time = time.time()
        OK = False
        while(time.time() - start_time < 100):
            if Redis.exists(book_name + p):
                OK = True
            else:
                time.sleep(0.5)
        if OK:
            self.render("index.html")
        else:
            print("Oh NO")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/search", searchHandler),
            (r"/wrap", WrapHandler),
            (r"/", IndexHandler)
        ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()