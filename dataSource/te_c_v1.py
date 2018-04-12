# information
# Spot Market Collector : TradingEconomics
# 화폐단위 : USD
# output : resource/*.json
# WorkFlow : 
# Before connect socketIO open file with append mode,
#  append each row to file when get response from socket
import datetime
import time
import websocket
import json
from lib.log import LOG
log = LOG()

te_url = "ws://stream.tradingeconomics.com/" 
client_key = "guest" #API_CLIENT_KEY
client_secret = "guest" #API_CLIENT_KEY

class Crawler:
    def __init__(self,DB):
        self.url = "ws://stream.tradingeconomics.com/" 
        self.key = "guest" #API_CLIENT_KEY
        self.secret = "guest" #API_CLIENT_KEY
        websocket.enableTrace(False)
        self.db = DB
        self.start_sc()
        
    def start_sc(self):
        self.ws = websocket.WebSocketApp(self.url + "?client=" + self.key + ":" + self.secret,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close
                                )
        self.ws.on_open=self.on_open
        self.ws.run_forever()
        log.w('info','Websocket service started...')

    def on_message(self, ws, message):
        row = json.loads(message)
        try:
            if row['dt']:
                try:    
                    row['dt'] = datetime.datetime(*time.localtime(row['dt']*0.001)[:6])
                    self.db.add_stream(row)
                except Exception as err:
                    log.w('error','TradingEconomics : Save db with timestamp => ',err)
        except:
            pass

    def on_error(self, ws, error):
        ws.close()
        log.w('error',"TradingEconomics : ",error)
        self.start_sc()

    def on_close(self, ws):
        ws.close()
        log.w('error',"TradingEconomics : Socket closed")
        self.start_sc()

    def on_open(self, ws):
        ws.send(json.dumps({"topic": "subscribe", "to": "commodities"}))
#         ws.send(json.dumps({"topic": "subscribe", "to": "currencies"}))