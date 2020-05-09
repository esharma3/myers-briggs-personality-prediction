from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    # list of links to other routes
    string = "Hello world!"
    return render_template("index.html", string=string)

@app.route('/response', methods=['POST'])
def response():
    snippet = request.form.get("fsnippet")
    # Preprocessing happens here, then:
    snippet = snippet.to_str()
    
    return render_template("index.html", personality=snippet)

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")
 
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)