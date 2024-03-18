from flask import Flask, render_template
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

def replace_nan(obj):
    if isinstance(obj, list):
        return [replace_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_nan(value) for key, value in obj.items()}
    elif pd.isna(obj):
        return None
    else:
        return obj

@app.route('/')
def index():
    # Load the processed data
    data_file = "data/datasets/processed/house_listings_processed_2024-03-12.json"
    df = pd.read_json(data_file, orient="records")

    # Replace NaN with None in the DataFrame, which will become null in JSON
    df = df.where(pd.notnull(df), None)

    # Additionally, apply the replacement recursively to nested structures
    data = [replace_nan(row.to_dict()) for index, row in df.iterrows()]

    # Get Google Maps API key from environment variables
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    return render_template('index.html', data=data, google_maps_api_key=google_maps_api_key)

if __name__ == '__main__':
    app.run(debug=True)