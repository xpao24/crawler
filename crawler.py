#!/usr/bin/python
# -*- coding:utf-8 -*-

import Queue
import urllib2
import re
import MySQLdb
from datetime import datetime
import dao
from task_model import Task
from bloom_filter import BloomFilter

def store(url):
    print url
    task = Task(id=None,priority=0,type=1,state=0,link=url,\
                avaliable_time=now(),start_time=None,end_time=None)
    dao.insert(task)

def httpRequest(url):
    #Request source file
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()
    return page

def extract_urls(url):
    page = httpRequest(url)
    pattern = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>',re.S)
    items = re.findall(pattern,page)
    urls = []
    for item in items:
        urls.append(item[0])
    return urls

def now():
    cur = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return cur

def main():
    inital_page = "http://yue.ifeng.com"

    url_queue  = Queue.Queue()
    filter = BloomFilter()
    filter.add(inital_page)  
    url_queue.put(inital_page)

    while(True):
        urls = []
        current_url = url_queue.get() #取队列第一个元素
        try:
	    store(current_url)
	    urls = extract_urls(current_url) #抽取页面中的链接
        except Exception,e:
            print "Error extract_urls"
            print e
	for next_url in urls:
	    if filter.notcontains(next_url):
                filter.add(next_url)
	        url_queue.put(next_url)
  
if __name__ == "__main__":
    main()

