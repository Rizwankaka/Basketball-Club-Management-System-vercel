#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py
