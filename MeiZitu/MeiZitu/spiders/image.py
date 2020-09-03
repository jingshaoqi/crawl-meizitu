# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from MeiZitu.items import MeizituItem

class MeiZituSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['meizitu.com', 'mzitu.com']
    start_urls = ['https://www.mzitu.com/']

    def parse(self, response):
        nodes = response.css('.main-content > .postlist > ul > li > a')
        with open('meizi.html','w') as f:
            f.write(response.text)
        for node in nodes:
            url = node.css('::attr(href)').extract_first().strip()
            headers = {
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
                'Referer': response.url
            }
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail, headers=headers)
            #break

        # 下一页
        '''
        next_element = response.css('.pagination > .nav-links > a.next.page-numbers')
        if next_element:
            next_href = next_element.css('::attr(href)').extract_first()
            next_url = parse.urljoin(response.url, next_href)
            yield Request(url = next_url, callback=self.parse)
        '''


    def parse_detail(self, response):
        img = response.css('div.content > div.main-image > p > a > img')
        if img is None:
            return
        item = MeizituItem()
        name = img.css('::attr(alt)').extract_first()
        imgs_url = img.css('::attr(src)').extract_first()
        item['name'] = name + '.jpg'
        item['imgs_url'] = imgs_url
        item['url'] = response.url
        item['referrer'] = response.url
        yield item
