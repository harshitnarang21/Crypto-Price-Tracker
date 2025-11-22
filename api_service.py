"""
Crypto API Service
Fetches live cryptocurrency prices from CoinGecko API
"""

import requests
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class CryptoAPIService:
    """Service for fetching cryptocurrency data from CoinGecko API"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Popular cryptocurrencies to track
    DEFAULT_CRYPTOS = [
        "bitcoin", "ethereum", "binancecoin", "ripple", "cardano",
        "solana", "polkadot", "dogecoin", "matic-network", "litecoin",
        "chainlink", "avalanche-2", "uniswap", "cosmos", "algorand"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Crypto-Tracker-Python-App'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a request to the API with error handling"""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            
            # Handle rate limiting
            if response.status_code == 429:
                print("⚠️  API rate limit reached. Please wait a moment and try again.")
                print("   CoinGecko free API allows 10-50 calls/minute.")
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("⚠️  API rate limit reached. Please wait a moment and try again.")
            else:
                print(f"❌ API Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
    
    def get_live_prices(self, crypto_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Get live prices for cryptocurrencies
        
        Args:
            crypto_ids: List of crypto IDs (e.g., ['bitcoin', 'ethereum'])
                       If None, uses default list
        
        Returns:
            List of dictionaries with crypto data
        """
        if crypto_ids is None:
            crypto_ids = self.DEFAULT_CRYPTOS
        
        # Convert list to comma-separated string
        ids = ",".join(crypto_ids)
        
        params = {
            'ids': ids,
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h'
        }
        
        data = self._make_request('coins/markets', params)
        
        if data is None:
            return []
        
        # Format the data
        formatted_data = []
        for coin in data:
            # Handle None values from API
            change_24h = coin.get('price_change_percentage_24h')
            if change_24h is None:
                change_24h = 0.0
            
            formatted_data.append({
                'id': coin.get('id', ''),
                'symbol': coin.get('symbol', '').upper(),
                'name': coin.get('name', ''),
                'price': coin.get('current_price', 0) or 0,
                'market_cap': coin.get('market_cap', 0) or 0,
                'volume_24h': coin.get('total_volume', 0) or 0,
                'change_24h': change_24h,
                'high_24h': coin.get('high_24h', 0) or 0,
                'low_24h': coin.get('low_24h', 0) or 0
            })
        
        return formatted_data
    
    def get_price_history(self, crypto_id: str, days: int = 30) -> List[Dict]:
        """
        Get historical price data for a cryptocurrency
        
        Args:
            crypto_id: Crypto ID (e.g., 'bitcoin')
            days: Number of days of history (1, 7, 14, 30, 90, 180, 365, max)
        
        Returns:
            List of dictionaries with timestamp and price
        """
        params = {
            'vs_currency': 'usd',
            'days': days
        }
        
        data = self._make_request(f'coins/{crypto_id}/market_chart', params)
        
        if data is None or 'prices' not in data:
            return []
        
        # Format historical data
        history = []
        for point in data['prices']:
            timestamp = datetime.fromtimestamp(point[0] / 1000)
            price = point[1]
            history.append({
                'timestamp': timestamp,
                'price': price
            })
        
        return history
    
    def get_crypto_info(self, crypto_id: str) -> Optional[Dict]:
        """
        Get detailed information about a cryptocurrency
        
        Args:
            crypto_id: Crypto ID (e.g., 'bitcoin')
        
        Returns:
            Dictionary with crypto information
        """
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false',
            'sparkline': 'false'
        }
        
        data = self._make_request(f'coins/{crypto_id}', params)
        return data
    
    def search_crypto(self, query: str) -> List[Dict]:
        """
        Search for cryptocurrencies by name or symbol
        
        Args:
            query: Search query
        
        Returns:
            List of matching cryptocurrencies
        """
        data = self._make_request('search', {'query': query})
        
        if data is None or 'coins' not in data:
            return []
        
        return data['coins'][:10]  # Return top 10 results
    
    def get_trending(self) -> List[Dict]:
        """
        Get trending cryptocurrencies
        
        Returns:
            List of trending cryptocurrencies
        """
        data = self._make_request('search/trending')
        
        if data is None or 'coins' not in data:
            return []
        
        trending = []
        for item in data['coins']:
            coin = item.get('item', {})
            trending.append({
                'id': coin.get('id', ''),
                'name': coin.get('name', ''),
                'symbol': coin.get('symbol', '').upper(),
                'market_cap_rank': coin.get('market_cap_rank', 0),
                'score': item.get('score', 0)
            })
        
        return trending


if __name__ == "__main__":
    # Test the API service
    print("🧪 Testing Crypto API Service...\n")
    
    api = CryptoAPIService()
    
    # Test live prices
    print("📊 Fetching live prices...")
    prices = api.get_live_prices(['bitcoin', 'ethereum'])
    for crypto in prices:
        print(f"{crypto['name']} ({crypto['symbol']}): ${crypto['price']:,.2f}")
    
    print("\n✅ API Service is working!")

