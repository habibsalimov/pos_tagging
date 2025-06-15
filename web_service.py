#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Turkish POS Tagger Web Service
RESTful API with modern web interface for Turkish POS tagging
"""

import os
import json
import time
import logging
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import traceback

from modern_pos_tagger import ModernTurkishPOSTagger

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global tagger instances (lazy loading)
taggers = {}

def get_tagger(model_type: str = "legacy") -> ModernTurkishPOSTagger:
    """Get or create tagger instance"""
    if model_type not in taggers:
        try:
            logger.info(f"Loading {model_type} tagger...")
            taggers[model_type] = ModernTurkishPOSTagger(model_type=model_type)
            logger.info(f"{model_type} tagger loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load {model_type} tagger: {e}")
            # Fallback to legacy
            if model_type != "legacy":
                logger.info("Falling back to legacy tagger...")
                taggers[model_type] = ModernTurkishPOSTagger(model_type="legacy")
            else:
                raise e
    
    return taggers[model_type]

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Turkish POS Tagger</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        textarea, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
            font-family: inherit;
        }
        
        textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
            margin-right: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .results h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .token {
            display: inline-block;
            margin: 5px;
            padding: 8px 12px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 3px solid #667eea;
        }
        
        .token-word {
            font-weight: 600;
            color: #333;
        }
        
        .token-tag {
            font-size: 0.9em;
            color: #666;
            margin-left: 5px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .examples {
            margin-top: 30px;
        }
        
        .example {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 3px solid #ee5a24;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        
        .example:hover {
            background: #f8f9fa;
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
            }
            
            .content {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔤 Modern Turkish POS Tagger</h1>
            <p>Advanced Part-of-Speech tagging for Turkish language with BERT and traditional models</p>
        </div>
        
        <div class="content">
            <form id="tagForm">
                <div class="form-group">
                    <label for="sentence">Turkish Sentence:</label>
                    <textarea id="sentence" placeholder="Enter your Turkish sentence here... (e.g., 'Bunu başından beri biliyordum zaten .')"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="model">Model Type:</label>
                    <select id="model">
                        <option value="legacy">Legacy Brill Tagger</option>
                        <option value="berturk" selected>BERTurk (Modern)</option>
                        <option value="distilbert">DistilBERT Multilingual</option>
                    </select>
                </div>
                
                <button type="submit" class="btn" id="tagBtn">🏷️ Tag Sentence</button>
                <button type="button" class="btn" onclick="clearResults()">🗑️ Clear</button>
            </form>
            
            <div id="loading" class="loading" style="display: none;">
                <div class="spinner"></div>
                <p>Processing your sentence...</p>
            </div>
            
            <div id="results" class="results" style="display: none;">
                <h3>Tagging Results:</h3>
                <div id="tokens"></div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value" id="tokenCount">0</div>
                        <div class="stat-label">Tokens</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="processingTime">0ms</div>
                        <div class="stat-label">Processing Time</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="modelUsed">-</div>
                        <div class="stat-label">Model Used</div>
                    </div>
                </div>
            </div>
            
            <div class="examples">
                <h3>Try these examples:</h3>
                <div class="example" onclick="setExample('Bunu başından beri biliyordum zaten .')">
                    "Bunu başından beri biliyordum zaten ."
                </div>
                <div class="example" onclick="setExample('Ali koştu ve parkta oynadı .')">
                    "Ali koştu ve parkta oynadı ."
                </div>
                <div class="example" onclick="setExample('Türkiye güzel bir ülkedir .')">
                    "Türkiye güzel bir ülkedir ."
                </div>
                <div class="example" onclick="setExample('Bu kitabı okumak çok zevkli .')">
                    "Bu kitabı okumak çok zevkli ."
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Modern Turkish POS Tagger | Built with Flask, BERT, and ❤️</p>
        </div>
    </div>

    <script>
        async function tagSentence(sentence, model) {
            const response = await fetch('/api/tag', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sentence: sentence,
                    model_type: model
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        }
        
        function displayResults(data) {
            const tokensDiv = document.getElementById('tokens');
            const resultsDiv = document.getElementById('results');
            
            tokensDiv.innerHTML = '';
            
            data.result.forEach(([word, tag]) => {
                const tokenDiv = document.createElement('div');
                tokenDiv.className = 'token';
                tokenDiv.innerHTML = `
                    <span class="token-word">${word}</span>
                    <span class="token-tag">${tag}</span>
                `;
                tokensDiv.appendChild(tokenDiv);
            });
            
            document.getElementById('tokenCount').textContent = data.result.length;
            document.getElementById('processingTime').textContent = `${Math.round(data.processing_time * 1000)}ms`;
            document.getElementById('modelUsed').textContent = data.model_info.model_type;
            
            resultsDiv.style.display = 'block';
        }
        
        function setExample(sentence) {
            document.getElementById('sentence').value = sentence;
        }
        
        function clearResults() {
            document.getElementById('sentence').value = '';
            document.getElementById('results').style.display = 'none';
        }
        
        document.getElementById('tagForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const sentence = document.getElementById('sentence').value.trim();
            const model = document.getElementById('model').value;
            
            if (!sentence) {
                alert('Please enter a sentence to tag.');
                return;
            }
            
            const loadingDiv = document.getElementById('loading');
            const tagBtn = document.getElementById('tagBtn');
            const resultsDiv = document.getElementById('results');
            
            loadingDiv.style.display = 'block';
            resultsDiv.style.display = 'none';
            tagBtn.disabled = true;
            
            try {
                const data = await tagSentence(sentence, model);
                displayResults(data);
            } catch (error) {
                alert(`Error: ${error.message}`);
                console.error('Tagging error:', error);
            } finally {
                loadingDiv.style.display = 'none';
                tagBtn.disabled = false;
            }
        });
        
        // Set default example
        window.addEventListener('load', () => {
            setExample('Bunu başından beri biliyordum zaten .');
        });
    </script>
</body>
</html>
"""

# API Routes
@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Turkish POS Tagger',
        'version': '2.0.0',
        'timestamp': time.time()
    })

@app.route('/api/models')
def get_models():
    """Get available models"""
    return jsonify({
        'models': [
            {
                'id': 'legacy',
                'name': 'Legacy Brill Tagger',
                'description': 'Traditional rule-based tagger',
                'language': 'Turkish'
            },
            {
                'id': 'berturk',
                'name': 'BERTurk',
                'description': 'BERT-based Turkish model',
                'language': 'Turkish'
            },
            {
                'id': 'distilbert',
                'name': 'DistilBERT Multilingual',
                'description': 'Lightweight multilingual model',
                'language': 'Multilingual'
            }
        ]
    })

@app.route('/api/tag', methods=['POST'])
def tag_sentence():
    """Tag a sentence with POS tags"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        sentence = data.get('sentence', '').strip()
        model_type = data.get('model_type', 'legacy')
        
        if not sentence:
            return jsonify({'error': 'No sentence provided'}), 400
        
        # Get tagger
        tagger = get_tagger(model_type)
        
        # Tag the sentence
        start_time = time.time()
        result = tagger.tag(sentence)
        processing_time = time.time() - start_time
        
        # Return results
        return jsonify({
            'sentence': sentence,
            'result': result,
            'processing_time': processing_time,
            'model_info': tagger.get_model_info(),
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Tagging error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing the sentence'
        }), 500

@app.route('/api/batch', methods=['POST'])
def tag_batch():
    """Tag multiple sentences"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        sentences = data.get('sentences', [])
        model_type = data.get('model_type', 'legacy')
        
        if not sentences:
            return jsonify({'error': 'No sentences provided'}), 400
        
        if len(sentences) > 100:
            return jsonify({'error': 'Maximum 100 sentences allowed'}), 400
        
        # Get tagger
        tagger = get_tagger(model_type)
        
        # Tag all sentences
        start_time = time.time()
        results = []
        
        for sentence in sentences:
            if isinstance(sentence, str) and sentence.strip():
                result = tagger.tag(sentence.strip())
                results.append({
                    'sentence': sentence.strip(),
                    'result': result
                })
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'results': results,
            'total_sentences': len(results),
            'processing_time': processing_time,
            'model_info': tagger.get_model_info(),
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"Batch tagging error: {e}")
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing the sentences'
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get service statistics"""
    try:
        stats = {
            'loaded_models': list(taggers.keys()),
            'available_models': ['legacy', 'berturk', 'distilbert'],
            'service_uptime': time.time(),
            'version': '2.0.0'
        }
        
        # Add model-specific stats
        for model_name, tagger in taggers.items():
            stats[f'{model_name}_info'] = tagger.get_model_info()
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    print("🚀 Starting Modern Turkish POS Tagger Web Service")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("📚 Available endpoints:")
    print("   GET  /               - Web interface")
    print("   GET  /health         - Health check")
    print("   GET  /api/models     - Available models")
    print("   POST /api/tag        - Tag single sentence")
    print("   POST /api/batch      - Tag multiple sentences")
    print("   GET  /api/stats      - Service statistics")
    
    # Run the Flask app
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )