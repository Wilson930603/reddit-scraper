# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawldataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Subreddit  = scrapy.Field()
    Thread_title = scrapy.Field()
    Comment_text = scrapy.Field()
    Comment_poster_ID = scrapy.Field()
    Original_poster = scrapy.Field()
    Date_posted = scrapy.Field()
    Accounting = scrapy.Field()
    Finance = scrapy.Field()
    Consultant = scrapy.Field()
    Marketing = scrapy.Field()
    Law = scrapy.Field()
    Medicine = scrapy.Field()
    URL = scrapy.Field()
