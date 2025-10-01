# flask server

from flask import Flask, send_from_directory
from flask import request, jsonify, render_template
import os

global scores
scores = []

app = Flask(
    __name__,
    static_folder='src', 
    template_folder='templates'
)

def update_scores(name, score, planet):
    global scores
    # Update the scores list
    scores.append({"name": name, "score": score, "planet": planet})
    # Overwrite same name if better
    for entry in scores:
        if entry["name"] == name and entry["planet"] == planet:
            entry["score"] = max(entry["score"], score)
            break
    # Keep only the top 10 scores
    # scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]




@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'main.html')
@app.route('/src/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)
@app.route('/scores')
def serve_scoreboard():
    # sort scores
    global scores
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return render_template('scores.html', scores=scores)

@app.route('/api/send_score', methods=['POST'])
def receive_score():
    data = request.json
    score = data.get('score')
    name = data.get('name')
    planet = data.get('planet')
    # Here you can process the score (e.g., save to a database or file)
    print(f"Received score: {score} from player: {name} on planet: {planet}")
    update_scores(name, score, planet)

    return jsonify({"status": "success", "message": "Score received"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5511)