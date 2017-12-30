#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 烟草条形码爬虫
-- 烟草表
DROP TABLE IF EXISTS `t_tobacco`;
CREATE TABLE `t_tobacco` (
  `id`                        BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
  `product_name`              VARCHAR(32)  COMMENT '产品名称',
  `brand`                     VARCHAR(32)  COMMENT '品牌',
  `product_type`              VARCHAR(32)  COMMENT '产品类型',
  `package_spec`              VARCHAR(64)  COMMENT '包装规格',
  `reference_price`           VARCHAR(32)  COMMENT '参考价格',
  `manufacturer`              VARCHAR(32)  COMMENT '生产厂家',
  `pics`                      VARCHAR(255) COMMENT '图片URL',
  `created_time`              DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time`              DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='烟草表';

-- 烟草条形码表
DROP TABLE IF EXISTS `t_barcode`;
CREATE TABLE `t_barcode` (
  `id`                        BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
  `tobacco_id`                BIGINT COMMENT '香烟产品ID',
  `barcode`                   VARCHAR(32) COMMENT '条形码',
  `btype`                     VARCHAR(32) COMMENT '类型 小盒条形码/条包条形码',
  `created_time`              DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time`              DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='烟草条形码表';
"""
from scrapy import Request

from coolscrapy.utils import parse_text, tx
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from coolscrapy.items import Book


class TobaccoSpider(Spider):



    """
    爬取本页面内容，然后再提取下一页链接生成新的Request标准做法
    另外还使用了图片下载管道
    """
    name = "myspider"
    allowed_domains = ["baidu.com"]
    base_url = "http://zhannei.baidu.com/cse/search?p=1&s=5592277830829141693&entry=1&q="
    start_urls = []
    # start_urls = [
    #     base_url + "斗破苍穹"
    # ]
    pics_pre = 'http://zhannei.baidu.com/'

    def __init__(self, search_book_name=None, *args, **kwargs):
        if search_book_name is not None:
            self.start_urls.append(self.base_url + search_book_name)

    def parse(self, response):
        # 处理本页内容
        for item in self.parse_page(response):
            yield item
        # 找下一页链接递归爬
        # next_url = tx(response.xpath('//a[text()="【下一页】"]/@href'))
        # if next_url:
        #     self.logger.info('+++++++++++next_url++++++++++=' + self.base_url + next_url)
        #     yield Request(url=self.base_url + next_url, meta={'ds': "ds"}, callback=self.parse)
        #"//*[@id="results"]/div[3]/div/div[2]/h3/a"
        #""
    def parse_page(self, response):
        self.logger.info('Hi, this is a page = %s', response.url)
        books = []
        for ind, each_row in enumerate(response.xpath('//*[@id="results"]/div[3]/div')):
            if ind == 0:
                continue
            book = Book()
            book['book_name'] = each_row.xpath("div[2]/h3/a/@title").extract_first()
            book['book_auther'] = each_row.xpath("div[2]/div/p[1]/a/text()").extract_first()
            book['book_url'] = each_row.xpath("div[2]/h3/a/@href").extract_first()
            book['book_ins'] = each_row.xpath("div[2]/p/text()").extract_first()
            book['book_type'] = each_row.xpath("div[2]/div/p[2]/span[2]/text()").extract_first()
            book['book_word_count'] = each_row.xpath("div[2]/div/p[3]/span[2]/text()").extract_first()
            book['book_type'] = each_row.xpath("div[2]/div/p[2]/span[2]/text()").extract_first()
            book['book_piture'] = each_row.xpath("div[1]/a/img/@src").extract_first()
            book['book_schedule'] = each_row.xpath("div[2]/div/p[4]/span[2]/text()").extract_first()
            books.append(book)
        self.logger.info(books)
        return books
