import sys
import logging
import configparser
from telegram import Bot


#-----------------------------------------------------------Config SECTION ---------------------------------------------#
config = configparser.ConfigParser()
config.read('config.ini')
# Get the var values and set them for logging [logLevel - FORMAT - usingTelegram - BotToken(next section)]
log_level = getattr(logging, config.get('logging', 'level', fallback='DEBUG'))
FORMAT = config.get('logging', 'format', fallback='[+%(levelname)s] %(asctime)s | %(message)s | %(debugLine)s')
TeleUse = config.getboolean('telegram', 'use', fallback=False)

#-------------------------------------------------------TELEGRAM HANDLER SECTION --------------------------------------#
if TeleUse:
    def exitScript(): print('[+ERR]Sorry you use Telegram but you dont have token');sys.exit()
    BotToken = config.get('telegram', 'token', fallback=exitScript())
    bot = Bot(token=BotToken)

#-----------------------------------------------------------MAIN SECTION ----------------------------------------------#
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger('GadsLogger')
logger.setLevel(log_level)
#-----------------------------------------------------------ACT SECTION ----------------------------------------------#
class WarningFilter(logging.Filter):
    def filter(self, record):
        if TeleUse:
            bot.send_message(chat_id=000, message='message')

warning_handler = logging.StreamHandler()
warning_handler.setLevel(logging.WARNING)
warning_filter = WarningFilter()
warning_handler.addFilter(warning_filter)

# Add the handler to the logger
logger.addHandler(warning_handler)

#------------------------------------------------------------TEST SECTION----------------------------------------------#
# start = {'debugLine': 'line 19 - func'}
# logger.warning('this is true message',extra=start)
