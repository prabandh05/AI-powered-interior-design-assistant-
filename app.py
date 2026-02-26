from flask import Flask, request, jsonify
import os
import json

from services.pipeline import InteriorDesignPipeline

app = Flask(__name__)

# Load dataset once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")

with open(DATASET_PATH) as f:
    dataset = json.load(f)

pipeline = InteriorDesignPipeline(dataset)


@app.route("/generate-design", methods=["POST"])
def generate_design():

    user_input = request.json

    if not user_input:
        return jsonify({"status": "error", "message": "No input provided"}), 400

    result = pipeline.run(user_input)

    return jsonify(result)


@app.route("/agent1", methods=["POST"])
def test_agent1():
    data = request.json
    result = pipeline.agent1.run(data)
    return jsonify(result)


@app.route("/agent2", methods=["POST"])
def test_agent2():
    data = request.json
    result = pipeline.agent2.run(data)
    return jsonify(result)


@app.route("/agent3", methods=["POST"])
def test_agent3():
    data = request.json
    agent1_output = data.get("agent1_output")
    agent2_output = data.get("agent2_output")
    result = pipeline.agent3.run(agent1_output, agent2_output)
    return jsonify(result)


@app.route("/agent4", methods=["POST"])
def test_agent4():
    data = request.json
    result = pipeline.agent4.generate_comparison_plans(
        theme=data["theme"],
        space_type=data["space_type"],
        required_items=data["required_items"],
        user_budget=data["budget"]
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)