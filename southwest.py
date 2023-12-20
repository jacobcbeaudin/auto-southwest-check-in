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
    data = request.json
    if "confirmationNumber" in data and "firstName" in data and "lasstName" in data:
        arguments = [data.get("confirmationNumber"), data.get("firstName"), data.get("lastName")]
    elif "username" in data and "password" in data:
        arguments = [data.get("username"), data.get("password"),]
    else:
        raise Exception(
            'Must specify "confirmationNumber", "firstName", and "firstName" OR "username" and "password"'
        )
    response = main(arguments)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
