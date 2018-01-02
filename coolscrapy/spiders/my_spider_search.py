#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request

from scrapy.spiders import CrawlSpider, Rule, Spider
from coolscrapy.items import Book
import logging
import  json
import re
import redis
Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
_log = logging.getLogger(__name__)

class TobaccoSpider(Spider):
    """
    爬取本页面内容，然后再提取下一页链接生成新的Request标准做法
    另外还使用了图片下载管道
    """
    name = "mySpider_search"
    allowed_domains = ["baidu.com"]
    base_url = "http://zhannei.baidu.com/cse/search?s=5592277830829141693&entry=1&q="
    start_urls = []
    # start_urls = [
    #     base_url + "斗破苍穹"
    # ]

    def __init__(self, search_book_name=None, p=1, *args, **kwargs):
        if search_book_name is not None:
            self.start_urls = []
            self.start_urls.append(self.base_url + search_book_name + "&p=" + p)
            self.p = p
            self.search_book_name = search_book_name

    def parse(self, response):
        # 处理本页内容
        books = []
        for ind, each_row in enumerate(response.xpath('//*[@id="results"]/div[3]/div')):
            if ind == 0:
                continue
            book = Book()
            book['book_name'] = each_row.xpath("div[2]/h3/a/@title").extract_first()
            book['book_author'] = each_row.xpath("div[2]/div/p[1]/a/text()").extract_first()
            book['book_url'] = each_row.xpath("div[2]/h3/a/@href").extract_first()
            book['book_ins'] = each_row.xpath("div[2]/p/text()").extract_first()
            book['book_type'] = each_row.xpath("div[2]/div/p[2]/span[2]/text()").extract_first()
            book['book_word_count'] = each_row.xpath("div[2]/div/p[3]/span[2]/text()").extract_first()
            book['book_type'] = each_row.xpath("div[2]/div/p[2]/span[2]/text()").extract_first()
            book['book_piture'] = each_row.xpath("div[1]/a/img/@src").extract_first()
            book['book_schedule'] = each_row.xpath("div[2]/div/p[4]/span[2]/text()").extract_first()
            books.append(book)
        #去除空格并且存入redis
        self.space_redis(books)
        # return books

    def space_redis(self, items):
        list = []
        for item in items:
            author = item._values.get('book_author', False)
            if author is not False:
                try:
                    temp_auther = re.findall("\\n(.*?)\\r", author)[0].strip()
                    item._values['book_author'] = temp_auther
                    list.append(item._values)
                except Exception as err:
                    _log.error('mySpider_space_Pipeline ERROR 【' + str(err) + "】")
                    continue

        item_json = json.dumps(list, ensure_ascii=False)
        Redis.set(self.search_book_name + "-" + self.p, item_json)
