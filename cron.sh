#! /bin/sh

export PATH=$PATH:/usr/local/bin

cd /home/ubuntu/lecture/Lecture_crawler

nohup scrapy crawl jnuISAT > spider.log 2>&1 &
nohup scrapy crawl scutCS >> spider.log 2>&1 &
nohup scrapy crawl ScutSoftware >> spider.log 2>&1 &
nohup scrapy crawl tshIIIS >> spider.log 2>&1 &
nohup scrapy crawl SKLOIS >> spider.log 2>&1 &
nohup scrapy crawl scauCOI >> spider.log 2>&1 &
