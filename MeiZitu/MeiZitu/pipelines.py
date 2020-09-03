# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class MeizituPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    # 重写该方法可从result中获取到图片的实际下载地址
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        title = item['name']
        image_guid = request.url.split('/')[-1]
        filename = 'full/{0}/{1}'.format(title, image_guid)
        return title

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        img_url = item['imgs_url']
        headers = {
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Referer': item['referrer']
        }
        yield Request(url= img_url, meta={'item': item}, headers=headers)
