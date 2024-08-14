from flask import Flask, jsonify
import requests
from utils.utils import transform_to_uppercase
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

# Data Store
data_store = {}

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    """Method to fetch data from url

    Returns:
        json: Success or failure message
    """
    app.logger.info("Data Collector Started")
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

    # Convert strng to uppercase
    for entry in data:
        for key, value in entry.items():
            if isinstance(value, str):
                entry[key] = transform_to_uppercase(value)
    
    # Store data in the dictionary
    data_store['posts'] = data
    app.logger.info("Data fetched and processed successfully.")
    return jsonify({"message": "Data fetched and processed successfully."})

# Return the processed data
@app.route('/get-processed-data', methods=['GET'])
def get_processed_data():
    """Method to return colletced data

    Returns:
        json: Json of stored data
    """
    return jsonify(data_store)

if __name__ == '__main__':
    app.logger.info("Starting the Flask app.")
    app.run(debug=True)
