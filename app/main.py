import json
import time
import os

from quart import Quart, request, Response

from pprint import pprint
from SearchEngine import SearchEngine
from Models.Query import BaseQuery

from DatabaseSeeder import DatabaseSeeder
from DBController import DBController

from Storage import Storage

app = Quart(__name__)

search_engine: SearchEngine = None

feature_toggles = {
    'save_search_results': True
}

if not os.path.exists('tmp'):
    os.makedirs('tmp')


@app.route('/')
async def index():
    return 'OK'


@app.route('/search_articles', methods=['POST'])
async def search_articles():
    global search_engine
    request_body = await request.get_json()
    print('search_articles: ', request_body)
    query_text = request_body['query']
    amount = request_body['amount']
    query = BaseQuery({'text': query_text, 'id': 1})

    start_time = time.time()
    search_results = await
    search_engine.find_article(query, amount=amount)
    answer_time = round((time.time() - start_time), 3)
    search_results['search_time'] = answer_time

    print('search_results')
    pprint(search_results)

    if feature_toggles['save_search_results']:
        file = open('tmp/history_request.txt', 'a')
        file.write('\n QUERY \n' + str(query_text) + ' \n RESPONSE \n' + str(search_results) + '\n_______\n\n\n')
        file.close()

    search_results['lda'] = []

    return Response(json.dumps(search_results, ensure_ascii=False), status=200, mimetype='application/json')


def check_db_status():
    db_len = 0
    for _ in DBController.get_all_articles():
        db_len += 1
    if db_len == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()


if __name__ == "__main__":
    log_of_result = []

    check_db_status()

    lsi = Storage.load_model('out/lsi', 'phyge', 'lsi')
    # lda = Storage.load_model('out/lda', 'phyge', 'lda')
    # d2v = Storage.load_model('out/d2v', 'phyge', 'd2v')

    search_engine = SearchEngine(models=[lsi])

    app.run(host='0.0.0.0', port=5050)
