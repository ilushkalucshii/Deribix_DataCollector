import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the API endpoint for Deribit
url = 'https://www.deribit.com/api/v2/public/get_instruments'

# Request data from Deribit
response = requests.get(url)
data = response.json()

# Check if request was successful
if data['result']:
    instruments = data['result']
    df = pd.DataFrame(instruments)
    
    # Example: Process and plot historical volatility
    # Replace this with the actual data you need from the API
    volatility = df['implied_volatility']  # Example column
    
    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(df['instrument_name'], volatility)
    plt.title('Implied Volatility Over Time')
    plt.xlabel('Instrument')
    plt.ylabel('Implied Volatility')
    
    # Save the plot
    plt.savefig('volatility_plot.png')

    # Show the plot
    plt.show()

else:
    print("Failed to retrieve data.")
