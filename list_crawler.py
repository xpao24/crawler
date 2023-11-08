#!/usr/bin/python
#-*- coding: UTF-8 -*-

# @author xpao24
# wwww.javaguidepro.cn

# @Time    : 2023-11-08
# @Author  : xpao24
# @URL  : https://wwww.javaguidepro.cn


import urllib2
import re
import dao
import time
from datetime import datetime
import threading,thread
from task_model import Task
import sys,os


# 条件变量
cv = threading.Condition()

def http_crawler(url,type):
    content = http_request(url)
    if type == 0:
        page = parse_page_list(content)
    else:
        page = content
    return page

def http_request(url):
    #Request source file
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()
    return page

def parse_page_list(page):
    pattern = re.compile('<a href="http://yue.ifeng.com/news/detail_(.*?)" target="_blank">(.*?)</a>',re.S)
    items = re.findall(pattern,page)
    #for item in items:
    #    print item[0],item[1]
    return items


def save_page(page,file_name):
    #Save source file
    project_path = os.getcwd()
    ymd = datetime.now().strftime('%Y%m%d')
    dir_path = project_path + "/pages/" +ymd +"/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    webFile = open(dir_path+file_name,'wb')
    webFile.write(page)
    webFile.close()

def now():
    cur = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return cur

def cond_wait(cv):
    cv.wait()    

def cond_signal(cond):
    cond.acquire() 
    cond.notify()
    cond.release()

def build_task(url):
    task = Task(id=None,priority=0,type=1,state=0,link=url,avaliable_time=now(),start_time=None,end_time=None)
    return task
  
def run():
    while True:
        print "开始处理任务"
        task = dao.select(state=0)       
        cv.acquire()
        while task == None:
            cond_wait(cv)
        cv.release()
        ret = dao.update(state=1, update_time=now(), id=task.id)
        if ret == 0:
            print "任务已经被处理，直接跳出循环"
            continue
        page = http_crawler(task.link,task.type)   
        if task.type == 0:
            print "处理列表任务...."
            for item in page:
                prefix = "http://yue.ifeng.com/news/detail_"
                link = prefix + item[0]
                new_task = build_task(link)
                dao.insert(new_task)
                cond_signal(cv)
            dao.update(state=2, update_time=now(), id=task.id)
        if task.type == 1:
	    file_name = task.link.split("/")[-1]
	    print "保存页面....",task.link,file_name   
            save_page(page,file_name)
            ret = dao.update(state=2, update_time=now(), id=task.id)
        print "任务完成"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "请输入正确的命令"
        print "eg: python list_crawler.py 5"
        sys.exit()
    num = sys.argv[1]
    if num == None:
        num = 1
    else:
        num = int(num)
    print "开启" + str(num) +"个线程处理"
    for i in range(num):
        thread.start_new_thread(run())
