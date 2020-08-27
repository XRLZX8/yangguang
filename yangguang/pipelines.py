# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class YangguangPipeline:
    def process_item(self, item, spider):
        item['content'] = self.parse_content(item['content'])
        item['host'] = spider.settings.get('MYSQL_HOST')
        if item['content_img'] is None:
            item['content_img'] = '该问政暂无图片'
        print(item)

    def parse_content(self,content):
        content = [re.sub(r'\xa0|\r|\t|\n|\s','',i)for i in content]
        content = [i for i in content if len(i) > 0]
        return content
