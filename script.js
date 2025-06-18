// --- Documentation ---
// This script handles the front-end logic. It listens for the form
// submission, sends the input data to the backend API, and displays
// the returned prediction.

// --- Configuration ---
// IMPORTANT: You will replace this with your deployed API URL later!
// const API_URL = 'http://127.0.0.1:5000/predict'; // For local testing
const API_URL = 'https://jasennelson.pythonanywhere.com/predict';

// --- Event Listener ---
document.getElementById('prediction-form').addEventListener('submit', function(event) {
    // Prevent the default form submission
    event.preventDefault();

    // --- Get User Input ---
    const feature1 = document.getElementById('feature1').value;
    const feature2 = document.getElementById('feature2').value;
    const feature3 = document.getElementById('feature3').value;

    // --- Prepare Data for API ---
    const data = {
        'feature1': parseFloat(feature1),
        'feature2': parseFloat(feature2),
        'feature3': parseFloat(feature3)
    };

    // Show loading state
    const predictionOutput = document.getElementById('prediction-output');
    predictionOutput.textContent = 'Loading...';

    // --- Send Data to API using Fetch ---
    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Convert JS object to JSON string
    })
    .then(response => response.json()) // Parse the JSON response from the server
    .then(result => {
        // --- Display Result ---
        if (result.error) {
            predictionOutput.textContent = `Error: ${result.error}`;
        } else {
            predictionOutput.textContent = result.prediction;
        }
    })
    .catch(error => {
        // --- Handle Errors ---
        console.error('Error:', error);
        predictionOutput.textContent = 'An error occurred. Check the console.';
    });
});