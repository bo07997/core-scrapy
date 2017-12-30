#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from scrapy import Request

from scrapy.spiders import CrawlSpider, Rule, Spider
from coolscrapy.items import Chapter_content


class TobaccoSpider(Spider):
    """
    爬取本页面内容，然后再提取下一页链接生成新的Request标准做法
    另外还使用了图片下载管道
    """
    name = "mySpider_book_content"
    #allowed_domains = ["baidu.com"]
    start_urls = []

    def __init__(self, chapter_url=None, chapter_id=None, *args, **kwargs):
        if chapter_url is not None:
            self.start_urls.append(chapter_url)
        self.chapter_id = chapter_id

    def parse(self, response):
        # 处理本页内容
        temp = response.xpath('//*[@id="contents"]/text()').extract()
        # for i, each_line in response.xpath('//*[@id="contents"]/text()').extract():
        #     result += each_line
        result = ""
        for li in temp:
            result += (li + "<br><br>")
        item = Chapter_content()
        item["chapter_id"] = self.chapter_id
        item['chapter_content'] = result
        yield item

