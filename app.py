
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

def home():
    # list of links to other routes
    string = "Hello world!"
    return render_template("index.html", string=string)

@app.route('/response', methods=['POST'])
def response():
    snippet = request.form.get("fsnippet")
    # Preprocessing happens here, then:
    personality_type = (snippet * 2)
    return render_template("index.html", personality=personality_type)

    snippet = snippet.to_str()
    
    return render_template("index.html", personality=snippet)

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