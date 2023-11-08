#!/usr/bin/python
# -*- coding:UTF-8 -*-

from bitarray import bitarray
import mmh3

class BloomFilter(object):

    def __init__(self,size=2**20,seeds=None):
        if size == None:
            self.size = 2**20
        else:
            self.size = size
        self.bitset = bitarray(self.size)
        self.bitset.setall(False)
        if seeds == None:
            self.seeds = [5,7,11,13,31,67]
        else:
            self.seeds = seeds

    def notcontains(self,ele):
        for i in self.seeds:
            hash = mmh3.hash(ele,i) % self.size 
            if self.bitset[hash] == False:
                return True
        return False

    def add(self,ele):
        for i in self.seeds:
            hash = mmh3.hash(ele,i) % self.size
            self.bitset[hash] = True

#f = BloomFilter(2*20)
#f.add("123")
#print f.notcontains("123")
