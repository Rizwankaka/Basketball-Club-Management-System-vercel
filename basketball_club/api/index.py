from flask import Flask, Request
import sys
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Add ProxyFix middleware
app.wsgi_app = ProxyFix(app.wsgi_app)

def handler(request):
    """Handle the serverless request."""
    return app
