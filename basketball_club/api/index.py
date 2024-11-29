import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def handler(request):
    """Handle incoming Vercel requests."""
    if request.method == "POST":
        return app(request.environ, start_response)
    elif request.method == "GET":
        return app(request.environ, start_response)
    return app

def start_response(status, headers):
    """WSGI start_response function."""
    return None
