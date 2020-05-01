from flask import Flask, request, jsonify, render_template
from joblib import load

model = load("clf.joblib")

app = Flask(__name__)


@app.route("/")
def status():
    return "Ready!"

{
    "text": "message"
}

{
    "result": "ham"
}

@app.route("/predict", methods=["POST"])
def predict():
    data_dict = request.get_json()

    text = [data_dict["text"]]

    return jsonify({
        "result": model.predict(text)[0]
    })

@app.route("/analysis")
def analysis():
    return  render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)