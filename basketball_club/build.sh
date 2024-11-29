#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p .vercel/output/functions/api
mkdir -p .vercel/output/static

# Copy the API files
cp -r api/* .vercel/output/functions/api/
cp app.py .vercel/output/functions/api/
cp requirements.txt .vercel/output/functions/api/

# Copy static files
cp -r static/* .vercel/output/static/ 2>/dev/null || :

# Create config file
cat > .vercel/output/config.json << EOF
{
    "version": 3,
    "routes": [
        {
            "src": "/(.*)",
            "dest": "/api/index.py"
        }
    ]
}
EOF
