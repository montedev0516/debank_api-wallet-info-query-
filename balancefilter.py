import os
import requests
import asyncio
import aiohttp

# Load your API key from an environment variable or set it directly 
DEBANK_API_KEY = os.getenv("DEBANK_API_KEY") 
TOP_HOLDERS_URL = "https://pro-openapi.debank.com/v1/token/top_holders"

async def fetch_wallet_balance(session, wallet_id):
    """Fetch the balance for a specific wallet."""
    url = f"https://pro-openapi.debank.com/v1/user/chain_balance?id={wallet_id}&chain_id=eth"
    headers = {
        'accept': 'application/json',
        'AccessKey': "1d380a63b92d6d9da3b184051a2abc2cd2af94a5"
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()  # Raise an error for bad responses
        return await response.json()

async def get_wallets_in_range(limit=50):
    """Get top wallets and filter those within the specified balance range."""
    async with aiohttp.ClientSession() as session:
        # Fetch top holders
        response = await fetch_top_wallets(session, limit)
        
        # Extract wallet IDs
        wallet_ids = [holder['id'] for holder in response if 'id' in holder]

        # Fetch balances concurrently
        tasks = [fetch_wallet_balance(session, wallet_id) for wallet_id in wallet_ids]
        balances = await asyncio.gather(*tasks)

        # Filter wallets based on balance range
        filtered_wallets = []
        for balance_info in balances:
            usd_value = balance_info.get('usd_value', 0)
            if 1000 <= usd_value <= 10000:
                filtered_wallets.append(balance_info)

        return filtered_wallets

async def fetch_top_wallets(session, limit):
    """Fetch top wallets from DeBank API."""
    params = {'chain_id': 'eth', 'id': 'eth', 'start': 0, 'limit': limit}
    url = f"{TOP_HOLDERS_URL}?{requests.compat.urlencode(params)}"
    headers = {
        'accept': 'application/json',
        'AccessKey': "1d380a63b92d6d9da3b184051a2abc2cd2af94a5"
    }
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()  # Raise an error for bad responses
        return await response.json()

# Main execution
if __name__ == "__main__":
    try:
        result = asyncio.run(get_wallets_in_range())
        print("Filtered Wallets:")
        for wallet in result:
            print(wallet)
    except Exception as e:
        print("Error:", str(e))