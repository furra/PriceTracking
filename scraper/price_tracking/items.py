# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TvItem(Item):
    # define the fields for your item here like:
    internal_code = Field()
    store_code = Field()
    code = Field()
    attributes = Field()
    available = Field()
    pass
