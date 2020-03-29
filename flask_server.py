import os
from flask import Flask
from model import get_prediction

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():

    if flask.request.method == "POST":
        data = get_prediction(predict_freq, duration)

    # return flask.jsonify(data)
    return data
    
if __name__ == '__main__':
    app.run()