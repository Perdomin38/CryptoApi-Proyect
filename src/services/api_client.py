import requests
import time
import logging
from typing import Optional
from src.models.data_models import LivePriceData, HistoricalData

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class CryptoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        Initializes the CryptoAPI client.
        """
        # We add max_retries to limit the number of connection attempts and prevent infinite hangs
        self.timeout = timeout
        self.max_retries = max_retries

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """
        Centralized request method with a built-in retry mechanism.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(endpoint, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    # Wait for 2 seconds before attempting the next retry
                    time.sleep(2) 
                else:
                    logging.error("Max retries reached. Request failed.")
                    return None
        return None

    def get_price(self, coin_id: str, display_currency: str = "usd") -> Optional[LivePriceData]:
        """
        Fetches the current live price of a specific cryptocurrency.
        """
        endpoint = f"{self.BASE_URL}/simple/price"
        vs_currencies = f"usd,{display_currency.lower()}" if display_currency.lower() != "usd" else "usd"
        params = {"ids": coin_id.lower(), "vs_currencies": vs_currencies}

        data = self._make_request(endpoint, params)
        
        if data and coin_id.lower() in data:
            # Return a strongly-typed LivePriceData object instead of a raw dictionary
            return LivePriceData(
                coin_id=coin_id.lower(),
                usd_price=data[coin_id.lower()]["usd"],
                display_currency=display_currency.lower(),
                display_price=data[coin_id.lower()][display_currency.lower()]
            )
        logging.warning(f"Coin '{coin_id}' not found.")
        return None

    def get_historical_data(self, coin_id: str, days: int = 30) -> Optional[HistoricalData]:
        """
        Fetches historical daily market data for a specific cryptocurrency.
        """
        endpoint = f"{self.BASE_URL}/coins/{coin_id.lower()}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}

        data = self._make_request(endpoint, params)
        
        if data and "prices" in data:
            # Return a strongly-typed HistoricalData object
            return HistoricalData(coin_id=coin_id.lower(), prices_usd=data["prices"])
        return None