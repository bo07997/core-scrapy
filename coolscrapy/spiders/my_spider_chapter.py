#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scrapy import Request

from scrapy.spiders import CrawlSpider, Rule, Spider
from coolscrapy.items import Book_chapter


class TobaccoSpider(Spider):



    """
    爬取本页面内容，然后再提取下一页链接生成新的Request标准做法
    另外还使用了图片下载管道
    """
    name = "mySpider_book_chapter"
    #allowed_domains = ["baidu.com"]
    start_urls = []

    def __init__(self, book_url=None, book_id=None, *args, **kwargs):
        if book_url is not None:
            self.start_urls.append(book_url)
        self.book_id = book_id

    def parse(self, response):
        # 处理本页内容
        for item in self.parse_page(response):
            item["book_id"] = self.book_id
            yield item

    def parse_page(self, response):
        self.logger.info('Hi, this is a book_chapter = %s', response.url)
        chapters = []
        result = response.xpath('//*[@id="at"]/tr')
        for i, each_line in enumerate(result):
            for j, each_chapter in enumerate(each_line.xpath("td/a")):
                chapter = Book_chapter()
                chapter['chapter_name'] = each_chapter.xpath("text()").extract_first()
                chapter['chapter_url'] = response.url + each_chapter.xpath("@href").extract_first()
                chapters.append(chapter)
        return chapters
