import os
import requests
from dotenv import load_dotenv
import pandas as pd
import sqlite3
import csv

# Load environment variables from .env file
load_dotenv()
access_key = os.getenv("DEBANK_API_KEY")  # Store your API key in an environment variable

# Function to get top holders
def get_top_holders(protocol_id, start):
    
    url = "https://pro-openapi.debank.com/v1/protocol/top_holders"
    headers = {
        'accept': 'application/json',
        'AccessKey': access_key
    }
    params = {'id': protocol_id, 'start': start, 'limit': 10}  # Add limit to params
    top_holders = []

    # Send GET request
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Request URL: {response.url}")  # Print the full request URL for debugging

    # Check if response is successful
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

# Function to save top holders to CSV
def save_holders_to_csv(top_holders, filename='top_holders.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        try:  # Try to write the data to the CSV file
            writer = csv.writer(file)
            writer.writerow(['Holder', 'Amount'])
            for holder in top_holders:
                holder_name = holder[0]
                amount_value = holder[1]
                writer.writerow([holder_name, amount_value])
                
            print(f"Top holders data saved to {filename}")
        except Exception as e:      # Catch any exceptions
            print(f"Error saving top holders data to {filename}: {e}")
    return filename
        
def main():
    top_holders = get_top_holders(protocol_id='curve', start=10)  # Replace 'curve' with the desired protocol ID
    if top_holders:
        # Process the top holders if needed
        print(f"Retrieved {len(top_holders)} top holders.")
    
        # Save top holders to CSV
        filename = save_holders_to_csv(top_holders)
        print(f"Saved top holders data to {filename}.")

if __name__ == "__main__":
    main()