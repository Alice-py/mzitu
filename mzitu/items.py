# -*- coding: utf-8 -*-

import scrapy
class MzituItem(scrapy.Item):
    pic_url = scrapy.Field()
    pic_name = scrapy.Field()
    pic_referer = scrapy.Field()
    pic_class_name = scrapy.Field()
    pic_path_class = scrapy.Field()
