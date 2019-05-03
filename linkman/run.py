
import os
import sys

import tornado.ioloop
import tornado.web
import random
import json
from linkman.mongo import (
    add_link, get_cards, 
    remove_doc, 
    change_card, add_card,
)
from linkman.settings import *
import time


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self, *args, **kwargs):
        # time.sleep(3)
        # print(self.request.body)
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json.loads(self.request.body)
    # Access self.args directly instead 1of using self.get_argument.

    def write_data(self):
        cards = get_cards()
        self.write(dict(
            cards=cards,
            username='me',
        ))


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class RemoveItemHandler(BaseHandler):
    def post(self, *args, **kwargs):
        remove_doc(self.args['id'])

        self.write_data()


class ChangeCardHandler(BaseHandler):
    def post(self, *args, **kwargs):
        change_card(self.args['id'], self.args['title'], self.args['desc'])

        self.write_data()


class AddLinkHandler(BaseHandler):

    def post(self, *args, **kwargs):
        # print("ARGS: ", self.args)
        add_link(self.args['id'], self.args['url'], self.args['text'])
        self.write_data()


class AddCardHandler(BaseHandler):

    def post(self, *args, **kwargs):
        # print("ARGS: ", self.args)
        add_card(self.args['title'], self.args['desc'])
        self.write_data()


class HelloHandler(BaseHandler):

    @property
    def mock_cards(self):
        return {
            'username': 'Вася',
            'cards': [{
                'title': 'Awesome card',
                'desc': "some common work links",
                'links': random.randint(3, 9)*[
                    {'text': 'link1 text', 'url': 'https://ya.ru'},
                ],
            } for i in range(random.randint(3, 9))]
        }

    def post(self, *args, **kwargs):
        self.write_data()
        # self.write(self.mock_cards)
        # self.write({'hello': 'really?'})

HANDLERS = [
    (r"/", MainHandler),
    (r".*/api/hello", HelloHandler),
    (r".*/api/add_link", AddLinkHandler),
    (r".*/api/remove_item", RemoveItemHandler),
    (r".*/api/change_card", ChangeCardHandler),
    (r".*/api/add_card", AddCardHandler),
]


def make_app():
    # print(os.path.join(os.path.dirname(__file__), "public"))
    return tornado.web.Application(
        template_path=os.path.join(os.path.dirname(__file__), "views"),
        static_path=os.path.join(os.path.dirname(__file__), "public"),
        debug=True,
        handlers=HANDLERS,
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
