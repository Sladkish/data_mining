# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class HhVacancySpider(scrapy.Spider):
    name = 'hh_vacancy'
    allowed_domains = ['spb.hh.ru']
    # start_urls = ['https://spb.hh.ru/search/vacancy']
    # start_urls = ['https://spb.hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=Data+science&page=0']
    start_urls = ["https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=data+science&page=0"]
    def parse(self, response: HtmlResponse):
        prof = response.css('span.g-user-content a::text').extract()
        pagination = response.css('a.bloko-button.HH-Pager-Control::attr(href)').extract()
        next_link = pagination[-1]
        # print(prof)
        yield response.follow(next_link, callback=self.parse)
        vacancy_urls = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for url in vacancy_urls:
            yield response.follow(url, callback=self.parse_vacancy_page)

        # print(next_link)
    def parse_vacancy_page(self,response: HtmlResponse):
        vacancy_title=''.join(response.css('div.vacancy-title h1::text').extract())
        salary=response.css('div.vacancy-title p::text').extract()[0]
        company_name=response.css('p.vacancy-company-name-wrapper meta ::attr(content)').extract()[0]
        company_id=response.css('p.vacancy-company-name-wrapper a::attr(href)').extract()[0]
        company_url_hh=('spb.hh.ru'+company_id)
        # company_id2=response.css('a.vacancy-company-name::attr(href)').extract_first().split('?')[0]
        yield response.follow(company_id, callback=self.parse_company_page)
        skills=response.css('span::attr(data-tag-id)').extract()

        yield {'vacancy_title':vacancy_title,
               'company_name':company_name,
               'company_url_hh':company_url_hh,
               'skills':skills,
               'salary':salary
               }

    def parse_company_page(self,response: HtmlResponse):
        company_url=response.css('div.HH-SidebarView-UrlContainer a::attr(href)').extract()[0]

        yield {'company_url': company_url}


