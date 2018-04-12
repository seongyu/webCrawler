# information
# Current Stock Collector : Naver Finance
# 화폐단위 : KRW
# Code : 0 => KRX, 1 => KOSDAQ
# Usage : 
# cw = Crawler()
# rtn = cw.spider(0 or 1)
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lib.log import LOG
log = LOG()

class Crawler:
    def __init__(self):
        self.cw_start = True
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534+ (KHTML, like Gecko) BingPreview/1.0b'
        }
        self.items = []
        self.check_market()
        log.w('info','NaverFinance service started...')

    def get(self,url):
        source_code = requests.get(url,headers = self.headers)
        soup = []
        try :
            soup = BeautifulSoup(source_code.text,'lxml')
        except Exception as err:
            log.w('error','NaverFinance : Request parse error => ',err)
        return soup

    def check_market(self):
        url = 'http://finance.naver.com/sise'
        soup = self.get(url)
        status = soup.select_one('#time1 > span').text
        if status.find('장중') == 0 :
            self.is_alive = True
        else :
            self.is_alive = False

    def spider(self,code):
        self.check_market()
        arr = []
        if code==0:
            code_name = 'KRX'
        elif code==1:
            code_name = 'KOSDAQ'
        self.cw_start = True
        page=1
        if self.is_alive :
            now_time = datetime.now()
            while self.cw_start:
                url='http://finance.naver.com/sise/sise_market_sum.nhn?sosok='+str(code)+'&page='+str(page)
                soup = self.get(url)
                craw_items = soup.find_all(class_='no')
                if len(craw_items) > 0 :
                    try :
                        for no in craw_items:
                            li = no.find_next_siblings('td')
                            item = {'i':'','t':'','c':0,'v':0,'e':''}
                            href = li[0].select_one('a')['href']
                            item['i']=code_name+href[href.index('code=')+5:]
                            item['c']= li[1].text
                            item['t'] = now_time
                            item['v']= li[8].text
                            item['e']= li[0].text
                            arr.append(item)
                        page+=1
                    except Exception as err:
                        log.w('error','NaverFinance : error in parse => ',err)
                else :
                    self.cw_start = False
        else :
            time.sleep(10*60)
        return arr