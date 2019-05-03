from mongoengine import *
from settings import (
    MONGO_DB, MONGO_PASS, MONGO_USER
)

import datetime
print('mongo')


class BaseDoc(Document):
    removed = DateTimeField()
    meta = {'allow_inheritance': True}

    def _ser():
        return {}

    def ser(self):
        res = dict(
            is_edit=False,
            link_adding=False,
            is_minimized=False, # TODO save
        )
        res.update(self._ser())
        return res


class Link(BaseDoc):
    url = StringField()
    text = StringField()

    def _ser(self):
        return dict(
            url=self.url,
            text=self.text,
            id=str(self.id),
        )


class Card(BaseDoc):
    title = StringField()
    desc = StringField()
    links = ListField(ReferenceField(Link))

    def _ser(self):
        return dict(
            title=self.title,
            desc=self.desc,
            links=[l.ser() for l in self.links if not l.removed],
            id=str(self.id),
            # new_link_url='xxx',
            # new_link_text='yyy',
        )


def add_card(title='', desc='', **kwargs):
    card = Card(title=title, desc=desc)
    return card.save()

def clean():
    docs = BaseDoc.objects()
    for doc in docs:
        if doc.removed:
            doc.delete()

def change_card(id, title, desc):
    card = Card.objects.get(id=id)
    card.title = title
    card.desc = desc
    card.save()

def add_link(id, url, text):
    card = Card.objects.get(id=id)
    if not (url.lower().startswith('http') or url.startswith('file')):
        url = 'https://' + url
    card.links.append(Link(url=url, text=text).save())
    card.save()


def remove_doc(id):
    doc = BaseDoc.objects.get(id=id)
    if doc:
        remove(doc)

def remove(doc):
    doc.removed = datetime.datetime.utcnow()
    return doc.save()


def create_connection():
    connect(
        db=MONGO_DB,
        username=MONGO_USER,
        password=MONGO_PASS,
        host='mongodb://{}:{}@ds263295.mlab.com:63295/{}'.format(
            USERNAME, PASS, DB,
        )
    )


def get_cards():
    create_connection()
    return [c.ser() for c in Card.objects(removed=None) if c.id]


if __name__ == '__main__':

    clean()
    cards = Card.objects(removed=None)
    print(len(cards))
    # print(cards)
    # remove(cards[0])

    #card = create_card('New card', 'fock you')
    # add_link(cards[0].id, 'sdfsdfo', 'sdfsdfsber')
    #vprint(cards[0].links)





