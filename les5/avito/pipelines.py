# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from sqdatabase.database import AvitoRABase
# from sqdatabase.model import  Real_estate, Base
import os
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class AvitoPipeline(object):
    def __init__(self):
        mongo_url = "mongodb://localhost:27017/"
        client = MongoClient(mongo_url)
        self.db_av = client.av_car

    def process_item(self, item, spider):
        # if spider.name == 'av_car':
        #     pass
        collection = self.db_av[spider.name]
        collection.insert_one(item)
        return item

class AvitoPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos']=[itm[1] for itm in results if itm[0]]
        return item

