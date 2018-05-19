from flask import Flask, request, Response
from TematicModels import TematicModels
from pprint import pprint

import json

app = Flask(__name__)
logging_enabled = False
simulation_thread = None


@app.route('/')
def index():
    return Response('Server is running', status=200)


@app.route('/search_articles', methods=['POST'])
def search_articles():
    search_articles = request.json
    print(search_articles)
    query_text = search_articles["text"]
    amount = search_articles["amount"]
    tematic_models = TematicModels(TEST_NUMBER=3)
    lsi_answer = tematic_models.find_article(query_text, model='lsi', amount=amount)
    pprint(lsi_answer)

    lda_answer = tematic_models.find_article(query_text, model='lda', amount=amount)
    pprint(lda_answer)
    response_body = dict(lsi=lsi_answer, lda=lda_answer)
    return Response(json.dumps(response_body), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)
