from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow CORS from any domain

@app.route('/proxy', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy():
    # Get the target URL from the request arguments
    target_url = request.args.get('url')
    
    if not target_url:
        return jsonify({"error": "Target URL is required as 'url' query param"}), 400

    # Extract method (GET, POST, etc.), headers, and body
    method = request.method
    headers = {key: value for key, value in request.headers if key != 'Host'}
    body = request.get_data()  # Raw request body (for POST/PUT/PATCH)

    try:
        # Forward the request to the target URL
        response = requests.request(
            method=method,
            url=target_url,
            headers=headers,
            data=body,
            params=request.args  # Query params
        )

        # Relay the response back to the client
        return (response.content, response.status_code, response.headers.items())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
