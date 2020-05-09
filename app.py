from flask import Flask, request, jsonify, render_template
from joblib import load
from predict import predict

model = load("clf.joblib")


app = Flask(__name__)

def home():
    # list of links to other routes
    string = "Hello world!"
    return render_template("index.html", string=string)

@app.route('/response', methods=['POST'])
def response():
    snippet = request.form.get("snippet")
    # Preprocessing happens here, then:
    personality_type = predict(snippet)
    return render_template("index.html", personality=personality_type)

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)