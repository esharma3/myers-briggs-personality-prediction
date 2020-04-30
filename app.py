from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # list of links to other routes
    return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("index.html")

@app.route("/analysis")
def analysis():
    return  render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)