import asyncio
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp


class CoinGeckoClient:
    """
    Free CoinGecko API client - No API key required!
    Rate limit: 10-50 calls/minute (generous free tier)
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        session = await self._get_session()
        url = f"{self.BASE_URL}{endpoint}"

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    print("⚠️  Rate limit hit, waiting 60s...")
                    await asyncio.sleep(60)
                    return await self._request(endpoint, params)
                else:
                    print(f"❌ API Error: {response.status}")
                    return {}
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return {}

    async def get_price(self, coin_id: str, vs_currency: str = "usd") -> Optional[Dict]:
        """
        Get current price for a cryptocurrency

        Args:
            coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
            vs_currency: Currency to compare against (default: 'usd')

        Returns:
            {
                'bitcoin': {
                    'usd': 50000.0,
                    'usd_24h_change': 2.5,
                    'usd_market_cap': 950000000000,
                    'usd_24h_vol': 25000000000
                }
            }
        """
        params = {
            "ids": coin_id,
            "vs_currencies": vs_currency,
            "include_24hr_change": "true",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
        }
        return await self._request("/simple/price", params)

    async def get_market_data(self, coin_id: str) -> Optional[Dict]:
        """
        Get detailed market data for a coin

        Returns:
            {
                'id': 'bitcoin',
                'symbol': 'btc',
                'name': 'Bitcoin',
                'current_price': 50000.0,
                'market_cap': 950000000000,
                'total_volume': 25000000000,
                'high_24h': 51000.0,
                'low_24h': 49000.0,
                'price_change_24h': 1000.0,
                'price_change_percentage_24h': 2.5,
                ...
            }
        """
        data = await self._request(
            f"/coins/{coin_id}",
            {
                "localization": "false",
                "tickers": "false",
                "community_data": "false",
                "developer_data": "false",
            },
        )

        if data and "market_data" in data:
            market = data["market_data"]
            return {
                "id": data.get("id"),
                "symbol": data.get("symbol", "").upper(),
                "name": data.get("name"),
                "current_price": market.get("current_price", {}).get("usd"),
                "market_cap": market.get("market_cap", {}).get("usd"),
                "total_volume": market.get("total_volume", {}).get("usd"),
                "high_24h": market.get("high_24h", {}).get("usd"),
                "low_24h": market.get("low_24h", {}).get("usd"),
                "price_change_24h": market.get("price_change_24h"),
                "price_change_percentage_24h": market.get(
                    "price_change_percentage_24h"
                ),
                "circulating_supply": market.get("circulating_supply"),
                "total_supply": market.get("total_supply"),
                "ath": market.get("ath", {}).get("usd"),
                "ath_date": market.get("ath_date", {}).get("usd"),
                "atl": market.get("atl", {}).get("usd"),
                "atl_date": market.get("atl_date", {}).get("usd"),
            }
        return None

    async def get_historical_data(self, coin_id: str, days: int = 30) -> List[Dict]:
        """
        Get historical price data

        Args:
            coin_id: CoinGecko coin ID
            days: Number of days of history (1, 7, 14, 30, 90, 180, 365, max)

        Returns:
            List of {timestamp, price, volume} dicts
        """
        data = await self._request(
            f"/coins/{coin_id}/market_chart", {"vs_currency": "usd", "days": days}
        )

        if data and "prices" in data:
            prices = data["prices"]
            volumes = data.get("total_volumes", [])

            result = []
            for i, (timestamp, price) in enumerate(prices):
                volume = volumes[i][1] if i < len(volumes) else 0
                result.append(
                    {
                        "timestamp": datetime.fromtimestamp(
                            timestamp / 1000
                        ).isoformat(),
                        "price": price,
                        "volume": volume,
                    }
                )
            return result
        return []

    async def get_trending_coins(self) -> List[Dict]:
        """
        Get trending cryptocurrencies

        Returns:
            List of trending coins with basic info
        """
        data = await self._request("/search/trending")

        if data and "coins" in data:
            return [
                {
                    "id": coin["item"]["id"],
                    "symbol": coin["item"]["symbol"],
                    "name": coin["item"]["name"],
                    "market_cap_rank": coin["item"].get("market_cap_rank"),
                    "price_btc": coin["item"].get("price_btc"),
                }
                for coin in data["coins"][:10]  # Top 10
            ]
        return []

    async def search_coins(self, query: str) -> List[Dict]:
        """
        Search for coins by name or symbol

        Returns:
            List of matching coins
        """
        data = await self._request("/search", {"query": query})

        if data and "coins" in data:
            return [
                {
                    "id": coin["id"],
                    "symbol": coin["symbol"],
                    "name": coin["name"],
                    "market_cap_rank": coin.get("market_cap_rank"),
                }
                for coin in data["coins"][:10]
            ]
        return []


# Singleton instance
_coingecko_client = None


def get_coingecko_client() -> CoinGeckoClient:
    global _coingecko_client
    if _coingecko_client is None:
        _coingecko_client = CoinGeckoClient()
    return _coingecko_client
