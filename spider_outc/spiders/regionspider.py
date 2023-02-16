import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from ..items import RegionItem1,RegionItem2,RegionItem3,RegionItem4
from scrapy.linkextractors import LinkExtractor
import re


class RegionSpider(scrapy.Spider):
    name = 'default'

    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2022/index.html']
    allowed_domains = ['stats.gov.cn']

    def parse(self, resposne,**kwargs):
        le = LinkExtractor(attrs=('href',), allow='.html$')
        lr = le.extract_links(resposne)
        # links = [i.url for i in lr]
        # texts = [i.text for i in lr]
        for node in lr:
            item1 = RegionItem1()
            item1['province'] = node.text
            yield item1
            yield Request(node.url, callback=self.parse2)

    def parse2(self, response):
        # province = response.meta['province']
        for node in response.xpath('//tr[@class="citytr"]'):
            item2 = RegionItem2()
            item2['city'] = node.xpath('./td[2]/a/text()').extract()[0]
            item2['city_code'] = node.xpath('./td[1]/a/text()').extract()[0]
            url1 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2022/'
            url = url1 + node.xpath('./td[2]/a/@href').extract()[0]
            yield item2
            yield Request(url, callback=self.parse3)

    def parse3(self, response):
        for node in response.xpath('//tr[@class="countytr"]'):
            item3 = RegionItem3()
            name = node.xpath('./td[2]/a/text()').extract()
            if name :
                item3['town'] = node.xpath('./td[2]/a/text()').extract()[0]
                item3['town_code'] = node.xpath('./td[1]/a/text()').extract()[0]

                url1 = response.request.url
                url1 = re.split('/\d+.html', url1)[0]

                url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
                yield item3
                yield Request(url, callback=self.parse4)

    def parse4(self, response):
        # 街道
        for node in response.xpath('//tr[@class="towntr"]'):
            item4 = RegionItem4()
            item4['village'] = node.xpath('./td[2]/a/text()').extract()[0]
            item4['village_code'] = node.xpath('./td[1]/a/text()').extract()[0]

            # url1 = response.request.url
            # url1 = re.split('/\d+.html', url1)[0]
            #
            # url = url1 + '/' + node.xpath('./td[2]/a/@href').extract()[0]
            yield item4
            # yield Request(url, callback=self.parse5)


