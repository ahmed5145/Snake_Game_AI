function startTraining() {
    fetch('/start-training', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log success message if needed
            // Optionally update UI to indicate training started
        })
        .catch(error => console.error('Error starting training:', error));
}

function fetchPlot() {
    fetch('/plot')
        .then(response => response.json())
        .then(data => {
            const plotContainer = document.getElementById('plotContainer');
            plotContainer.innerHTML = `<img src="data:image/png;base64, ${data.plot}" alt="Plot"/>`;
        })
        .catch(error => console.error('Error fetching plot:', error));
}

// Initial fetch for plot when page loads
fetchPlot();

// Interval to fetch plot updates every 5 seconds
setInterval(fetchPlot, 5000);
