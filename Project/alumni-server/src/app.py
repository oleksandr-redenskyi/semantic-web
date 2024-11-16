import os
import logging

from flask import Flask, jsonify, request

from sparql_utils import DBpediaData


logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format="%(asctime)s:%(levelname)s:%(module)s:%(message)s",
)
log = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/alumni', methods=['GET'])
def get_alumni():
    """Endpoint to get alumni of Taras Shevchenko Kyiv National University."""
    try:
        alumni = DBpediaData.get_alumni()
        return jsonify(alumni), 200
    except Exception as e:
        log.exception(f'An error occured when getting alumni')
        return jsonify({"error": str(e)}), 500


@app.route('/page/<person_uri>', methods=['GET'])
def get_person(person_uri: str):
    """Endpoint to get data about a specific person by their URI."""
    try:
        person_data = DBpediaData.get_person_data(person_uri)
        return jsonify(person_data), 200
    except Exception as e:
        log.exception(f'An error occured when getting person info')
        return jsonify({"error": str(e)}), 500


# Add CORS headers through a decorator
@app.after_request
def after_request(response):
    # Allow all origins (for testing)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('API_PORT', 5000)))
