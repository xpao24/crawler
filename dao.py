#!/usr/bin/python
# -*- encoding:utf-8 -*-

# @Time    : 2023-11-08
# @Author  : xpao24
# @URL  : https://wwww.javaguidepro.cn

import MySQLdb
from task_model import Task
import sys


def connection() :
    db = None
    if db == None:
        db = MySQLdb.connect("localhost","root","123456","news_crawler")
    return db

def select(state):
    db = connection()
    cursor = db.cursor()
    sql = "select * from task where state = '%d'" % (state) 
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row == None:
            task = None
        else:
            task = Task(id=row[0],priority=row[1],type=row[2],state=row[3],link=row[4],avaliable_time=row[5],start_time=row[6],end_time=row[7])
    except:
        print "Error : unable to fetch daba" 
    db.close()
    return task

def update(state,update_time,id):
    db = connection()
    cursor = db.cursor()
    if state == 1:
        sql = "update task set state = '%d', start_time = '%s' where id = '%d'" % (state,update_time,id)
    if state == 2:
        sql = "update task set state = '%d', end_time = '%s' where id = '%d'" % (state,update_time,id)
    try:
        count = 0
        count = cursor.execute(sql)
        db.commit()
    except Exception,e:
        print "Error cann't update "
        print e 
        db.rollback()
    finally:
        db.close()
    return count

def insert(task):
    db = connection()
    cursor = db.cursor()
    sql = "insert into task (priority,type,state,link,avaliable_time) values ( \
            '%d','%d','%d','%s','%s')" % (task.priority,task.type,task.state,task.link, \
            task.avaliable_time) 
    try:
        count = 0
        count = cursor.execute(sql)
        db.commit()
    except Exception,e:
        print "Error insert"
        print e
        db.rollback()
    finally:
        db.close()
    return count
   
def lock(table_name):
    db = connection()
    cursor = db.cursor()
    sql = "lock tables "+ table_name +" write;" 
    try:
       print sql
       result = cursor.execute(sql)
       db.commit()
    except Exception,e:
       print "Error lock failed" 
       print e
       db.rollback()
    finally:
       db.close()

def unlock():
    db = connection()
    cursor = db.cursor()
    sql = "unlock tables"
    try:
       print sql
       result = cursor.execute(sql)
       db.commit()
       print result
    except Exception,e:
       print "Error lock failed"
       print e
       db.rollback()
    finally:
       db.close()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        command = sys.argv[1]
        print command
        if command == None:
             print "参数错误: query,update,lock"
             sys.exit()
        if command == "query" or command == "update" or command == "insert":
             param = sys.argv[2]
             state = int(param)
             if command == "query":
                 print "======查询====="
                 task = select(state)
                 print task.id,task.state,task.avaliable_time
             if command == "update":
                 task = select(1)
                 print "======更新 进行中====="
                 count = update(state=1,update_time=task.avaliable_time,id=task.id)
                 print count==1
                 print "======更新完成 ===="
                 count = update(state=2,update_time=task.avaliable_time,id=task.id)
                 print count==1
             if command == "insert":
                 task = select(state)
                 task.id = None
                 count = insert(task) 
                 print count==1
        elif command == "lock":
             param = sys.argv[2]
             table_name = param
             if table_name != None:
                 print table_name + "locked!" 
                 lock(table_name)
             else:
                 print "请输入表名"
                 sys.exit()
        else:
            print "不支持的命令"
    else:
        print "for example : python dao.py query 1 "
        sys.exit()
