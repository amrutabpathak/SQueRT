"""
To run this app, in your terminal:
> python query_tool_api.py
"""
import connexion
from sklearn.externals import joblib

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
def predict(query):
    # Accept the query provided as part of our POST
    # Use as input to model.predict()
    res = model.predict([[query]])

    # Return the prediction as a json
    return {"prediction" : res}

# Read the API definition for our service from the yaml file
app.add_api("query_tool_api.yaml")

# Start the app
if __name__ == "__main__":
    app.run()
