import requests
import csv

# Define your API key
API_KEY = "..."

# Function to get all protocols on Ethereum mainnet
def get_protocols():
    url = "https://pro-openapi.debank.com/v1/protocol/list?chain_id=eth"
    headers = {
        "accept": "application/json",
        "AccessKey": API_KEY
    }
    response = requests.get(url, headers=headers)
    
    # Print the entire response for inspection
    print("Response:", response.json())  # Inspecting the raw response
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):  # Check if data is a list
            return data  # Return the list directly
        else:
            return data.get("data", [])  # Fallback for dictionary format
    else:
        print("Error fetching protocols:", response.status_code)
        return []

# Function to save protocols data to a CSV file
def save_protocols_to_csv(protocols, filename='protocols_eth.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['ID', 'Name', 'Chain', 'Site URL', 'Logo URL', 'Has Supported Portfolio'])
        
        # Write protocol data
        for protocol in protocols:
            writer.writerow([
                protocol.get('id'),
                protocol.get('name'),
                protocol.get('chain'),
                protocol.get('site_url'),
                protocol.get('logo_url'),
                protocol.get('has_supported_portfolio')
            ])
    
    print(f"Protocols data saved to {filename}")

# Main execution
if __name__ == "__main__":
    protocols = get_protocols()
    if protocols:
        save_protocols_to_csv(protocols)
