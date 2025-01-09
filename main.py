import ssl
import asyncio
import websockets
import json

# Define the API requests
REQUESTS = {
    "Deribit Indices": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "public/get_index",
        "params": {"currency": "BTC"},
    },
    "Volatility Index (DVOL)": {
        "jsonrpc": "2.0",
        "id": 833,
        "method": "public/get_volatility_index_data",
        "params": {
            "currency": "BTC",
            "start_timestamp": 1704067200000,  # January 1, 2024
            "end_timestamp": 1735689600000,    # December 31, 2024
            "resolution": "86400"               # Daily data (1 day = 86400 seconds)
        }
    },
    "Historical Volatility": {
       "jsonrpc" : "2.0",
        "id" : 8387,
        "method" : "public/get_historical_volatility",
        "params" : {
            "currency" : "BTC"
        }
    },
    "Insurance Fund": {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "public/get_insurance_fund",
        "params": {"currency": "BTC"},
    },
    "Confirmation of Reserves": {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "public/get_currencies",
        "params": {},
    },
    "Financing Rate": {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "public/get_funding_rate_value",
        "params": {"instrument_name": "BTC-PERPETUAL"},
    },
    "Market Data": {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "public/ticker",
        "params": {"instrument_name": "BTC-PERPETUAL"},
    },
    "Options Data": {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "public/get_book_summary_by_currency",
        "params": {"currency": "BTC", "kind": "option"},
    },
    "Futures Metrics": {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "public/get_book_summary_by_currency",
        "params": {"currency": "BTC", "kind": "future"},
    },
    "Metric Options": {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "public/get_instruments",
        "params": {"currency": "BTC", "kind": "option"},
    },
}

# Function to fetch data
async def call_api(requests):
    ssl_context = ssl._create_unverified_context()
    results = {}

    async with websockets.connect("wss://test.deribit.com/ws/api/v2", ssl=ssl_context) as websocket:
        for key, request in requests.items():
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            results[key] = json.loads(response)
    return results

# Function to process and organize data
def process_data(results):
    processed_data = {}
    for key, result in results.items():
        if result.get("result"):
            processed_data[key] = result["result"]
        else:
            processed_data[key] = {"error": result.get("error", "Unknown error")}
    return processed_data

# Function to display data in a more understandable format
def display_data(processed_data):
    for metric, data in processed_data.items():
        print(f"--- {metric} ---")
        
        # If data is a dictionary (e.g., historical volatility), format it in a readable way
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        
        # If data is a list (e.g., index data or volatility data), display a few entries
        elif isinstance(data, list):
            if isinstance(data[0], dict):  # Check if the list contains dicts
                for index, entry in enumerate(data[:10]):  # Show first 5 entries if there are many
                    print(f"Entry {index + 1}:")
                    for sub_key, sub_value in entry.items():
                        print(f"  {sub_key}: {sub_value}")
            else:  # If the list contains simple values
                for index, value in enumerate(data[:5]):  # Show first 5 entries if there are many
                    print(f"Entry {index + 1}: {value}")
        
        # Handle unknown data formats
        else:
            print(f"Data: {data}")
        
        print("\n")

# Main function
async def main():
    results = await call_api(REQUESTS)
    processed_data = process_data(results)

    # Display the organized data
    display_data(processed_data)

# Run the script
asyncio.run(main())
