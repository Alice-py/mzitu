# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mzitu.items import MzituItem


class MzituSpiderSpider(CrawlSpider):
    name = 'mzitu_spider'
    allowed_domains = ['www.mzitu.com', 'i5.mmzztt.com']
    start_urls = ['https://www.mzitu.com/']

    rules = (
        # 二级链接（分类）  restrict_xpaths限定节点，deny排除掉不要的链接，成功获取到所有的二级链接
        Rule(LinkExtractor(restrict_xpaths="//ul[@id='menu-nav']", deny='https://www.mzitu.com/all/',
                           allow=r'https://www.mzitu.com/[a-z]+/'),
             follow=True),

        # 三级链接（下一页）   这里注意一下一般fillow在最终爬取再放行跟进
        # https://www.mzitu.com/xinggan/page/\d/
        Rule(LinkExtractor(allow=r'https://www.mzitu.com/.*/page/\d+/'), follow=True),

        # 四级链接（）
        # https://www.mzitu.com/\d/
        Rule(LinkExtractor(restrict_xpaths="//ul[@id='pins']",
                           allow=r'https://www.mzitu.com/\d+'),
             # callback='parse_print_four',
             follow=True),

        # 详情页五级链接（下一页）
        Rule(LinkExtractor(allow=r"https://www.mzitu.com/\d+/\d+"),
             callback='parse_print_five',
             follow=True),

    )

    def parse_print_five(self, response):
        # 详情页的每一页（下一页）,顺便保存图片
        item = MzituItem()
        # 包头
        referer = str(response).replace('<200 https://www.mzitu.com/', '')
        pic_referer = referer.split('/')
        item['pic_referer'] = pic_referer[0]

        # url
        pic_url_list = []
        pic_url = response.xpath("//div[@class='main-image']//img/@src").get()
        pic_url_list.append(pic_url)
        item['pic_url'] = pic_url_list

        # path_class
        pic_path_class = response.xpath("//div[@class='main-meta']//a/text()").get()
        item['pic_path_class'] = pic_path_class
        # path_name
        pic_class_name = response.xpath("//div[@class='currentpath']//text()").getall()[-1].replace(" »", '')
        item['pic_class_name'] = pic_class_name

        # 图片名
        pic_name = pic_url.replace('https://i5.mmzztt.com/', '')
        pic_name = pic_name.replace('/', '_')
        item['pic_name'] = pic_name

        yield item
