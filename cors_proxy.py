from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)
logging.basicConfig(level=logging.DEBUG)

@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy():
    # Get the URL from query params (e.g., ?url=https://api.example.com)
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    logging.info(f"Proxying request to {url}")
    logging.debug(f"Request headers: {request.headers}")
    logging.debug(f"Request method: {request.method}")
    logging.debug(f"Request body: {request.json if request.is_json else request.data}")

    # Copy headers from incoming request, excluding 'Host'
    headers = {key: value for key, value in request.headers if key != 'Host'}

    # Determine the request method and forward accordingly
    if request.method == 'GET':
        resp = requests.get(url, headers=headers, params=request.args)  # Use params to forward query params
    elif request.method == 'POST':
        resp = requests.post(url, headers=headers, json=request.json, data=request.data)  # Forward JSON or form-data
    elif request.method == 'PUT':
        resp = requests.put(url, headers=headers, json=request.json, data=request.data)
    elif request.method == 'DELETE':
        resp = requests.delete(url, headers=headers)
    elif request.method == 'OPTIONS':
        # Handle preflight requests by returning appropriate CORS headers
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response
    else:
        return jsonify({'error': 'Unsupported HTTP method'}), 405

    # Forward response from target server to the client
    response = Response(resp.content, resp.status_code, resp.headers.items())
    
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
