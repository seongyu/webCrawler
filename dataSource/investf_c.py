# information
# Current Stock Collector : investing.com
# 화폐단위 : USD
# Country : USA
# Market Status Check :
#     NYSE => 뉴욕증시
#     London
#     Frankfurt
#     Hong Kong
#     Tokyo
#     Sydney
# Usage
# cw = Crawler('NYSE')
# rtn = cw.spider()

import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lib.log import LOG
log = LOG()

class Crawler:
    def __init__(self,MT):
        self.headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
        }
        self.items = []
        self.MT = MT
        self.check_market(MT)
        log.w('info','InvestFinance service started...')

    def get(self,url):
        source_code = requests.get(url,headers = self.headers)
        soup = []
        try :
            soup = BeautifulSoup(source_code.text,'lxml')
        except Exception as err:
            log.w('error','InvestFinance : Request parse error => ',err)
        return soup

    def post(self,url,data):
        source_code = requests.post(url, headers = self.headers, data = data)
        soup = []
        try :
            soup = source_code.json()
        except Exception as err:
            log.w('error','InvestFinance : Request parse error => ',err)
        return soup

    def check_market(self,MT):
        url = 'https://www.investing.com/markets/MarketsTopBarMenu'
        soup = self.get(url)
        for mlist in soup.find_all(class_='data'):
            ls = mlist.text
            if ls.find(MT) == 0 :
                if ls.find('Closes') >= 0 : 
                    self.is_alive=True
                else :
                    self.is_alive=False
                break

    def spider(self):
        arr = []
        self.check_market(self.MT)
        self.cw_start = True
        page=1
        total_page = 0
        if self.is_alive :
            time_now = datetime.now()
            while self.cw_start:
                url = 'https://www.investing.com/stock-screener/Service/SearchStocks'
                data = 'country%5B%5D=5&exchange%5B%5D=2&pn='+str(page)+'&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d'
                try:
                    lists = self.post(url,data)
                    if total_page == 0 :
                        total_page = round(lists['totalCount']/len(lists['hits']))
                    elif page==total_page :
                        self.cw_start = False
                    for ls in lists['hits']:
                        item = {'i':'','t':'','c':0,'v':0,'e':''}
                        item['i']=ls['exchange_trans']+':'+ls['stock_symbol']
                        item['c']= ls['last'] if ls['last'] else None
                        item['t'] = time_now
                        item['v']= ls['turnover_volume'] if ls['turnover_volume'] else None
                        item['e']= ls['name_trans'] if ls['name_trans'] else None
                        arr.append(item)
                    page+=1
                except Exception as err:
                    log.w('error','InvestFinance : error in parse => ',err)
                    pass
        else :
            time.sleep(10*60)
        return arr