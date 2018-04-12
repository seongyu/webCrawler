import database.mongodb as MDB
import dataSource.bithumb_c as connect_b
import dataSource.investf_c as connect_n
import dataSource.nf_c as connect_k
import dataSource.te_c_v1 as connect_s

import threading
import time
from lib.log import LOG
log = LOG()

cc_cw = connect_b.Crawler()
nasdaq_cw = connect_n.Crawler('NYSE')
k_cw = connect_k.Crawler()

start = True
n = 0

class spmThread(threading.Thread):
    def __init__(self, threadID, name, DB):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.DB = DB
    def run(self):
        connect_s.Crawler(self.DB)

class sbmThread(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.DB = DB
    def run(self):
        while True:
            time.sleep(self.counter)
            row = cc_cw.spider()
            if row:
                print(row)
                
class nsdThread(threading.Thread):
    def __init__(self, threadID, name, counter, DB):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.DB = DB
        self.n = 0
    def run(self):
        while True:
            time.sleep(self.counter)
            row = nasdaq_cw.spider()
            if row:
                print(row)
                self.n = self.n+1
                
class krxThread(threading.Thread):
    def __init__(self,threadID,name,counter,DB):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.DB = DB
        self.n = 0
    def run(self):
        while True:
            time.sleep(self.counter)
            row = k_cw.spider(0)
            if row:
                self.DB.add(row,'krx')
                
class ksdThread(threading.Thread):
    def __init__(self,threadID,name,counter,DB):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.DB = DB
        self.n = 0
    def run(self):
        while True:
            time.sleep(self.counter)
            row = k_cw.spider(1)
            if row:
                self.DB.add(row,'kosdaq')

if __name__ == "__main__":
#     DB = MDB.DB('test')
    # DB = MDB.DB('M')
    log.w('info','Total service started...')
    # thread1 = spmThread(1,'spmThread', DB)
    thread2 = sbmThread(2,'sbmThread',30)
    # thread3 = nsdThread(3,'nsdThread',10,DB)
    # thread4 = krxThread(4,'krxThread',10,DB)
    # thread5 = ksdThread(5,'ksdThread',10,DB)
    # thread1.start()
    # thread2.start()
    thread3.start()
    # thread4.start()
    # thread5.start()