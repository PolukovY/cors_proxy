from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)

CORS(app, resources={r"/proxy": {"origins": "*", "allow_headers": ["*"]}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    logging.info(f"Proxying request to {url}")
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request method: {request.method}")
    logging.info(f"Request body: {request.json if request.is_json else request.data}")

    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    try:
        if request.method == 'GET':
            resp = requests.get(url, headers=headers, params=request.args)
        elif request.method == 'POST':
            resp = requests.post(url, headers=headers, json=request.json)
        elif request.method == 'PUT':
            resp = requests.put(url, headers=headers, json=request.json)
        elif request.method == 'DELETE':
            resp = requests.delete(url, headers=headers)
        elif request.method == 'OPTIONS':
            response = jsonify({'status': 'OK'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, x-api-key, Accept, Content-Type'
            return response
        else:
            return jsonify({'error': 'Unsupported HTTP method'}), 405

        response = Response(resp.content, resp.status_code, resp.headers.items())
        if 'Access-Control-Allow-Origin' in response.headers:
            del response.headers['Access-Control-Allow-Origin']

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, x-api-key, Accept, Content-Type'

        return response

    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        return jsonify({'error': 'Proxy request failed', 'details': str(e)}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
