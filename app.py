import flask
from flask import Flask, request, render_template
import json
import Main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        global this_query
        global this_keyword
        query = request.json['input_question']
        keyword = request.json['input_keyword']
        this_query = query
        this_keyword = keyword
        json_info_str = Main.main(query, keyword)
        json_info = json.loads(json_info_str, strict=False)
        # print(type(json_info))
        predictions = []
        snippet = []
        paper_id = []
        for i in json_info["results"]:
            # print(type(i))
            predictions.append(i['predictions'])
            snippet.append(i['snippet'])
            paper_id.append(i['paper_identifier'])

        res = {'snippet': snippet,
                'pdf_link': paper_id,
                'predictions': predictions}

        return flask.jsonify(res)

    except Exception as error:
        bad_res = str(error)
        return app.response_class(response=json.dumps(bad_res), status=500, mimetype='application/json')


@app.route('/feedback', methods=['POST'])
def collect_feedback():
    try:
        feedback = request.json['feedback']
        Main.save_feedback(this_keyword, this_query, feedback)
    except Exception as error:
        bad_res = str(error)
        return app.response_class(response=json.dumps(bad_res), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)