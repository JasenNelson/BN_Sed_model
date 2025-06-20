"""
Bayesian Network Sediment Model API

This Flask application serves a pre-trained Bayesian Network model for sediment prediction.
It provides a RESTful API endpoint for making predictions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

# Initialize Flask application
app = Flask(__name__)

# Enable CORS to allow requests from any origin
CORS(app)

# Global variable to store the loaded model
model = None

def load_model():
    """Load the pre-trained Bayesian Network model."""
    global model
    try:
        import dill
        print("Loading model...")
        with open('/home/jasennelson/mysite/bn_sed_model.pkl', 'rb') as f:
            model_data = dill.load(f)
            model = model_data['model']
            # Rebuild the model with CPDs
            for cpd in model_data['cpds']:
                model.add_cpds(cpd)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Error: Model file 'bn_sed_model.pkl' not found.")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        import traceback
        traceback.print_exc()

@app.route('/')
def status():
    """Provide a simple status check."""
    # This lets you know the API is running without trying to serve a page.
    return jsonify({
        'status': 'API is running',
        'model_loaded': model is not None
    })
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    
    Expected JSON payload format:
    {
        "contaminant": "Low/Medium/High",
        "toc": float,
        "grain_size": "Clay/Silt/Sand/Gravel"
    }
    
    Returns:
        JSON response with prediction and probability
    """
    if model is None:
        return jsonify({'error': 'Model is not loaded.'}), 500
    
    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        
        # Prepare evidence for prediction
        evidence = {
            'Contaminant_Level': data.get('contaminant', 'Low'),
            'TOC_Content': data.get('toc', 1.0),
            'Grain_Size': data.get('grain_size', 'Silt')
        }
        
        # Make prediction using the model
        from pgmpy.inference import VariableElimination
        infer = VariableElimination(model)
        
        # Get the probability distribution for Ecological_Effect
        result = infer.query(variables=['Ecological_Effect'], evidence=evidence)
        
        # Get the most likely state and its probability
        prediction = max(result.values, key=lambda x: result.get_value(Ecological_Effect=x))
        probability = result.get_value(Ecological_Effect=prediction)
        
        # Return prediction
        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'probability': float(probability)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

# Load the model when the application starts
load_model()

if __name__ == '__main__':
    # Run the Flask application
    # In production, use a production WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
