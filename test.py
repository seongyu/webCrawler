import requests
from bs4 import BeautifulSoup
from datetime import datetime


def post(url,data):
    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }
    source_code = requests.post(url, headers = headers, data = data)
    soup = []
    try :
        soup = source_code.json()
    except Exception as err:
        log.w('error','InvestFinance : Request parse error => ',err)
    return soup

def spider():
    arr = []
    cw_start = True
    page=1
    total_page = 0
    time_now = datetime.now()
#     while cw_start:
    url = 'https://www.investing.com/stock-screener/Service/SearchStocks'
    data = 'country%5B%5D=5&exchange%5B%5D=2&pn='+str(page)+'&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d'
    try:
        lists = post(url,data)
        print(lists)
        print(lists['totalCount'])
        print(len(lists['hits']))
        
#             if total_page == 0 :
#                 total_page = round(lists['totalCount']/len(lists['hits']))
#             elif page==total_page :
#                 cw_start = False
#             for ls in lists['hits']:
#                 item = {'i':'','t':'','c':0,'v':0,'e':''}
#                 item['i']=ls['exchange_trans']+':'+ls['stock_symbol']
#                 item['c']= ls['last'] if ls['last'] else None
#                 item['t'] = time_now
#                 item['v']= ls['turnover_volume'] if ls['turnover_volume'] else None
#                 item['e']= ls['name_trans'] if ls['name_trans'] else None
#                 arr.append(item)
#             page+=1
    except Exception as err:
        log.w('error','InvestFinance : error in parse => ',err)
        pass
    return arr

spider()