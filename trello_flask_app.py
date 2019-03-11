from flask import Flask, request
import telepot
import urllib3

from trello_parser import get_status
from settings import *

proxy_url = "http://proxy.server:{}".format(PORT)
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(BOT_KEY)
bot.setWebhook("https://whereismyguts.pythonanywhere.com/{}".format(FLASK_SECRET), max_connections=5)

app = Flask(__name__)

@app.route('/{}'.format(FLASK_SECRET), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = get_status()
        chat_id = update["message"]["chat"]["id"]
        # print('chat', chat_id)
        bot.sendMessage(chat_id, text)
    return "OK"
