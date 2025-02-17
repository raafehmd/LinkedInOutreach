# auth.py
from flask import request, jsonify
import os

def require_api_key(f):
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated
