from flask import Flask, request, jsonify
from model import get_prediction
from flask import Response

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    if request.method == "POST":
        request_json = request.get_json()
        predict_freq = request_json['predict_freq']
        duration = request_json['duration']

        response = get_prediction(predict_freq, duration)

    return Response(response, mimetype='application/json')
  

@app.route('/')
def index():
    return "<h1>Welcome to e-manager-model server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)