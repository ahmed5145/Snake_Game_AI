# server.py

from flask import Flask, render_template, jsonify
from agent import Agent
import threading
from flask_compress import Compress

app = Flask(__name__)
compress = Compress(app)
agent = Agent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-training', methods=['POST'])
def start_training():
    threading.Thread(target=agent.start_training).start()
    return jsonify({'message': 'Training started'})

@app.route('/plot')
def plot_image():
    plot_data = agent.get_plot()
    return jsonify({'plot': plot_data})

if __name__ == '__main__':
    app.run(debug=True)
