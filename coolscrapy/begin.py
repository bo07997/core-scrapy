from scrapy import cmdline

# name = 'mySpider_search'
# cmd = 'scrapy crawl {0} -a search_book_name="斗破苍穹"'.format(name)
# cmdline.execute(cmd.split())

# name = 'mySpider_book_chapter'
# cmd = 'scrapy crawl {0} -a book_url=http://www.x23us.com/html/50/50778/ -a book_id=1'.format(name)
# cmdline.execute(cmd.split())

name = 'mySpider_book_content'
cmd = 'scrapy crawl {0} -a chapter_url=https://www.x23us.com/html/50/50778/20464105.html -a chapter_id=1'.format(name)
cmdline.execute(cmd.split())