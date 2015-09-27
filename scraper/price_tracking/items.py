# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class TvItem(Item):
    # define the fields for your item here like:
    store_code = Field()
    internal_code = Field()
    price = Field()
    internet_price = Field()
    stock = Field()
    attributes = Field()
    url = Field()
    pass
