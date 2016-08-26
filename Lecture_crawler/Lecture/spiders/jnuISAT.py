# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
import re
from scrapy import Request
import datetime

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class jnuISATSpider(scrapy.Spider):
    name = "jnuISAT"
    count = 0
    allowed_domains = ["xxxy.jnu.edu.cn"]
    start_urls = ["http://xxxy.jnu.edu.cn/Category_37/Index_1.aspx",
                  "http://xxxy.jnu.edu.cn/Category_37/Index_2.aspx"]

    def parse(self, response):
        # 增量
        f = open("url", "a+")
        urls = f.read()

        single_url = re.split(ur'\n', urls)
        urllist = set([])
        for url in single_url:
            urllist.add(url)

        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//ul[@class="newsList"]/li/a')

        for site in sites:
            tit = site.xpath("../a[@title]").extract()[0]
            if re.findall(ur'.*?学术讲座.*', tit):
                link = site.xpath('../a/@href').extract()[0]
                lin = "http://xxxy.jnu.edu.cn" + link

                if lin not in urllist:
                    print lin
                    urllist.add(lin)
                    f.write(lin + "\n")
                    yield Request(lin, callback=self.parse_item)
                else:
                    print "already exist"
        f.close()

    def parse_item(self, response):
        flag = 0
        sel = scrapy.selector.Selector(response)
        content = response.xpath('//div[@id="fontzoom"]')

        f = open("content", "a")

        contt = sel.xpath('//div[@class="property"]/span[3]/text()').extract()[0]
        contt = contt.lstrip(u'发布时间：')
        conttt = datetime.datetime.strptime(contt, u'%Y年%m月%d日')
        f.write("\n<<<<<<<<<<<>>>>>>>>>\n")
        self.count += 1
        f.write("count：%d\n" % (self.count))
        f.write("学校&学院：" + "暨南大学信息学院(jnuISAT)\n" + "链接：" + response.url + "\n")

        item = LectureItem()
        for i in range(1):
            x = content[i].xpath('string(.)').extract()[0]
            xs = re.split(ur'\n', x)
            for x in xs:

                if re.findall(u'题.*?目(.*)', x):
                    x = re.findall(u'题.*?目(.*)', x)[0]
                    x = x.lstrip(u'一：')
                    x = x.lstrip(u'二：')
                    x = x.lstrip(u'三：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["title"] = x

                    f.write("题目：" + item["title"].encode('utf-8') + "\n")

                elif re.findall(u'报.*?告.*?人(.*)', x) and not re.findall(u'.*?简介(.*)', x):

                    x = re.findall(u'报.*?告.*?人(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["speaker"] = x
                    f.write("报告人：" + item["speaker"].encode('utf-8') + "\n")

                elif re.findall(u'时.*?间(.*)', x) and not re.findall(u'.*?的(.*)', x):
                    x = re.findall(u'时.*?间(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    if re.findall(u'周日', x) or re.findall(u'星期日', x):
                        flag = 1
                    xy = re.split(ur'日', x)
                    if flag == 1:
                        xy[1] = xy[2]
                    xyz = re.split(ur'午', xy[1])
                    x = xy[0] + "日" + xyz[1]
                    if re.findall(u'始', x):
                        item["time"] = datetime.datetime.strptime(x, u'%Y年%m月%d日%H：%M始\r')
                        f.write("时间：" + x.encode('utf-8') + "\n")
                    else:
                        # 2016年4月29日8：30～10：00
                        xy = re.split(ur'～', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y年%m月%d日%H：%M')
                        f.write("时间：" + xy[0].encode('utf-8') + "\n")

                elif re.findall(u'地.*?点(.*)', x):

                    x = re.findall(u'地.*?点(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["place"] = x
                    f.write("地点：" + item["place"].encode('utf-8') + "\n")
                item["link"] = response.url
                item["university"] = u"暨南大学信息学院"
                item["update_time"] = conttt

            f.write("更新时间：" + contt)

        yield LectureItem(item)
        f.close()
