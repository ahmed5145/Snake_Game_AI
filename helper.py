import matplotlib.pyplot as plt
import io
import base64
from matplotlib.ticker import MaxNLocator

def plot(scores, mean_scores):
    plt.figure(figsize=(12, 6))
    plt.title('Snake Game AI Training Progress', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Games', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.plot(scores, label='Score', color='blue', linestyle='-', marker='o', markersize=4)
    plt.plot(mean_scores, label='Mean Score', color='green', linestyle='-', marker='x', markersize=4)

    plt.legend(loc='upper left', fontsize=12)
    plt.ylim(ymin=0)
    plt.tight_layout()

    # Convert plot to base64-encoded image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()  # Close the figure to free up memory

    return plot_data, plt.gcf(), plt.gca()  # Return plot data, figure and axes objects
