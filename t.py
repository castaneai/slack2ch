import re
import slackweb
from pyquery import PyQuery as pq

WEBHOOK = '<incoming webhook url>'


def filter_message(mes):
    # リンク置き換え
    mes = re.sub(r'<a href=.*>(.*)</a>', r'\1', mes)
    # 改行置き換え
    mes = mes.replace('<br/>', '\n')
    return mes


def parse_post(pqo):
    return {
        'number': int(pqo.attr('data-id')),
        'message': filter_message(pqo.find('.message').html()),
    }


def get_posts(html):
    return [parse_post(pqo) for pqo in html('.post').items()]

with open('bgs.html', encoding='cp932') as f:
    html = f.read()
posts = get_posts(pq(html))

slack = slackweb.Slack(url=WEBHOOK)
for p in posts[:-2]:
    print(p['message'])
    slack.notify(text=p['message'])



