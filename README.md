## Proxy API with CORS Support
This project implements a simple proxy API using Flask that can handle HTTP requests (GET, POST, PUT, DELETE, etc.) and forward them to another server. It also supports Cross-Origin Resource Sharing (CORS), allowing requests from any domain.

## Features
- Proxy HTTP Methods: Supports GET, POST, PUT, DELETE, etc.
- CORS Handling: Allows requests from any domain, making it flexible for front-end applications.
- Header and Payload Forwarding: The API forwards all headers and body payloads from the client to the target server.
- Error Handling: Provides basic error handling for failed proxy requests.

# Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repository.git
cd your-repository

Create and activate a virtual environment (optional):

git clone https://github.com/your-username/your-repository.git
cd your-repository

Install the dependencies:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


python proxy_api.py
The server will start on http://localhost:5000.

## Usage
To use the proxy API, send a request to the /proxy endpoint and provide the target URL as a query parameter (url). The request method, headers, and body will be forwarded to the target server.

Example Requests
### GET Request:

curl -X GET "http://localhost:5000/proxy?url=https://jsonplaceholder.typicode.com/posts/1"
POST Request (with headers and JSON body):

curl -X POST "http://localhost:5000/proxy?url=https://jsonplaceholder.typicode.com/posts" \
  -H "Content-Type: application/json" \
  -d '{"title": "foo", "body": "bar", "userId": 1}'

### DELETE Request:

curl -X DELETE "http://localhost:5000/proxy?url=https://jsonplaceholder.typicode.com/posts/1"
.
├── proxy_api.py         # Main file containing the proxy API implementation
└── README.md            # Project documentation
Configuration
You can configure the following aspects of the project:

# Target URL: Pass the target URL as a query parameter url to the /proxy endpoint.
CORS: By default, CORS is enabled for all domains. You can restrict it by modifying the CORS(app) configuration in proxy_api.py.

## Dependencies
- Flask: A lightweight web framework for Python.
- Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing.
- Requests: A Python library for making HTTP requests.

## Requirements
- Python 3.x
- Flask
- Flask-CORS
- Requests

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
