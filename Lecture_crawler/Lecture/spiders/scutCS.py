# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
import re
from scrapy import Request
import datetime

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class ScutCSSpider(scrapy.Spider):
    name = "scutCS"
    allowed_domains = ["cs.scut.edu.cn"]
    count = 0
    start_urls = [
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=1",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=2",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=3",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=4",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=5",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=6",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=7",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=8",
        "http://cs.scut.edu.cn/xygk/kytz/?_active_paging_=paging&_page_=9"
    ]

    def parse(self, response):

        # 增量
        f = open("url", "a+")
        urls = f.read()

        single_url = re.split(ur'\n', urls)
        urllist = set([])
        for url in single_url:
            urllist.add(url)

        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//div[@id="paging"]/ul/li')

        for site in sites:

            tit = site.xpath('a/@title').extract()[0]

            if re.findall(ur'.*?报告会.*', tit):
                link = site.xpath('a/@href').extract()[0]
                lin = link.replace("/xygk/kytz", "http://cs.scut.edu.cn/xygk/kytz")

                if lin not in urllist:
                    urllist.add(lin)
                    f.write(lin + "\n")
                    yield Request(lin, callback=self.parse_item)
                else:
                    print "already exist"
        f.close()

    def parse_item(self, response):
        flag = 0
        flag2 = 0
        sel = scrapy.selector.Selector(response)
        content = response.xpath('//div[@class="news_text"]')
        f = open("content", "a")


        f.write("\n<<<<<<<<<<<>>>>>>>>>\n")
        self.count += 1
        f.write("count：%d\n" % (self.count))
        f.write("学校&学院：" + "华工计算机学院(scutCS)\n" + "链接：" + response.url + "\n")

        item = LectureItem()

        for i in range(1):
            x = content[i].xpath('string(.)').extract()[0]
            xs = re.split(ur'\n', x)

        for x in xs:
            for x in xs:

                if re.findall(u'.*?题目(.*)', x):
                    x = re.findall(u'.*?题目(.*)', x)[0]
                    x = x.lstrip()
                    x = x.lstrip(u'1：')
                    x = x.lstrip(u'2：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'报.*?告.*?人(.*)', x) and not re.findall(u'.*?简介(.*)', x):
                    x = re.findall(u'报.*?告.*?人(.*)', x)[0]
                    x = x.lstrip()
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    item["speaker"] = x
                    f.write("报告人：" + x.encode('utf-8') + "\n")

                elif re.findall(u'时.*?间(.*)', x):
                    x = re.findall(u'时.*?间(.*)', x)[0]
                    x = x.lstrip()
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    if re.findall(u'周日', x) or re.findall(u'星期日', x):
                        flag = 1
                    if re.findall(u'：', x):
                        flag2 = 1
                    xy = re.split(ur'日', x)
                    if flag == 1:
                        xy[1] = xy[2]
                    xyz = re.split(ur'午', xy[1])
                    x = xy[0] + "日" + xyz[1]
                    if flag2 == 0:
                        item["time"] = datetime.datetime.strptime(x, u'%Y年%m月%d日%H:%M')
                    if flag2 == 1:
                        item["time"] = datetime.datetime.strptime(x, u'%Y年%m月%d日%H：%M')
                    f.write("时间：" + x.encode('utf-8') + "\n")


                elif re.findall(u'地.*?点(.*)', x):
                    x = re.findall(u'地.*?点(.*)', x)[0]
                    x = x.lstrip()
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    item["place"] = x
                    f.write("地点：" + x.encode('utf-8') + "\n")
                item["link"] = response.url
                item["university"] = u"华工计算机学院"
                update_time = sel.xpath('//div[@class="sub_title"]/text()').extract()[0]
                update_time = update_time.lstrip(u'日期：')
                updatet = re.split(" ", update_time)
                b = datetime.datetime.strptime(updatet[0], u'%Y年%m月%d日')
                item["update_time"] = b

            f.write("更新时间：" + updatet[0].encode('utf-8'))
        yield LectureItem(item)

        f.close()
