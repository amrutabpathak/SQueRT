"""
To run this app, in your terminal:
> python query_tool_api.py
"""
import connexion
from sklearn.externals import joblib
import Main     # local module

# Instantiate our Flask app object
app = connexion.FlaskApp(__name__, port=8080, specification_dir='swagger/')
application = app.app

# Load our pre-trained model
#model = joblib.load('./model/iris_classifier.joblib')

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
    paper_id, snippet = Main.main(this_query, this_topic)

    # Use as input to model.predict()
    #res = model.predict([[query]])

    # Return the prediction as a json
    return {"prediction" : paper_id, snippet}

# Implement our feedback function
def feedback(ranking):
    # Accept the user's ranking provided as part of our POST
    # Pass ranking to Main controller
    Main.save_feedback(this_topic, this_query, ranking)

    return {"Your feedback" : ranking}

# Read the API definition for our service from the yaml file
app.add_api("query_tool_api.yaml")

# Start the app
if __name__ == "__main__":
    app.run()
