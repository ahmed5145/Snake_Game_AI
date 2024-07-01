# helper.py

import matplotlib.pyplot as plt
import io
import base64

def plot(scores, mean_scores):
    plt.figure(figsize=(12, 6))
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.legend()
    plt.ylim(ymin=0)

    # Convert plot to base64-encoded image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()  # Close the figure to free up memory

    return plot_data
