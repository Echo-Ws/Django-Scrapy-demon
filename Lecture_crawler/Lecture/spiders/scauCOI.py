# -*- coding: utf-8 -*-

import scrapy
from Lecture.items import LectureItem
import re
from scrapy import Request
import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class scauCOISpider(scrapy.Spider):
	name = "scauCOI"
	allowed_domains = ["www.scau.edu.cn"]
	count = 0
	start_urls = ['http://www.scau.edu.cn/jzyg/sxxy/']

	def parse(self, response):

		f = open('url','a+')
		urls = f.read()

		single_url = re.split(ur'\n', urls)
		urllist = set([])
		for url in single_url:
			urllist.add(url)
		sel = scrapy.selector.Selector(response)
		sites = sel.xpath('//table[@id = "trsList"]/tbody/tr/td/font/a')

		for site in sites:
			link = site.xpath('../a/@href').extract()[0]   
			link = link.lstrip('.')             
			lin = "http://www.scau.edu.cn/jzyg/sxxy" + link
			if lin != "http://www.scau.edu.cn/jzyg/sxxy/201601/t20160113_137226.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201606/t20160616_140479.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201602/t20160229_137724.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201603/t20160323_138420.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201605/t20160513_139745.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201601/t20160117_137318.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201606/t20160612_140375.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201603/t20160323_138355.htm" and lin != "http://www.scau.edu.cn/jzyg/sxxy/201601/t20160102_136897.htm":
				yield Request(lin, callback = self.parse_item)

	def parse_item(self, response):
		sel = scrapy.selector.Selector(response)
		content = response.xpath('//div[@class = "TRS_Editor"]')

		f = open("content", "a")
		#f.write("\n<<<<<<<<<<<>>>>>>>>>\n")
		f.write("\n<<<<<<<<<<<>>>>>>>>>\n")
		f.write("链接："+response.url+"\n")
		flag_title = 0
		flag_time = 0
		flag_place = 0
		flag_speaker = 0
		for i in range(1):
			x = content[i].xpath('string(.)').extract()[0]
			xs = re.split(ur'：', x)
		item = LectureItem()
		item['title'] = 'Null'
		item['place'] = 'Null'
		item['speaker'] = 'Null'
		item['time'] = 'Null'


		for x in xs:
			if re.findall(u'题.*?目(.*)', x):
				if flag_title == 0:
					str = xs[xs.index(x) + 1]
					if re.findall(ur'报告人', str):
						strr = re.split(ur'报告人', str)
						str = strr[0]
					if re.findall(ur'特', str):
						strr = re.split(ur'特', str)
						str = strr[0]
					str = str.lstrip()
					item["title"] = str
					flag_title = 1
					item['title'] = str
					#f.write(ur"题目：" + str + '\n')


			elif re.findall(u'时.*?间(.*)', x):
				if flag_time == 0:
					str = xs[xs.index(x) + 1]

					if re.findall(ur'地', str):
						strr = re.split(ur'地', str)
						str = strr[0]

					if re.findall(ur'报', str):
						strr = re.split(ur'报', str)
						str = strr[0]

					if re.findall(ur'午', str) and re.findall(ur'四', str):
						strr = re.split(ur'（', str)
						str = datetime.datetime.strptime(strr[0],u'%Y.%m.%d')

					if re.findall(ur'日', str) and re.findall(ur'）', str) and not re.findall(ur'午', str):
						strr = re.split(ur'日', str)
						strrr = re.split(ur'）', strr[1])
						str = strr[0] +"日" + strrr[1]
						if re.findall(ur':', str):
							strr = re.split(ur':', str)
							str = strr[0]
						str = datetime.datetime.strptime(str,u'%Y年%m月%d日%H')

					if re.findall(ur'午', str) and re.findall(ur'日', str):
						strr = re.split(ur'日', str)
						strrr = re.split(ur'午', strr[1])
						strrr[1] = strrr[1].lstrip()
						str = strr[0] + '日' + strrr[1]
						if re.findall(ur':', str):
							strr = re.split(ur':', str)
							str = strr[0]
						str = datetime.datetime.strptime(str,u'%Y年%m月%d日%H')

					flag_time = 1
					item['time'] = str
					print 'AAAAAAAAAA'
					print item['time']
					#f.write("时间：" + str + '\n')


			elif re.findall(u'地.*?点(.*)', x):
				if flag_place == 0:
					str = xs[xs.index(x) + 1]
					if re.findall(ur'王', str):
						strr = re.split(ur'王', str)
						str = strr[0]
					if re.findall(ur'特', str):
						strr = re.split(ur'特', str)
						str = strr[0]
					if re.findall(ur'报', str):
						strr = re.split(ur'报', str)
						str = strr[0]
					if re.findall(ur'欢迎', str):
						strr = re.split(ur'欢迎', str)
						str = strr[0]
					flag_place = 1
					item['place'] = str
					#f.write("地点：" + str + '\n')

			elif re.findall(u'人(.*)', x) or re.findall(u'嘉.*?宾(.*)', x):
				if flag_speaker == 0:
					str = xs[xs.index(x) + 1]
					if re.findall(ur'主', str):
						strr = re.split(ur'主', str)
						str = strr[0]
					if re.findall(ur'报告', str):
						strr = re.split(ur'报告', str)
						str = strr[0]
					if re.findall(ur'时', str):
						strr = re.split(ur'时', str)
						str = strr[0]
					if re.findall(ur'演讲', str):
						strr = re.split(ur'演讲', str)
						str = strr[0]
					str = str.lstrip()
					flag_speaker = 1
					if not re.findall(ur'学院', str):
						item["speaker"] = str
					#f.write("演讲人：" + str + '\n')
		item['university'] = u'数学与信息学院(软件学院)'
		item['link'] = response.url
		item['update_time']='null'
		f.write('主题：'+ item['title'] + '\n')
		f.write('演讲人：'+ item['speaker'] + '\n')
		f.write('时间：')
		#f.write(item['time'])
		f.write('\n')
		f.write('地点：' + item['place'] + '\n')
		yield LectureItem(item)
