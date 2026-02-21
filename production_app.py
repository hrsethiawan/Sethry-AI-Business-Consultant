# production_app.py
import torch
from flask import Flask, render_template, request, jsonify
from optimized_business_ai import OptimizedBusinessConsultingAI
import time
import logging
import signal
import sys
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure random key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variable to track if we're shutting down
shutdown_flag = False

# Handle graceful shutdown
def signal_handler(sig, frame):
    logger.info('Received shutdown signal...')
    global shutdown_flag
    shutdown_flag = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Initialize AI with GPU optimization
try:
    access_token = "hf_"
    consultant = OptimizedBusinessConsultingAI(access_token=access_token)
    logger.info("🚀 Production App Ready with GPU Optimization!")
except Exception as e:
    logger.error(f"❌ Failed to initialize: {str(e)}")
    raise

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/consult', methods=['GET'])
def consult():
    """API endpoint for business consulting questions"""
    if shutdown_flag:
        return jsonify({'error': 'Service is shutting down'}), 503
    
    question = request.args.get('question', '').strip()
    category = request.args.get('category', 'general').strip().lower()
    
    if not question:
        return jsonify({'error': 'Question parameter is required'}), 400
    
    # Validate category
    valid_categories = ['general', 'finance', 'marketing', 'operations', 'hr']
    if category not in valid_categories:
        category = 'general'
    
    try:
        start_time = time.time()
        
        # Generate response using the AI model
        response = consultant.generate_response(
            question=question,
            category=category
        )
        
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        
        logger.info(f"Consultation completed in {processing_time}s for: {question[:50]}...")
        
        return jsonify({
            'question': question,
            'answer': response,
            'category': category,
            'processing_time': processing_time,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = f"Error processing consultation: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

@app.route('/api/batch-consult', methods=['POST'])
def batch_consult():
    """API endpoint for batch business consulting questions"""
    if shutdown_flag:
        return jsonify({'error': 'Service is shutting down'}), 503
    
    try:
        data = request.get_json()
        questions = data.get('questions', [])
        category = data.get('category', 'general').strip().lower()
        
        if not questions:
            return jsonify({'error': 'Questions array is required'}), 400
        
        # Validate category
        valid_categories = ['general', 'finance', 'marketing', 'operations', 'hr']
        if category not in valid_categories:
            category = 'general'
        
        start_time = time.time()
        
        # Generate responses for all questions
        responses = consultant.batch_generate(questions, category)
        
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        
        results = []
        for i, (question, response) in enumerate(zip(questions, responses)):
            results.append({
                'question': question,
                'answer': response,
                'index': i
            })
        
        logger.info(f"Batch consultation completed for {len(questions)} questions")
        
        return jsonify({
            'results': results,
            'total_questions': len(questions),
            'category': category,
            'processing_time': processing_time,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = f"Error processing batch consultation: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'Failed to process batch request: {str(e)}'}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """API endpoint to get model information"""
    if shutdown_flag:
        return jsonify({'error': 'Service is shutting down'}), 503
    
    try:
        info = consultant.get_model_info()
        return jsonify(info)
    except Exception as e:
        error_msg = f"Error getting model info: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'Failed to get model info: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Simple check - just see if we can access the model
        info = consultant.get_model_info()
        return jsonify({
            'status': 'healthy',
            'model_info': info,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Run the Flask app
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
