from flask import Flask, Request
import sys
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

try:
    from app import app
    print("Successfully imported Flask app")
except Exception as e:
    print(f"Error importing app: {str(e)}")
    raise e

# Add ProxyFix middleware
app.wsgi_app = ProxyFix(app.wsgi_app)

def handler(request: Request):
    """Handle incoming Vercel requests."""
    try:
        print("Handler called with request method:", request.method)
        return app
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": {
                "error": str(e),
                "path": sys.path,
                "cwd": os.getcwd(),
                "files": os.listdir(os.getcwd())
            }
        }
