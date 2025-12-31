from flask import Flask, render_template, jsonify, request

print("🔥 app.py started")

app = Flask(__name__)

state = {
    "monkey": {"x": 50, "y": 250, "on_box": False},
    "box": {"x": 200, "y": 260},
    "banana": {"x": 200, "y": 100},
    "has_banana": False
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def get_state():
    return jsonify(state)

@app.route("/action", methods=["POST"])
def action():
    move = request.json["move"]

    if move == "right":
        state["monkey"]["x"] += 20
    elif move == "left":
        state["monkey"]["x"] -= 20
    elif move == "push":
        if abs(state["monkey"]["x"] - state["box"]["x"]) < 30:
            state["box"]["x"] += 20
            state["monkey"]["x"] += 20
    elif move == "climb":
        if abs(state["monkey"]["x"] - state["box"]["x"]) < 30:
            state["monkey"]["on_box"] = True
            state["monkey"]["y"] = 220
    elif move == "grab":
        if state["monkey"]["on_box"] and abs(state["box"]["x"] - state["banana"]["x"]) < 30:
            state["has_banana"] = True

    return jsonify(state)

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
