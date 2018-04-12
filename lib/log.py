import logging
import logging.handlers
import datetime
import os.path

class LOG:
    def __init__(self):
        self.logger = self.ready()
        logging.getLogger("requests").setLevel(logging.WARNING)
        
    def w(self,lv,msg,v=''):
        if lv == 'info' : ac = 20
        elif lv == 'error' : ac = 40
        elif lv == 'warning' : ac = 30
        elif lv == 'debug' : ac = 10
        elif lv == 'critical' : ac = 50
        self.logger.log(ac,msg+str(v))
        
    def ready(self):
        directory = 'log/'
        filename = str(datetime.date.today())+'.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        logger = logging.getLogger()
        fileHandler = logging.handlers.TimedRotatingFileHandler(directory+filename,'midnight',1)
        logger.addHandler(fileHandler)
        
        return logger