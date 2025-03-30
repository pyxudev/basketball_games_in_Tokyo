import json
import asyncio
import datetime
from flask import *
from flask_cors import CORS
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
itemId = 0

def getsoup(url):
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except Exception as e:
        return '404'

def getdetails(soup):
    global itemId
    lis = soup.select('#main-list > li')
    res = {}
    for li in lis:
        detail_keys = li.select('.clearfix > dt')
        detail_values = li.select('.clearfix > dd')
        link = li.select('.clearfix > dd > a')[0].get('href')
        itemId += 1
        details = {}
        jsonKeys = ['teamname', 'requirements', 'time', 'address']
        for i in range(0, len(detail_keys)-1):
            details[jsonKeys[i]] = detail_values[i].text
        details['link'] = 'https://www.net-menber.com' + link
        res[str(itemId)] = details

    return res

async def getGames(kw):
    url_base = 'https://www.net-menber.com/list/baske/index.html?ken='
    kens = {'東京':8, '埼玉':10, '千葉':11}
    res = {'0': 'Dammy'}
    for ken, num in kens.items():
        url = url_base + str(num) + "&q=" + quote(kw)
        soup = getsoup(url)
        if soup == '404':
            continue
        pager = soup.select('.pager')[0].select('li > a')
        pages = len(pager)
        if pages == 0:
            res = {**res, **getdetails(soup)}
        else:
            for page in range(0, pages):
                url += "&p=" + str(page+1)
                soup = getsoup(url)
                res = {**res, **getdetails(soup)}
    return res

@app.route('/search/<string:text>', methods=["GET"])
def reqindex(text):
    dt = datetime.datetime.now()
    print(str(dt.hour) + ':' + str(dt.minute) + ' ' + text)
    loop = asyncio.new_event_loop()
    lists = loop.run_until_complete(getGames(text))
    print(lists)
    global itemId
    itemId = 0

    return json.dumps(lists,  ensure_ascii=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)