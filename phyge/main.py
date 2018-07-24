from flask import Flask, request, Response
import json
import time

from pprint import pprint
from SearchEngine import SearchEngine
from Models.Query import BaseQuery

from DatabaseSeeder import DatabaseSeeder
from DBController import DBController

from Models.TrainingSample import TrainingSample
from Storage import Storage
from TematicModels import LsiModel, LdaModel

app = Flask(__name__)
logging_enabled = False

search_engine: SearchEngine = None


@app.route('/')
def index():
    return Response('Server is running', status=200)


@app.route('/search_articles', methods=['POST'])
def search_articles():
    global search_engine
    request_body = request.json
    print('search_articles: ', request_body)
    query_text = request_body['query']
    amount = request_body['amount']
    query = BaseQuery({'text': query_text, 'id': 1})

    start_time = time.time()
    search_results = search_engine.find_article(query, amount=amount)
    answer_time = round((time.time() - start_time), 3)
    search_results['search_time'] = answer_time

    print('search_results')
    pprint(search_results)
    return Response(json.dumps(search_results, ensure_ascii=False), status=200, mimetype='application/json')


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global search_results
    check_answer = request.json
    log_of_result.append(dict(check_answer, **search_results))
    pprint(log_of_result)

    response_body = dict(control='Answer saved.')
    return Response(json.dumps(response_body), status=200, mimetype='application/json')


if __name__ == "__main__":
    log_of_result = []

    if len(DBController.get_all_articles()) == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()

    lsi = Storage.load_model('out/lsi', 'phydge', 'lsi')
    lda = Storage.load_model('out/lda', 'phydge', 'lda')

    search_engine = SearchEngine(models=[lsi, lda])

    app.run(host='0.0.0.0', port=5050, threaded=True)
