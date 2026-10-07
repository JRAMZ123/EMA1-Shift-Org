from flask import Flask, request, jsonify, render_template_string
from github_manager import save_html, read_html
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the HTML file"""
    html_content = read_html('index.html')
    return html_content, 200, {'Content-Type': 'text/html'}

@app.route('/api/save', methods=['POST'])
def save_changes():
    """Save org chart changes to GitHub"""
    data = request.json
    html_content = data.get('html')
    commit_message = data.get('message', 'Update org chart')
    
    if not html_content:
        return jsonify({'error': 'No HTML content provided'}), 400
    
    result = save_html('index.html', html_content, commit_message)
    
    if result:
        return jsonify({'success': True, 'message': 'Changes saved to GitHub'}), 200
    else:
        return jsonify({'error': 'Failed to save to GitHub'}), 500

@app.route('/api/load', methods=['GET'])
def load_changes():
    """Load the latest org chart from GitHub"""
    html_content = read_html('index.html')
    if html_content:
        return jsonify({'html': html_content}), 200
    else:
        return jsonify({'error': 'Failed to load from GitHub'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
