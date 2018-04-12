# information
# Current Digital currency Collector : Bithumb
# 화폐단위 : KRW/(coin)
# Country : USA
# ItemList
#     BTC = Bitcoin
#     ETH = Ether Leeum
#     DASH = dash
#     LTC = Litecoin
#     ETC = Ether Solarium Classic
#     XRP = ripple
# Usage
# cw = Crawler()
# rtn = cw.spider()

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from lib.log import LOG
log = LOG()

class Crawler:
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            }
        self.url = 'https://api.bithumb.com/public/ticker/ALL'
        self.items = []
        log.w('info','DigitalCash service started...')

    def get(self,url):
        source_code = requests.get(url,headers = self.headers)
        soup = []
        try :
            soup = BeautifulSoup(source_code.text,'lxml')
        except Exception as err:
            log.w('error','DigitalCash : Request parse error => ',err)
        return soup

    def post(self,url):
        source_code = requests.get(url, headers = self.headers)
        result = []
        try : 
            if str(source_code).index('200')>0 :
                result = source_code.json()
            else :
                result['status'] = '-1'
        except Exception as err :
            log.w('error','DigitalCash : Request error => '+str(source_code)+' => ',err)
            result['status'] = '-1'
            pass
        return result

    def spider(self):
        url = self.url
        rtn = self.post(url)
        time = datetime.now()
        arr = []
        try:
            if rtn['status']=='0000':
                    itlist = rtn['data']
                    arr = [
                        {
                            'code':'BTC',
                            'buy_p':int(float(itlist['BTC']['buy_price'])),
                            'sel_p':int(float(itlist['BTC']['sell_price'])),
                            'avr_p':int(float(itlist['BTC']['average_price'])),
                            'time':time
                            },
                        {'code':'ETH','buy_p':int(float(itlist['ETH']['buy_price'])),'sel_p':int(float(itlist['ETH']['sell_price'])),'avr_p':int(float(itlist['ETH']['average_price'])),'time':time},
                        {'code':'DASH','buy_p':int(float(itlist['DASH']['buy_price'])),'sel_p':int(float(itlist['DASH']['sell_price'])),'avr_p':int(float(itlist['DASH']['average_price'])),'time':time},
                        {'code':'LTC','buy_p':int(float(itlist['LTC']['buy_price'])),'sel_p':int(float(itlist['LTC']['sell_price'])),'avr_p':int(float(itlist['LTC']['average_price'])),'time':time},
                        {'code':'ETC','buy_p':int(float(itlist['ETC']['buy_price'])),'sel_p':int(float(itlist['ETC']['sell_price'])),'avr_p':int(float(itlist['ETC']['average_price'])),'time':time},
                        {'code':'XRP','buy_p':int(float(itlist['XRP']['buy_price'])),'sel_p':int(float(itlist['XRP']['sell_price'])),'avr_p':int(float(itlist['XRP']['average_price'])),'time':time}
                    ]
        except Exception as err:
                log.w('error','DigitalCash : error in parse => ',err)
                pass
        return arr
    
    
