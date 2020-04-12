"""
To run this app, in your terminal:
> python query_tool_api.py
"""
import connexion
from flask import render_template
from sklearn.externals import joblib
import Main     # local module

# Instantiate our Flask app object
app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
application = app.app

# Load our pre-trained model
#model = joblib.load('./model/iris_classifier.joblib')


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:8080/
    :return:        the rendered template 'home.html'
    """
    return render_template('templates/home.html')


# Implement a simple health check function (GET)
def health():
    # Test to make sure our service is actually healthy
    sample_query = ''

    try:
        predict(sample_query)
    except:
        return {"Message": "Service is unhealthy"}, 500

    return {"Message": "Service is OK"}


# Implement our predict function
def predict(query, topic='All'):
    # Accept the query and optional topic provided as part of our POST
    global this_query
    global this_topic

    this_query = query
    this_topic = topic

    # Pass query and topic to Main controller
    paper_id, snippets = Main.main(this_query, this_topic)

    # Use as input to model.predict()
    #res = model.predict([[query]])

    # Return the prediction as a json
    return {"paper": paper_id, "relevant snippets": snippets}


# Implement our feedback function
def feedback(ranking):
    # Accept the user's ranking provided as part of our POST
    # Pass ranking to Main controller
    Main.save_feedback(this_topic, this_query, ranking)

    return {"Your feedback": ranking}


# Read the API definition for our service from the yaml file
app.add_api("query_tool_api.yaml")

# Start the app
if __name__ == "__main__":
    app.run()
