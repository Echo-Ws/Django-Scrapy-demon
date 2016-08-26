# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
import re
from scrapy import Request
import datetime


class tshIIISSpider(scrapy.Spider):
    name = "tshIIIS"
    allowed_domains = ["iiis.tsinghua.edu.cn"]
    count = 0
    start_urls = [
        "http://iiis.tsinghua.edu.cn/list-265-1.html",
        "http://iiis.tsinghua.edu.cn/list-265-2.html",
        "http://iiis.tsinghua.edu.cn/list-265-3.html",
        "http://iiis.tsinghua.edu.cn/list-265-4.html",
        "http://iiis.tsinghua.edu.cn/list-265-5.html",
        "http://iiis.tsinghua.edu.cn/list-265-6.html",
        "http://iiis.tsinghua.edu.cn/list-265-7.html",
        "http://iiis.tsinghua.edu.cn/list-265-8.html",
        "http://iiis.tsinghua.edu.cn/list-265-9.html",
        "http://iiis.tsinghua.edu.cn/list-265-10.html",
        "http://iiis.tsinghua.edu.cn/list-265-11.html",
        "http://iiis.tsinghua.edu.cn/list-265-12.html",
        "http://iiis.tsinghua.edu.cn/list-265-13.html",
        "http://iiis.tsinghua.edu.cn/list-265-14.html",
        "http://iiis.tsinghua.edu.cn/list-265-15.html",
        "http://iiis.tsinghua.edu.cn/list-265-16.html",
        "http://iiis.tsinghua.edu.cn/list-265-17.html",
        "http://iiis.tsinghua.edu.cn/list-265-18.html",
        "http://iiis.tsinghua.edu.cn/list-265-19.html",
        "http://iiis.tsinghua.edu.cn/list-265-20.html",
        "http://iiis.tsinghua.edu.cn/list-265-21.html",
        "http://iiis.tsinghua.edu.cn/list-265-22.html",
        "http://iiis.tsinghua.edu.cn/list-265-23.html",
        "http://iiis.tsinghua.edu.cn/list-265-24.html",
        "http://iiis.tsinghua.edu.cn/list-265-25.html",
        "http://iiis.tsinghua.edu.cn/list-265-26.html",
        "http://iiis.tsinghua.edu.cn/list-265-27.html",
        "http://iiis.tsinghua.edu.cn/list-265-28.html",
        "http://iiis.tsinghua.edu.cn/list-265-29.html",
        "http://iiis.tsinghua.edu.cn/list-265-30.html",
        "http://iiis.tsinghua.edu.cn/list-265-31.html",
        "http://iiis.tsinghua.edu.cn/list-265-32.html",
        "http://iiis.tsinghua.edu.cn/list-265-33.html",
        "http://iiis.tsinghua.edu.cn/list-265-34.html",
        "http://iiis.tsinghua.edu.cn/list-265-35.html",
        "http://iiis.tsinghua.edu.cn/list-265-36.html",
        "http://iiis.tsinghua.edu.cn/list-265-37.html",
        "http://iiis.tsinghua.edu.cn/list-265-38.html",
        "http://iiis.tsinghua.edu.cn/list-265-39.html",
        "http://iiis.tsinghua.edu.cn/list-265-40.html",
        "http://iiis.tsinghua.edu.cn/list-265-41.html",
        "http://iiis.tsinghua.edu.cn/list-265-42.html",
        "http://iiis.tsinghua.edu.cn/list-265-43.html",
        "http://iiis.tsinghua.edu.cn/list-265-44.html",
        "http://iiis.tsinghua.edu.cn/list-265-45.html",
        "http://iiis.tsinghua.edu.cn/list-265-46.html",
        "http://iiis.tsinghua.edu.cn/list-265-47.html",
        "http://iiis.tsinghua.edu.cn/list-265-48.html",
        "http://iiis.tsinghua.edu.cn/list-265-49.html"]

    def parse(self, response):
        # 增量
        f = open("url", "a+")
        urls = f.read()

        single_url = re.split(ur'\n', urls)
        urllist = set([])
        for url in single_url:
            urllist.add(url)

        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//tbody/tr/td/a')

        for site in sites:
            titl = site.xpath('../a/text()').extract()[0]
            tit = site.xpath('../a/@href').extract()[0]
            lin = tit.replace("/s", 'http://iiis.tsinghua.edu.cn/s')

            if lin not in urllist:
                print lin
                urllist.add(lin)
                f.write(lin + "\n")
                yield Request(lin, callback=self.parse_item)
            else:
                print "already exist"
        f.close()

    def parse_item(self, response):
        sel = scrapy.selector.Selector(response)
        sites = response.xpath('//div[@class="media-body"]/p')
        info = sites.xpath('string(.)').extract()[0]
        # print ("iiiiiiiiii",info)
        xs = re.split(ur'\n', info)

        f = open("content", "a")

        item = LectureItem()

        if re.findall(u'.*?讨论组(.*)', xs[1]):
            x = re.split(ur'                        ', xs[1])
            xs[1] = x[2]

        xs[1] = xs[1].lstrip()
        xs[3] = xs[3].lstrip()
        xs[4] = xs[4].lstrip()
        xs[5] = xs[5].lstrip()
        xs[1] = xs[1].lstrip(u'标题：')
        xs[4] = xs[4].lstrip(u'时间： ')
        xs[5] = xs[5].lstrip(u'地点：')

        # print xs[1].encode('utf-8')
        # print xs[3].encode('utf-8')
        # print xs[4].encode('utf-8')
        # print xs[5].encode('utf-8')

        f.write("\n<<<<<<<<<<<>>>>>>>>>\n")
        self.count += 1
        f.write("count：%d\n" % (self.count))
        f.write("学校&学院：" + "清华大学交叉信息学院(tshIIIS)\n" + "链接：" + response.url + "\n")

        f.write("标题：" + xs[1].encode('utf-8') + "\n")
        item["title"] = xs[1]
        f.write("演讲人：" + xs[3].encode('utf-8') + "\n")
        item["speaker"] = xs[3]
        f.write("时间：" + xs[4].encode('utf-8') + "\n")
        xz = re.split(ur' ', xs[4])
        xy = re.split(ur'-', xz[1])
        str = xz[0] + '-' + xy[0]
        item['time'] = datetime.datetime.strptime(str, u'%Y-%m-%d-%H:%M')
        print "aaaaaaaaaaaaaaaa"
        print item['time']
        f.write("地点：" + xs[5].encode('utf-8') + "\n")
        item["place"] = xs[5]
        item["link"] = response.url
        item["university"] = u"清华大学交叉信息学院"

        if not item.get("update_time"):
            item["update_time"] = "Null"

        yield LectureItem(item)
        f.close()






