# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photos(value):
    if value[:2]=='//':
        return f'http:{value}'
    return value

def cleaner_tags(item):
    result=item.split('">')[-1].split(':')
    key=result[0]
    value=result[-1].split('</span')[-1].split('</')[0][1:-1]

    return {key: value}

def cleaner_address(item):
    result=item.split('\n')

    return result[-1]

def dict_tags(items):
    result={}
    for itm in items:
        result.update(itm)
    return result

class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AvitoCar(scrapy.Item):
    _id=scrapy.Field()
    title=scrapy.Field(output_processor=TakeFirst())
    price=scrapy.Field(output_processor=TakeFirst())
    tags=scrapy.Field(input_processor=MapCompose(cleaner_tags), output_processor=dict_tags)
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photos))
    address = scrapy.Field(input_processor=MapCompose(cleaner_address))
