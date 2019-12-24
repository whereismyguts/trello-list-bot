from flask import Flask, fl_request
import telepot
import urllib3

from trello_parser import get_status
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
from settings import *

proxy_url = "http://proxy.server:{}".format(PORT)
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(BOT_KEY)
bot.setWebhook("https://whereismyguts.pythonanywhere.com/{}".format(FLASK_SECRET), max_connections=5)

app = Flask(__name__)


class BaseHandler():
    
    def __init__(self, data):
        self.data = data
    
    @property
    def event(self):
        if 'message' in self.data:
            return 'message'
        if 'callback_query' in self.data:
            return 'press'

    def handle_message(self):
        self._handle_message(self.data['message']['chat']['text'])

    def handle_press(self):
        buttons = sum(self.data['message']['chat']['text']['reply_markup']['inline_keyboard'])
        button_id = filter(lambda b: b['callback_data'] == self.data['callback_query']['data'])[0]

        self._handle_press(buttons, button_id)

    def handle(self):
        if self.event == 'message':
            self.handle_message()

        if self.event == 'press':
            self.handle_press()
        return 'OK'

    def send(self, text):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Press me', callback_data='press1')],
                [InlineKeyboardButton(text='Press me too', callback_data='press2')],
            ]
        )
        self.bot.sendMessage(self.chat_id, text, reply_markup=keyboard)

    @property
    def chat_id(self):
        return self.data['message']['chat']['id']


class FinacialHandler(BaseHandler):

    def _handle_message(self, text):
        print(text)
        self.send('texted: {}'.format(text))

    def _handle_press(self, buttons, button_id):
        print(buttons[button_id])
        self.send('pressed: {}'.format(buttons[button_id]))


@app.route('/{}'.format(FLASK_SECRET), methods=["POST"])
def telegram_webhook():
    handler = FinacialHandler(fl_request.get_json(), bot)
    return handler.handle()

    # if "message" in update:
    #     print(update["message"])

    #     msg = update['message']
    #     text = msg['chat']['text'].strip()
    #     amount = int(text)
    #     username = msg['from']['username']
    #     chat_id = update["message"]["chat"]["id"]

    #     user = User.get(User.username == username)

    #     if not user:
    #         user = User.create(
    #             username=username,
    #             telegram_id=msg['from']['id'],
    #             name=msg['from']['firstname'],
    #         )
    #         bot.sendMessage(chat_id, 'Welcome, {}'.format(user.name))
    #         return 'OK'

    #     buttons = None
    #     if text.isdigit() and user.state == User.STATE_INIT:
    #         answer = "Spend: {}.\n".format(text)
    #         categories = Category.select().where(
    #             Category.user_id == user.id,
    #             Category.deleted == None,
    #         )

    #         if len(categories) == 0:
    #             answer += "No categories found. Please enter the name of the new category"
    #             user.state = User.STATE_CREATE_CATEGORY

    #         else:
    #             buttons = [
    #                 [IKB(
    #                     text=cat.name,
    #                     callback_data=cat.id,
    #                 )] for cat in categories
    #             ]
    #             answer += "Select category"
    #             user.state = User.STATE_SELECT_CATEGORY

    #         user.save()
    #         bot.sendMessage(chat_id, answer, reply_markup=buttons and InlineKeyboardMarkup(
    #             inline_keyboard=buttons))
    #         return 'OK'

    #     bot.sendMessage(chat_id, 'endpoint reached')
    #     return 'OK'

    #     plans = Plan.select().where(
    #         Plan.user_id == user.id,
    #         Plan.deleted == None,
    #     )

    #     keyboard = InlineKeyboardMarkup(
    #         inline_keyboard=[
    #             [InlineKeyboardButton(text='Press me', callback_data='press')],
    #         ]
    #     )
    #     bot.sendMessage(chat_id, text, reply_markup=keyboard)
    # return "OK"