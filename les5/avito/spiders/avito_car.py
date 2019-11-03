# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from avito.items import AvitoCar

class AvitoCarSpider(scrapy.Spider):
    name = 'avito_car'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/avtomobili']
    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[contains(@class, "pagination")]/'
                                   'div[contains(@class, "pagination-nav")]/'
                                   'a[contains(@class, "pagination-next")]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        ads = response.xpath('//div[contains(@class, "catalog_table")]//div[contains(@class, "item")]//'
                             'h3[@data-marker="item-title"]/a/@href').extract()
        for itm in ads:
            yield response.follow(itm, callback=self.car_parse)
    def car_parse(self, response: HtmlResponse):
        item = ItemLoader(AvitoCar(), response)
        # title = response.xpath('//div[contains(@class, "title-info")]//h1[contains(@class, "title-info")]//'
        #                        'span[contains(@class, "title-info")]/text()').get()
        # price = response.xpath('//span[contains(@class, "price-value-strin")]//span[contains(@class, "js-item-price")]/@content').extract_first()
        # photos = response.xpath('//div[contains(@class, "gallery-extended-img-frame")]/@data-url').extract()
        # address = response.xpath('//span[@class="item-address__string"]/text()').get()[2:]
        # # tad_data = response.xpath('//li[@class= "item-params-list-item"]/text()').extract()
        # # tad_key = response.xpath('//span[@class= "item-params-label"]/text()').extract()
        # tags = response.xpath('//li[@class= "item-params-list-item"]').extract()

        item.add_xpath("title", '//div[contains(@class, "title-info")]//h1[contains(@class, "title-info")]//'
                                'span[contains(@class, "title-info")]/text()')
        item.add_xpath("price", '//div[@class= "item-price-value-wrapper"]//span[@class="js-item-price"]/@content')
        item.add_xpath("photos", '//div[contains(@class, "gallery-extended-img-frame")]/@data-url')
        item.add_xpath("address", '//span[@class="item-address__string"]/text()')
        item.add_xpath("tags", '//li[@class= "item-params-list-item"]')
        yield item.load_item()

