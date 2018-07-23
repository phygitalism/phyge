from flask import Flask, request, Response
import json
from pprint import pprint
from SearchEngine import SearchEngine
from Models.Query import Query

from DatabaseSeeder import DatabaseSeeder
from DBController import DBController

from TrainingSample import TrainingSample
from TematicModels import LSImodel, LDAmodel, W2Vmodel

app = Flask(__name__)
logging_enabled = False

search_lsi: SearchEngine = None


@app.route('/')
def index():
    return Response('Server is running', status=200)


@app.route('/search_articles', methods=['POST'])
def search_articles():
    global search_lsi
    request_body = request.json
    print('search_articles: ', request_body)
    query_text = request_body["query"]
    amount = request_body["amount"]
    query = Query({'text': query_text, 'id': 1})
    search_results = search_lsi.find_article(query, amount=amount)
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

    testing_sample = TrainingSample()

    lsi = LSImodel(testing_sample)
    search_lsi = SearchEngine(model=lsi)

    app.run(host='0.0.0.0', port=5050, threaded=True)
