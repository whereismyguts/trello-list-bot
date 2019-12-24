from flask import Flask, fl_request

from flask import Flask, request
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import OrderedWebhook
import urllib3

from trello_parser import get_status
from settings import *

proxy_url = "http://proxy.server:{}".format(PORT)
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
URL = "https://whereismyguts.pythonanywhere.com/{}".format(FLASK_SECRET)
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(
    proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
app = Flask(__name__)
IKB = InlineKeyboardButton

bot = telepot.Bot(BOT_KEY)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)


# need `/setinline`
def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)

    # Compose your own answers
    articles = [{'type': 'article',
                    'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

    bot.answerInlineQuery(query_id, articles)


# need `/setinlinefeedback`
def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


webhook = OrderedWebhook(
    bot,
    {
        'chat': on_chat_message,
        'callback_query': on_callback_query,
        'inline_query': on_inline_query,
        'chosen_inline_result': on_chosen_inline_result
    }
)




@app.route('/{}'.format(FLASK_SECRET), methods=["POST"])
def pass_update():
    webhook.feed(request.data)
    return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL, max_connections=5)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()

# @app.route('/{}'.format(FLASK_SECRET), methods=["POST"])
# def telegram_webhook():
#     update = request.get_json()
#     if "message" in update:
#         print(update["message"])

#         msg = update['message']
#         text = msg['chat']['text'].strip()
#         amount = int(text)
#         username = msg['from']['username']
#         chat_id = update["message"]["chat"]["id"]

#         user = User.get(User.username == username)

#         if not user:
#             user = User.create(
#                 username=username,
#                 telegram_id=msg['from']['id'],
#                 name=msg['from']['firstname'],
#             )
#             bot.sendMessage(chat_id, 'Welcome, {}'.format(user.name))
#             return 'OK'

#         buttons = None
#         if text.isdigit() and user.state == User.STATE_INIT:
#             answer = "Spend: {}.\n".format(text)
#             categories = Category.select().where(
#                 Category.user_id == user.id,
#                 Category.deleted == None,
#             )

#             if len(categories) == 0:
#                 answer += "No categories found. Please enter the name of the new category"
#                 user.state = User.STATE_CREATE_CATEGORY

#             else:
#                 buttons = [
#                     [IKB(
#                         text=cat.name,
#                         callback_data=cat.id,
#                     )] for cat in categories
#                 ]
#                 answer += "Select category"
#                 user.state = User.STATE_SELECT_CATEGORY

#             user.save()
#             bot.sendMessage(chat_id, answer, reply_markup=buttons and InlineKeyboardMarkup(
#                 inline_keyboard=buttons))
#             return 'OK'

#         bot.sendMessage(chat_id, 'endpoint reached')
#         return 'OK'

#         plans = Plan.select().where(
#             Plan.user_id == user.id,
#             Plan.deleted == None,
#         )

#         keyboard = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text='Press me', callback_data='press')],
#             ]
#         )
#         bot.sendMessage(chat_id, text, reply_markup=keyboard)
#     return "OK"
