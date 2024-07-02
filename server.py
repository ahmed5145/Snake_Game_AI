from flask import Flask, render_template, jsonify, after_this_request
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
    # Check if training is already running
    if not agent.training_in_progress:
        threading.Thread(target=agent.train_continuously).start()
        return jsonify({'message': 'Training started'})
    else:
        return jsonify({'message': 'Training already in progress'})

@app.route('/plot')
def plot_image():
    @after_this_request
    def add_plot(response):
        try:
            # Get the latest score from the agent
            latest_score = agent.plot_scores[-1] if agent.plot_scores else 0
            # Update plot data in agent with the latest score
            agent.update_plot_data(latest_score)
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Content-Type'] = 'application/json'
            response.data = jsonify({'message': 'Plot updated'}).data
        except Exception as e:
            print(f"Error generating plot: {str(e)}")
            response.data = jsonify({'error': 'Failed to update plot'}).data
        return response

    return app.response_class(response='', status=200)

if __name__ == '__main__':
    app.run(debug=True)
