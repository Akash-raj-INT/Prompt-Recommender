from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Load prompts
with open("prompt_templates.json") as f:
    prompt_data = json.load(f)

@app.route("/get_prompt", methods=["POST"])
def get_prompt():
    data = request.json
    goal = data.get("goal")
    inputs = data.get("inputs")

    if goal not in prompt_data:
        return jsonify({"error": "Goal not found"}), 400

    try:
        template = prompt_data[goal]["template"]
        prompt = template.format(**inputs)
    except KeyError as e:
        return jsonify({"error": f"Missing input for: {e}"}), 400

    return jsonify({"prompt": prompt})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
