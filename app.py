from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Serve index.html at root
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Load prompt templates
with open("prompt_templates.json", "r") as file:
    prompt_data = json.load(file)

@app.route("/get_prompt", methods=["POST"])
def get_prompt():
    data = request.json
    goal = data.get("goal")
    inputs = data.get("inputs")

    if goal not in prompt_data:
        return jsonify({"error": "Goal not found"}), 400

    template = prompt_data[goal]["template"]
    try:
        prompt = template.format(**inputs)
    except KeyError as e:
        return jsonify({"error": f"Missing input for: {e}"}), 400

    return jsonify({"prompt": prompt})

if __name__ == "__main__":
    print("✅ Starting Flask server...")
    app.run(debug=True)
