# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
from scrapy import Request
import re
import datetime

class ScutSoftware(scrapy.Spider):
    name = "ScutSoftware"
    allowed_domain = ["scut.edu.cn"]

    count = 1
    last_max_num = 0
    max_num = 0

    def start_requests(self):
        nextPage = "http://www2.scut.edu.cn/s/87/t/431/p/28/i/" + str(self.count) + "/list.htm"
        yield Request(nextPage, callback=self.parse)

    def parse(self, response):

        url_list = response.xpath('//table[@class="columnStyle"]//a')

        if url_list is None:
            return

        self.count += 1

        nextPage = "http://www2.scut.edu.cn/s/87/t/431/p/28/i/" + str(self.count) + "/list.htm"

        yield Request(nextPage, callback=self.parse)

        for url in url_list:
            title = url.xpath('font/text()').extract()[0]
            if re.findall(ur'.*?学术讲座.*', title) or re.findall(ur'.*?技术交流.*', title) or re.findall(ur'.*?学术报告.*', title) or re.findall(ur'.*?报告会.*', title):
                url = url.xpath('@href').extract()[0]
                info_num = re.findall('.*?info(.*).h.*', url)[0]
                info_num = int(info_num)
                # 当大于上一次爬取到的信息号时，说明没有爬过
                if info_num > self.last_max_num:
                    # 记录此次最大的信息号
                    if info_num > self.max_num:
                        self.max_num = info_num
                    url = url.replace("/s", 'http://www2.scut.edu.cn/s')
                    yield Request(url, callback=self.extract_url)

    def extract_url(self, response):
        content = response.xpath('//div[@id="infocontent"]//p')

        # 去除里面不含任何文字的空标签和主持人的选项，num记录要被删除的号码
        num = []
        for x in range(len(content)):
            text = content[x].xpath('string(.)').extract()
            text = text[0]

            if text == ''or text == u' 'or re.findall(ur'.*?主 持 人.*', text):
                num.append(x)

        for x in range(len(num)):
            content.pop(num[x] - x)

        # f = open('why', 'a')
        #
        # f.write("\n<<<<<<<<<<<>>>>>>>>>\n"+response.url+"\n"+str(self.count-1)+"\n")

        # 将其初始化为数字 如果没有匹配项目，则在后面lstrip方法时会出错，自动把没有抓取到完整信息的通知过滤掉
        item = LectureItem()
        item["title"] = 0
        item["speaker"] = 0
        item["time"] = 0
        item["place"] = 0

        for i in range(4):
            x = content[i].xpath('string(.)').extract()[0]
            xs = re.split(ur'\n', x)
            # ：不统一 有的:是英文的有的是中文的 所以为了匹配只能把冒号去掉
            for x in xs:
                if not item["title"] and re.findall(u'.*?题目(.*)', x):
                    item["title"] = re.findall(u'.*?题目(.*)', x)[0]

                elif not item["speaker"] and re.findall(u'报.*?告.*?人(.*)', x):
                    item["speaker"] = re.findall(u'报.*?告.*?人(.*)', x)[0]

                elif not item["time"] and re.findall(u'.*?时间(.*)', x):
                    item["time"] = re.findall(u'.*?时间(.*)', x)[0]

                elif not item["place"] and re.findall(u'.*?地点(.*)', x):
                    item["place"] = re.findall(u'.*?地点(.*)', x)[0]

        item["link"] = response.url
        for x in item:
            item[x] = item[x].lstrip(u'：')
            item[x] = item[x].encode('utf-8').lstrip(':')
            item[x] = item[x].decode('utf-8').lstrip()
            # f.write(item[x].encode('utf-8') + '\n')

        content = response.xpath('//div[@class="foothang"]').xpath('string(.)').extract()[0]
        # print content.encode('utf-8')
        content = re.findall('[\d]+', content)

        item['update_time'] = str(content[0]) + '-' + str(content[1]) + '-' + str(content[2])
        item['update_time'] = datetime.datetime.strptime(item['update_time'], '%Y-%m-%d')
        # print item['update_time']
        # print re.findall(U'.*?更新日期：(.*)访问.*', content)
        item['university'] = u'华南理工大学'

        content = re.findall('[\d]+', item['time'])

        # 为了排序牺牲了部分讲座的结束时间和连续开几天的讲座的信息 http://www2.scut.edu.cn/s/87/t/431/ec/0c/info125964.htm此为丢失的讲座
        item['time'] = str(content[0]) + '-' + str(content[1]) + '-' + str(content[2])+' ' + \
                       str(content[3])+':'+str(content[4])
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d %H:%M')
        yield LectureItem(item)












