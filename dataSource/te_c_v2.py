# information
# Spot Market Collector : TradingEconomics
# 화폐단위 : USD
# output : resource/*.json
# WorkFlow : 
# Add each row to Array when IO send message.
# Write the array to file each 1 minute and clear it. 

import datetime
import websocket
import _thread
import time
import json

write_timeout = 60

class Crawler:
    def __init__(self):
        self.url = "ws://stream.tradingeconomics.com/" 
        self.key = "guest" #API_CLIENT_KEY
        self.secret = "guest" #API_CLIENT_KEY
        self.filename = self.get_file_name()
        self.arr = []

        websocket.enableTrace(True)
        _thread.start_new_thread(self.save_file, ('saveThread',self.arr))
        print('start thread')
        self.start_sc()

    def start_sc(self):
        self.ws = websocket.WebSocketApp(self.url + "?client=" + self.key + ":" + self.secret,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close
                                )
        self.ws.on_open=self.on_open
        self.ws.run_forever()

    def on_message(self, ws, message):
#         print('write file : '+self.filename+', count :',len(self.arr))
        self.arr.append(message+',\n')

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send(json.dumps({"topic": "subscribe", "to": "commodities"}))

    def get_file_name(self):
        dt = datetime.date.today()
        return dt.isoformat()+'_dump'

    def save_file(self,threadNm,arr):
        while True:
            time.sleep(write_timeout)
            print('insert file...')
            if self.filename != self.get_file_name():
                print('End todays writing...')
                self.filename = self.get_file_name()
            try :
                with open('../resource/'+self.filename,'a') as f:
                    for line in arr :
                        f.write(line)
                self.arr = []
            except:
                print('save file error')

Crawler()