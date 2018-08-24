# -*- coding: utf-8 -*-
import json
import re

import scrapy

from sz_rents.items import SzRentsItem


class RentsSpider(scrapy.Spider):
    name = 'rents'
    allowed_domains = ['sz.lianjia.com/dituzufang']
    start_urls = ['http://sz.lianjia.com/dituzufang/']

    url = "https://sz.lianjia.com/zufang/pg2bd1/"
    def start_requests(self):
        for i in range(1,101):
            url = "https://sz.lianjia.com/zufang/pg{}bd1/".format(i)

            yield scrapy.Request(url,callback=self.parse_url,dont_filter=True)
    def parse_url(self, response):
        detail_page = response.xpath('//*[@id="house-lst"]/li/div[2]/h2/a/@href').extract()[0]
        yield scrapy.Request(detail_page,callback=self.parse,dont_filter=True)
    def parse(self, response):
        item = SzRentsItem()
        xiaoqu = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[6]/a[1]/text()').extract()
        type = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[2]/text()').extract()
        size = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[1]/text()').extract()
        #orientation = response.xpath('//*[@id="house-lst"]/li/div[2]/div[1]/div[1]/span[3]/text()').extract()
        price = response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/span[1]/text()').extract()
        location = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[1]/text()').extract()
        bankuai = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/a[2]/text()').extract()
        item['xiaoqu'] = xiaoqu
        item['type'] =type
        if len(size[0]) <= 7:
            item['size'] = size[0][:-2]
        else:
            groups= re.match('([1-9]\d+)',size[0])
            item['size'] = groups.group(1)
        #item['orientation']=orientation
        item['price']=price
        item['location'] = location
        item['bankuai'] = bankuai
        yield item
