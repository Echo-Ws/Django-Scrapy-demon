# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
import re
from scrapy import Request
import datetime
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class SKLOISSpider(scrapy.Spider):
    name = "SKLOIS"
    allowed_domains = ["sklois.iie.cas.cn"]
    count = 0
    update = 0
    start_urls = ["http://sklois.iie.cas.cn/tzgg/tzgg_16520/index.html",
                  "http://sklois.iie.cas.cn/tzgg/tzgg_16520/index_1.html",
                  "http://sklois.iie.cas.cn/tzgg/tzgg_16520/index_2.html"
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
        sites = sel.xpath('//table[@width="665"]/tr/td/a')

        for site in sites:

            tit = site.xpath('../a/@title').extract()[0]
            if re.findall(ur'.*?学术报告.*', tit) or re.findall(ur'.*?讲座通知.*', tit) or re.findall(ur'.*?学术讲座.*', tit):
                link = site.xpath('../a/@href').extract()[0]
                link = link.lstrip(u'.')
                lin = "http://sklois.iie.cas.cn/tzgg/tzgg_16520" + link
                if lin not in urllist:
                    urllist.add(lin)
                    f.write(lin + "\n")
                    # self.update = site.xpath('../../td[2]/text()').extract()[0]
                    # print ("aaaaaaaaaaaaaaaa",self.update)
                    yield Request(lin, callback=self.parse_item)
                else:
                    print "already exist"
        f.close()

    def parse_item(self, response):
        sel = scrapy.selector.Selector(response)
        content = response.xpath('//td[@class="nrhei"]')
        f = open("content", "a")
        items = []
        flag = 0
        flag1 = 0

        f.write("\n<<<<<<<<<<<>>>>>>>>>\n")

        self.count += 1
        f.write("count：%d\n" % (self.count))
        f.write("所属机构：信息安全国家重点实验室(SKLOIS)\n" + "链接：" + response.url + "\n")
        item = LectureItem()
        for i in range(1):
            x = content[i].xpath('string(.)').extract()[0]
            xs = re.split(ur'\n', x)

            for x in xs:

                if re.findall(u'目(.*)', x) and not re.findall(u'.*?五(.*)', x) and not re.findall(u'.*?的(.*)',
                                                                                                 x) and flag == 0:
                    x = re.findall(u'目(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    flag = 1
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'主.*?题(.*)', x) and not re.findall(u'.*?五(.*)', x):
                    x = re.findall(u'主.*?题(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")


                elif re.findall(u'学术报告(.*)', x) and flag == 0:
                    x = re.findall(u'学术报告(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    flag = 1
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'Title:(.*)', x) and flag == 0:
                    x = re.findall(u'Title:(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    flag = 1
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'报告题目(.*)', x) and flag == 0:
                    x = re.findall(u'报告题目(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    flag = 1
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'目(.*)', x) and not re.findall(u'.*?五(.*)', x) and re.findall(u'.*?思考(.*)',
                                                                                               x) and flag == 0:
                    x = re.findall(u'目(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    flag = 1
                    item["title"] = x
                    f.write("题目：" + x.encode('utf-8') + "\n")

                elif re.findall(u'报.*?告.*?人(.*)', x) and not re.findall(u'.*?简介(.*)', x) and not re.findall(u'.*?的(.*)',
                                                                                                            x):
                    x = re.findall(u'报.*?告.*?人(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["speaker"] = x
                    f.write("报告人：" + x.encode('utf-8') + "\n")

                elif re.findall(u'Speaker(.*)', x) and not re.findall(u'.*?bio(.*)', x):
                    x = re.findall(u'Speaker(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["speaker"] = x
                    f.write("报告人：" + x.encode('utf-8') + "\n")

                elif re.findall(u'主.*?讲.*?人(.*)', x) and not re.findall(u'.*?简介(.*)', x) and not re.findall(u'.*?的(.*)',
                                                                                                            x):
                    x = re.findall(u'主.*?讲.*?人(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["speaker"] = x
                    f.write("报告人：" + x.encode('utf-8') + "\n")

                elif re.findall(u'报.*?告.*?人(.*)', x) and not re.findall(u'.*?简介(.*)', x) and re.findall(u'.*?研究(.*)',
                                                                                                        x):
                    x = re.findall(u'报.*?告.*?人(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.lstrip(':')
                    x = x.lstrip()
                    item["speaker"] = x
                    f.write("报告人：" + x.encode('utf-8') + "\n")

                elif re.findall(u'.*?时.*?间(.*)', x) and flag1 == 0:
                    x = re.findall(u'.*?时.*?间(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    if re.findall(ur'地点', x):
                        xyz = re.split(ur'地点：', x)
                        x = xyz[0]
                        item['place'] = xyz[1]
                        f.write("地点：" + item['place'].encode('utf-8') + "\n")
                    if re.findall(u'日', x):
                        xy = re.split(ur'日', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y年%m月%d')
                    elif not re.findall(ur',', x) and not re.findall(ur'（', x):
                        xy = re.split(ur' ', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')
                    elif re.findall(ur'星期', x):
                        xy = re.split(ur'（', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')

                    elif re.findall(ur'September', x) and re.findall(ur'7', x):
                        item["time"] = datetime.datetime(2015, 9, 7)
                    elif re.findall(ur'May', x) and re.findall(ur'26', x):
                        item["time"] = datetime.datetime(2015, 5, 26)
                    print "aaaaaaaaa"
                    print item['time']
                    # xy = re.split(ur'(',x)
                    # item["time"] = x
                    flag1 = 1
                    # f.write("时间：" + item["time"] + "\n")


                elif re.findall(u'Time(.*)', x) and not re.findall(u'and(.*)', x) and not re.findall(u'the(.*)', x):
                    x = re.findall(u'Time(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    if re.findall(u'日', x):
                        xy = re.split(ur'日', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y年%m月%d')
                    elif not re.findall(ur',', x) and not re.findall(ur'（', x):
                        xy = re.split(ur' ', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')
                    elif re.findall(ur'星期', x):
                        xy = re.split(ur'（', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')

                    elif re.findall(r'September', x) and re.findall(r'7', x):
                        item["time"] = datetime.datetime(2015, 9, 7)
                        print item["time"]
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    elif re.findall(r'May', x) and re.findall(r'26', x):
                        item["time"] = datetime.datetime(2015, 5, 26)
                    print "aaaaaaaaa"
                    print item['time']
                    # xy = re.split(ur'(',x)
                    item["time"] = x
                    flag1 = 1
                    f.write("时间：" + x.encode('utf-8') + "\n")


                elif re.findall(u'.*?日.*?期(.*)', x) and flag1 == 0 and not re.findall(u'的(.*)', x):
                    x = re.findall(u'.*?日.*?期(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    if re.findall(u'日', x):
                        xy = re.split(ur'日', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y年%m月%d')
                    elif not re.findall(ur',', x) and not re.findall(ur'（', x):
                        xy = re.split(ur' ', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')
                    elif re.findall(ur'星期', x):
                        xy = re.split(ur'（', x)
                        item["time"] = datetime.datetime.strptime(xy[0], u'%Y.%m.%d')

                    elif re.findall(ur'September', x) and re.findall(ur'7', x):
                        item["time"] = datetime.datetime(2015, 9, 7)
                    elif re.findall(ur'May', x) and re.findall(ur'26', x):
                        item["time"] = datetime.datetime(2015, 5, 26)
                    print "aaaaaaaaa"
                    print item['time']
                    # xy = re.split(ur'(',x)
                    item["time"] = x
                    flag1 = 1
                    f.write("时间：" + x.encode('utf-8') + "\n")

                elif re.findall(u'.*?地.*?点(.*)', x):
                    x = re.findall(u'.*?地.*?点(.*)', x)[0]
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    item["place"] = x
                    f.write("地点：" + x.encode('utf-8') + "\n")

                elif re.findall(u'Address(.*)', x):
                    x = x.lstrip(u'Address: ')
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    item["place"] = x
                    f.write("地点：" + x.encode('utf-8') + "\n")

                elif re.findall(u'Place(.*)', x):
                    x = x.lstrip(u'：')
                    x = x.encode('utf-8').lstrip(':')
                    x = x.decode('utf-8').lstrip()
                    item["place"] = x
                    f.write("地点：" + x.encode('utf-8') + "\n")
                item["link"] = response.url
                item["university"] = u"信息安全国家重点实验室"

            # item["update_time"] = self.update
            # f.write("更新日期："+ self.update.encode('utf-8') +"\n")
        if not item.get("speaker"):
            item["speaker"] = "Null"

        if not item.get("update_time"):
            item["update_time"] = "Null"
        yield LectureItem(item)
        f.close()
