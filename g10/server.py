from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import assistant  

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "")
    response = assistant.process_command_from_web(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
