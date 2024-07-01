// app.js

function startTraining() {
    fetch('/start-training', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.message))
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

setInterval(fetchPlot, 5000); // Update plot every 5 seconds
