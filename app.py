import flask
from flask import Flask, request, render_template
import json
#import Main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        query = request.json['input_question']
        keyword = request.json['input_keyword']
        #json_info = Main.main(query, keyword)

        predictions = []
        snippet = []
        paper_id = []
        for i in json_info["results"].keys():
            predictions.append(json_info["results"][i]['predictions'])
            snippet.append(json_info["results"][i]['snippet'])
            paper_id.append(json_info["results"][i]['paper_identifier'])

        res = {'snippet': snippet,
                'pdf_link': paper_id,
                'predictions': predictions}

        return flask.jsonify(res)

    except Exception as error:
        bad_res = str(error)
        return app.response_class(response=json.dumps(bad_res), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)
