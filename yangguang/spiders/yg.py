import scrapy
from yangguang.items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    # start_urls = ['http://wzzdg.sun0769.com/political/index/politicsNewest?id=1&page=2']
    base_url = 'http://wzzdg.sun0769.com/'
    list_url = 'http://wzzdg.sun0769.com/political/index/politicsNewest?id=1&page={}'
    start_urls = [list_url.format(1)]

    def parse(self, response):
        li_list = response.xpath('//li[@class="clear"]')
        for li in li_list:
            item = YangguangItem()
            #xpath写的时候注意层级，如果之前已经取到了li，那么接下来为了循环取li中的内容，需要将目录选择改为./在
            # 当前面目录下进行筛选，而不是继续使用//进行全局筛选
            item['title'] = li.xpath('./span[@class="state3"]/a/text()').extract_first()
            item['pub_date'] = li.xpath('./span[@class="state5 "]/text()').extract_first()
            href_temp = li.xpath('./span[@class="state3"]/a/@href').extract_first()
            item['href'] = self.base_url+href_temp
            # print(item)
            yield scrapy.Request(
                    url=item['href'],
                    callback=self.parse_2,
                    meta={'item':item}
                )
        next_url = self.base_url+response.xpath('//a[@class="arrow-page prov_rota"]/@href').extract_first()
        # print(next_url)
        if next_url is not None:
            yield scrapy.Request(
                url = next_url,
                callback=self.parse
            )

    def parse_2(self,response):
        # print(response.text)
        item = response.meta.get('item')
        item['content'] = response.xpath('//pre/text()').extract()#多行文本不要用extract_first()
        img_temp = response.xpath('//div[@class="clear details-img-list Picture-img"]/img/@src').extract()
        if img_temp:
            item['content_img'] = img_temp
        else:
            item['content_img'] = None
        yield item
