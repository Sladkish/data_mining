from scrapy.crawler import CrawlerProcess
from scrapy.settings import  Settings

from  avito import settings
from  avito.spiders.avito_car import AvitoCarSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoCarSpider)
    process.start()
