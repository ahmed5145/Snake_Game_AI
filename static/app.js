const gameCanvas = document.getElementById('gameCanvas');
const plotCanvas = document.getElementById('plotCanvas');
const ctxGame = gameCanvas.getContext('2d');
const ctxPlot = plotCanvas.getContext('2d');

let gameId = null;
let plotId = null;

function startTraining() {
    fetch('/start-training')
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error starting training:', error));
}

function updateGame(state) {
    // Update game canvas based on state (e.g., draw snake, food, score)
}

function updatePlot(scores, meanScores) {
    // Update plot canvas based on scores and mean scores
}

function fetchGameState() {
    fetch('/game-state')
        .then(response => response.json())
        .then(state => updateGame(state))
        .catch(error => console.error('Error fetching game state:', error));
}

function fetchPlotData() {
    // Implement fetching plot data (optional based on your implementation)
}

function gameLoop() {
    gameId = requestAnimationFrame(gameLoop);
    fetchGameState();
    // Fetch plot data if needed
}

function plotLoop() {
    plotId = requestAnimationFrame(plotLoop);
    fetchPlotData();
}

// Start game loop
gameLoop();

// Start plot loop if needed
// plotLoop();
