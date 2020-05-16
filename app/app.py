from flask import Flask, request, jsonify, render_template
# from joblib import load
from predict import predict

# model = load("clf.joblib")


app = Flask(__name__, template_folder='../templates/')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/response', methods=['GET', 'POST'])
def response():

    if request.method == "POST":
        snippet = request.form['fsnippet']
        # Testing with predict.py
        personality_type = predict(snippet)
    return render_template("index.html", name=personality_type)

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

@app.route("/methodology")
def methodology():
    return render_template("methodology.html")
 
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)