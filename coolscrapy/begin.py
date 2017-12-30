from scrapy import cmdline

# cmdline.execute("scrapy crawl myspider  -o dmoz.json".split())
name = 'myspider'
cmd = 'scrapy crawl {0} -a search_book_name="斗破苍穹"'.format(name)
cmdline.execute(cmd.split())