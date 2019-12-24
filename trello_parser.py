# -*- encoding: utf-8 -*-
import requests
from settings import *

status_wip = ['В работе', ]
status_wait = ['Уточнения', ]
status_done = ['Code Review', 'Test']
status_todo = ['TODO', 'Сервер']  # + status_wait


def get(path):
    #  print('get: ' + path)
    url = 'https://api.trello.com/1/{}?key={}&token={}'.format(
        path,
        TRELLO_KEY,
        TRELLO_TOKEN,
    )
    r = requests.get(url)
    return r.json()


def get_cards():
    return get(path='members/me/cards')


def get_lists(board_id):
    return get(path='boards/{}/lists'.format(board_id))


def get_boards():
    return get(path='members/me/boards')


def check_n_populate(ts_list, l_name, c_name, extra):
    for tl, sl in ts_list:
        if l_name in sl or any([l_name.startswith(s) for s in sl]):
            tl.append('{} {}'.format(c_name, extra))


def get_status(web=False):
    boards = ''
    if not boards:
        cards = get_cards()
        boards = {b['id']: dict(
            name=b['name'],
            lists=dict()
        ) for b in get_boards()}

        for b_id in boards:
            lists = get_lists(b_id)
            for l in lists:
                # if or l['name'] in my_lists:
                boards[b_id]['lists'][l['id']] = dict(
                    name=l['name'],
                    cards=list(),
                )

        for card in cards:
            board_id = card['idBoard']
            list_id = card['idList']
            board_lists = boards[board_id]['lists']
            if list_id in board_lists:
                lst = board_lists[list_id]
                crd = dict(
                    name=card['name'],
                    url=card['shortUrl']
                )
                lst['cards'].append(crd)

    result = ''

    b_id = 1
    for b in list(boards.values())[::-1]:
        board_block = ''
        t_id = 1
        if not b['lists']:
            continue
        todo_tasks = []
        wip_tasks = []
        done_tasks = []
        wait_tasks = []
        for l in b['lists'].values():
            if not l['cards']:
                continue
            extra = '(в работе)' if l['name'] in status_wip else ''  # (%s)' % l['name']
            for c in l['cards']:
                check_n_populate([
                    (todo_tasks, status_todo),
                    (wip_tasks, status_wip),
                    (done_tasks, status_done),
                    (wait_tasks, status_wait)
                ], l['name'], c['name'], extra)

        if todo_tasks or wip_tasks:  # or done_tasks:
            board_block += '\n\n' + b['name'] + ':\n'

        board_block, t_id = append_tasks(board_block, b_id, t_id, wip_tasks)  # , '  Делаю сегодня:')
        board_block, t_id = append_tasks(board_block, b_id, t_id, todo_tasks)
        board_block, t_id = append_tasks(
            board_block, b_id, t_id, wait_tasks, '\n-на уточнении-')
        if board_block:
            print('board id: {}'.format(b_id))
            print(board_block)
            print()
            b_id += 1
            result += board_block
        # if wip_tasks:
        #     result+='\n'+'  в работе:'
        #     for t in wip_tasks:
        #         result+='\n'+'  {}.{}'.format(i, t)
        #         i += 1
        #     result+='\n'
        # if todo_tasks:
        #     for t in todo_tasks:
        #         result+='\n'+'  {}.{}'.format(i, t)
        #         i += 1
        #     result+='\n'
    if web:
        result = result.replace('\n', '<br>---<br>')
    return result
    # if done_tasks:
    #     print('  done:')
    #     for t in done_tasks:
    #         print(' '*2+'{}.{}'.format('x', t))
    #     print()


def append_tasks(res, b_id, t_id, tasks, label=''):
    if tasks:
        res += label
        for t in tasks:
            res += '\n' + '{}.{}. {}'.format(b_id, t_id, t)
            t_id += 1
    return res, t_id


if __name__ == "__main__":
    print(get_status())

