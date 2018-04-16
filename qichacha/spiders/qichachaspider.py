# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
# from scrapy.selector import Selector
# import json
from qichacha.items import QichachaItem
import re

class Qichacha(CrawlSpider):
    name = "qichacha"
    redis_key = 'qichacha:start_urls'
    start_urls = ['http://www.qichacha.com/gongsi_area.shtml?prov=AH&p=1']

    url = 'http://www.qichacha.com'
    # rules = (Rule(LinkExtractor(), callback='parse_page', follow=True),)
    #
    # # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #
    #     # 修改这里的类名为当前类名
    #     super(Qichacha, self).__init__(*args, **kwargs)
    def start_requests(self):
        reqs = []
        All_province = ['AH','BJ','CQ','FJ','GS','GD','GX','GZ','HAIN','HB','HLJ','HEN','HB',
                        'HUN','JS','JX','JL','LN','NMG','NX','QH','SD','SH','SX','SAX','SC','TJ','XJ','XZ','YN','ZJ','CN']
        for province in All_province:
            for i in range(1,501):
                req = Request('http://www.qichacha.com/g_%s_%d.html'%(province,i))
                reqs.append(req)
        return reqs
    def parse(self,response):
        # print response.body
        # selector = Selector(response)
        # print(type(response))
        #先大后小，分块处理
        Companys = response.xpath('//a[@class="list-group-item clearfix"]')
        for eachCompany in Companys:
            abs_url = eachCompany.xpath('@href').extract()[0]
            nameandstatus = eachCompany.xpath('span[@class="clear"]/span/text()').extract()
            # fullTitle = ''
            # for each in title:
            #     fullTitle += each
            #item类实例化
            item = QichachaItem()
            list = eachCompany.xpath('span[@class="clear"]/small/text()').extract()
            # print(list)
            # representative = eachCompany.xpath('span[@class="clear"]/small/text()').extract()[0]
            # star = eachCompany.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            # quote = eachCompany.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote可能为空，因此需要先进行判断
            location = list[len(list)-1].strip()
            if len(list) > 6:
                # location = list[6]
                fund = list[3].strip()
                area = list[4].strip()
            elif '元' in list[3]:
                # location = list[5]
                area = 'null'
                fund = list[3].strip()
            elif len(list) == 5:
                # location = list[5]
                area = list[3].strip()
                fund = 'null'
            else:
                area = 'null'
                fund = 'null'
            name = ''.join(nameandstatus[:-1]).strip()
            status = nameandstatus[len(nameandstatus)-1].strip()
            representative = list[1].strip()
            date = list[2].strip()
            item['name'] = name
            item['status'] = status
            item['representative'] = representative
            item['fund'] = fund
            item['date'] = date
            item['area'] = area
            item['location'] = location
            item['company_url'] = self.url+abs_url
            # item['representative'] = representative
            yield item
        # nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        # nextLink = re.findall('<a class="next" href="(.*?)">>></a>',response.text,re.S)
        # print(nextLink)
        # 第500页是最后一页，没有下一页的链接
        # if nextLink:
            # nextLink = nextLink[0]
            # print(nextLink[0])
            # yield Request(self.url + nextLink[0], callback=self.parse)
