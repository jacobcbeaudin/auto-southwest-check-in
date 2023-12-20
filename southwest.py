#!/usr/bin/env python3
"""Entrypoint into the script where the arguments are passed to lib.main"""

import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

from lib.main import main


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/checkin', methods=['POST'])
def checkin():
    # Example of using the existing main function
    # You would modify this according to your application's logic
    data = request.json
    arguments = sys.argv[1:]
    response = main(arguments)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
