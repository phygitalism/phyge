from flask import Flask, request, Response
import json
from pprint import pprint
from SearchEngine import SearchEngine, ServerState
from Models.Query import Query

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
    queries = [Query({'text': query_text, 'id': 1})]
    print('MODEL', search_articles['model'])
    search_lsi = SearchEngine(query=queries, test_case_id=4, model_name='lsi')
    search_lda = SearchEngine(query=queries, test_case_id=4, model_name='lda')
    if search_lsi.server_state == ServerState.Stop:
        print("\nCan't start server, model didn't loaded\n")
        search_lsi.train_model()
    if search_lda.server_state == ServerState.Stop:
        print("\nCan't start server, model didn't loaded\n")
        search_lda.train_model()
    else:
        print("\nStart server\n")
        answer_lsi = search_lsi.get_answers(amount=amount)
        answer_lda = search_lda.get_answers(amount=amount)
        models_answer = {'lda': answer_lda[0]["answer_articles"], 'lsi': []}
    print('models answer')
    pprint(models_answer)
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
    # tematic_models = TematicModels(test_number=PhyVariables.currentTestKey)
    app.run(host='0.0.0.0', port=5050, threaded=True)
