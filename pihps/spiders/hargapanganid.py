# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pihps.items import PihpsItem
from datetime import datetime


class HargapanganidSpider(Spider):
    name = 'hargapanganid'
    allowed_domains = ['hargapangan.id']
    start_urls = ['https://hargapangan.id/statistik-provinsi/harian']

    #rules = (
    #    Rule(LinkExtractor(allow=r'questions\?page=[0-9]&sort=newest'), 
    #        callback='parse_item', follow=True),
    #)

    def parse(self, response):
        reports = response.xpath('//*[@id="report"]')

        for report in reports:
            province = report.xpath('//*[@id="report-header"]/div[2]/text()').extract()[0]
            city    = report.xpath('//*[@id="report-header"]/div[3]/text()').extract()[0]
            market  = report.xpath('//*[@id="report-header"]/div[4]/text()').extract()[0]
            date    = report.xpath('//*[@id="report"]/thead/tr/th[14]/text()').extract()[0]
            
            rowBody = report.xpath('//*[@id="report"]/tbody/tr')

            for tdElement in rowBody:
                commodity = tdElement.xpath('td[2]/span/text()').extract()
                price   = tdElement.xpath('td[14]/text()').extract()

                if len(commodity) > 0 and price[0] <> '-':
                    item = PihpsItem()
                    item['province'] = province.strip(': \t\n\r')
                    item['city']    = city.strip(': \t\n\r')
                    item['market']  = market.strip(': \t\n\r')
                    item['date']    = datetime.strptime(date, '%d/%m/%Y')
                    item['commodity'] = commodity[0].strip()
                    item['price']   = price[0].strip()

                    yield item
                
