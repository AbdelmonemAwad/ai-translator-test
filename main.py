#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Translator Main Entry Point
"""

# Initialize the Flask application
try:
    print("✓ Attempting to import original AI Translator...")
    from app import app
    print("✓ Successfully imported original AI Translator v2.2.1")
except ImportError as e:
    print(f"✗ Failed to import app.py: {e}")
    # Create a minimal fallback app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "AI Translator - Import Error. Please check app.py"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)