from pymongo import MongoClient
from lib.log import LOG
# url = '13.124.143.112:27017'
url = 'localhost:27017'
log = LOG()

class DB:
    def __init__(self,database):
        client = MongoClient(url)
        self.db = client[database]
        self.stream = 'streaming'
        log.w('info','Ready to DataBase')
        
    def add(self,row,collection):
        try:
            self.db[collection].insert(row)
        except Exception as err:
            log.w('error','Database : add => ',err)
        
    def add_stream(self,row):
        try:
            self.db[self.stream].insert(row)
        except Exception as err:
            log.w('error','Database : add_stream => ',err)