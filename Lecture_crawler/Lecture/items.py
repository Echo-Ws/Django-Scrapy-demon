# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LectureItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    speaker = scrapy.Field()
    time = scrapy.Field()
    place = scrapy.Field()
    university = scrapy.Field()
    link = scrapy.Field()
    update_time = scrapy.Field()
