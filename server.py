from flask import Flask, render_template, jsonify
from agent import Agent
from game import SnakeGameAI
import numpy as np

app = Flask(__name__)
agent = Agent()
game = SnakeGameAI()  # Initialize your game instance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game-state')
def game_state():
    state = agent.get_state(game)  # Pass the game instance here
    state_as_list = state.tolist()  # Convert NumPy array to Python list
    return jsonify(state_as_list)

if __name__ == '__main__':
    app.run(debug=True)
