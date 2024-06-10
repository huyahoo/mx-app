#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000 &

# Start frontend
cd ../frontend
# serve -s dist -l 80
yarn dev
