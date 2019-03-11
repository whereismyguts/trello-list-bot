import telepot
import urllib3
import time
import datetime
from trello_parser import get_status
from settings import *

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(
    proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


bot = telepot.Bot(BOT_KEY)
bot.setWebhook(
    "https://whereismyguts.pythonanywhere.com/{}".format(FLASK_SECRET), max_connections=1)

chat_id = 258610595
hour_in_secs = 60*60

if __name__ == "__main__":
    now = datetime.datetime.utcnow()+datetime.timedelta(hours=3)
    if now.weekday() in [5, 6]:
        bot.sendMessage(chat_id, 'its da weekend!! '+str(now))
        exit()

    while True:
        now = datetime.datetime.utcnow()+datetime.timedelta(hours=3)
        if now.hour > 20:
            bot.sendMessage(chat_id, 'It\'s time to stop working. Bye.')
            exit()

        # if now.hour in [9, 13, 17]:
        text = get_status()
        bot.sendMessage(chat_id, text)

        time.sleep(hour_in_secs/60)
