import time
import requests
from prometheus_client import start_http_server, Gauge

# Create a Prometheus metric (Gauge) with a label for the coin name
CRYPTO_PRICE = Gauge('crypto_price_usd', 'Current price of crypto in USD', ['symbol'])

def fetch_prices():
    # Public API - No key required for simple requests
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        # Update the Prometheus metrics
        CRYPTO_PRICE.labels(symbol='BTC').set(response['bitcoin']['usd'])
        CRYPTO_PRICE.labels(symbol='ETH').set(response['ethereum']['usd'])
        CRYPTO_PRICE.labels(symbol='DOGE').set(response['dogecoin']['usd'])
        print(f"Metrics updated: BTC is {response['bitcoin']['usd']}")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    # Start the exporter server on port 8000
    start_http_server(8000)
    print("Market Exporter is running on port 8000...")
    while True:
        fetch_prices()
        time.sleep(30) # Scrape the API every 30 seconds