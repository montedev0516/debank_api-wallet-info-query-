import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
access_key = os.getenv("DEBANK_API_KEY")  # Store your API key in an environment variable

def get_top_holders(protocol_id, start):
    url = "https://pro-openapi.debank.com/v1/protocol/top_holders"
    headers = {
        'accept': 'application/json',
        'AccessKey': access_key
    }
    params = {'id': protocol_id, 'start': start, 'limit': 10}  # Add limit to params
    top_holders = []

    response = requests.get(url, headers=headers, params=params)
    
    print(f"Request URL: {response.url}")  # Print the full request URL for debugging

    if response.status_code == 200:
        data = response.json()
        # Directly check if data is a list
        if isinstance(data, list) and data:  # Check if data is a non-empty list
            top_holders = data
            print("Top Holders:", top_holders)
            return top_holders
        else:
            print("No data found or data is not in expected format.")
    else:
        print("Error:", response.status_code, response.text)  # Print error message
    return top_holders

def main():
    top_holders = get_top_holders(protocol_id='curve', start=10)  # Replace 'curve' with the desired protocol ID
    if top_holders:
        # Process the top holders if needed
        print(f"Retrieved {len(top_holders)} top holders.")

if __name__ == "__main__":
    main()