import requests
import json
import os
from datetime import datetime
import time

def fetch_house_listings(location, status=None, singlefamily=None, RAPID_API_KEY=None, RAPID_API_HOST=None):
    url = "https://zillow56.p.rapidapi.com/search"

    querystring = {
        "location": location,
        "status": status,
        "isSingleFamily": singlefamily,
        "isLotLand": "false",
    }

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    try:
        all_results = []
        page = 1
        total_pages = 1

        while page <= total_pages:
            querystring["page"] = page

            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            data = response.json()
            all_results.extend(data["results"])
            total_pages = data["totalPages"]

            page += 1
            time.sleep(0.7)

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create the directory if it doesn't exist
        directory = "data/datasets/raw"
        os.makedirs(directory, exist_ok=True)

        # Generate the filename with the current date
        filename = f"house_listings_{current_date}.json"
        filepath = os.path.join(directory, filename)

        # Save the JSON response to the file
        with open(filepath, 'w') as file:
            json.dump(all_results, file)

        return all_results
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch house listings. Error: {str(e)}\n"
                        f"Status Code: {response.status_code}\n"
                        f"Response Content: {response.text}")