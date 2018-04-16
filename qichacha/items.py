# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class QichachaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    status = Field()
    representative = Field()
    fund = Field()
    date = Field()
    area = Field()
    location = Field()
    company_url = Field()
