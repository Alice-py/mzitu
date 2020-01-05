# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re


class DownloadPicPipeline(ImagesPipeline):
    # 保存图片

    def update_header(self, referer):
        # 由于mmzztt网站采用的反爬机制为识别包头的referer，固从每个图片拿到对应id进行组合
        default_headers = {
            'accept': 'image/webp,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        default_headers['referer'] = "https://www.mzitu.com/{}".format(referer)
        return default_headers

    def get_media_requests(self, item, info):
        for pic_url in item['pic_url']:
            yield Request(url=pic_url, headers=self.update_header(item['pic_referer']), meta={'class':item['pic_path_class'],'class_name':item['pic_class_name']})

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):

        # 提取url前面名称作为图片名。
        image_guid = request.url.split('/')[-1]
        # 接收上面meta传递过来的图片名称
        name = request.meta['class']
        class_name = request.meta['class_name']
        # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
        name = re.sub(r'[？\\*|“<>:/]', '', name)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{2}/{0}/{1}'.format(class_name, image_guid, name)
        print(filename)
        return filename

