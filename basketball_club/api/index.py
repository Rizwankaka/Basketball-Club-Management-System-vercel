from flask import Flask
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def handler(request):
    """Handle the request and return the Flask application response."""
    with app.request_context(request):
        return app.handle_request()
