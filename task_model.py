#!/usr/bin/python 
# -*- encoding:utf-8 -*-

class Task(object):

    def __init__(self,id,priority,type,state,link,avaliable_time,start_time,end_time):
        self.id = id
        self.priority = priority
        self.type = type
        self.state = state
        self.link = link
        self.avaliable_time = avaliable_time
        self.start_time = start_time
        self.end_time = end_time
