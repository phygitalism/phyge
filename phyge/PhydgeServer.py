from flask import Flask, request, Response
import json
from pprint import pprint
from TematicModels import TematicModels

app = Flask(__name__)
logging_enabled = False
simulation_thread = None


@app.route('/')
def index():
    return Response('Server is running', status=200)


@app.route('/search_articles', methods=['POST'])
def search_articles():
    global models_answer
    search_articles = request.json
    print('search_articles: ', search_articles)
    query_text = search_articles["query"]
    amount = search_articles["amount"]
    query_vec = tematic_models.load_query_to_vec(query_text)
    lsi_answer = tematic_models.find_article(query_vec, model='lsi', amount=amount)
    print('\nLSI answer:')
    pprint(lsi_answer)

    lda_answer = tematic_models.find_article(query_vec, model='lda', amount=amount)
    print('\nLDA answer:')
    pprint(lda_answer)
    models_answer = dict(lsi=lsi_answer, lda=lda_answer)
    return Response(json.dumps(models_answer, ensure_ascii=False), status=200, mimetype='application/json')


@app.route('/check_answer', methods=['POST'])
def check_answer():
    global models_answer
    check_answer = request.json
    log_of_result.append(dict(check_answer, **models_answer))
    pprint(log_of_result)

    response_body = dict(control='Answer saved.')
    return Response(json.dumps(response_body), status=200, mimetype='application/json')


if __name__ == "__main__":
    log_of_result = []
    tematic_models = TematicModels(test_number=3)
    app.run(host='0.0.0.0', port=5050, threaded=True)
