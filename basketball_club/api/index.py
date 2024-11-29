from flask import Flask
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# This is the handler that Vercel will call
def handler(request):
    return app
