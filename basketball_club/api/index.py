from flask import Flask
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app

# This is the handler Vercel will call
def handler(request):
    """Handle incoming Vercel requests."""
    try:
        return flask_app
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": str(e)
        }
