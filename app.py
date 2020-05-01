from flask import Flask, request, jsonify, render_template
from joblib import load

app = Flask(__name__)

# @app.route("/")
# def home():
#     # list of links to other routes
#     return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("index.html")

@app.route("/analysis")
def analysis():
    return  render_template("index.html")

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
        "result": clf.predict(text)[0]
    })

if __name__ == "__main__":
    app.run(debug=True)