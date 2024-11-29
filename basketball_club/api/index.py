from flask import Flask
import sys
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Add ProxyFix middleware
app.wsgi_app = ProxyFix(app.wsgi_app)

# Handler for Vercel
def handler(request):
    """Wrapper for the Flask app to work with Vercel serverless."""
    with app.request_context(request.environ):
        try:
            return app(request.environ, lambda x, y: y)
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error in handler: {e}")
            # Return an error response
            return {"error": str(e)}, 500
