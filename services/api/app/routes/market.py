from fastapi import APIRouter, HTTPException, Query

from app.integrations.coingecko import get_coingecko_client

router = APIRouter()

# Popular crypto mappings (symbol -> CoinGecko ID)
SYMBOL_TO_ID = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "SOL": "solana",
    "ADA": "cardano",
    "XRP": "ripple",
    "DOT": "polkadot",
    "DOGE": "dogecoin",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "LTC": "litecoin",
    "BCH": "bitcoin-cash",
}


def get_coin_id(symbol: str) -> str:
    """Convert symbol to CoinGecko ID"""
    symbol_upper = symbol.upper().replace("-USD", "").replace("USD", "")
    return SYMBOL_TO_ID.get(symbol_upper, symbol.lower())


@router.get("/price/{symbol}")
async def get_current_price(symbol: str):
    """
    Get current price for a cryptocurrency

    Example: /market/price/BTC or /market/price/bitcoin
    """
    client = get_coingecko_client()
    coin_id = get_coin_id(symbol)

    try:
        data = await client.get_price(coin_id)

        if not data or coin_id not in data:
            raise HTTPException(status_code=404, detail=f"Coin '{symbol}' not found")

        coin_data = data[coin_id]
        return {
            "symbol": symbol.upper(),
            "coin_id": coin_id,
            "price": coin_data.get("usd"),
            "change_24h": coin_data.get("usd_24h_change"),
            "market_cap": coin_data.get("usd_market_cap"),
            "volume_24h": coin_data.get("usd_24h_vol"),
            "timestamp": "now",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch price: {str(e)}")


@router.get("/details/{symbol}")
async def get_market_details(symbol: str):
    """
    Get detailed market data for a cryptocurrency

    Example: /market/details/BTC
    """
    client = get_coingecko_client()
    coin_id = get_coin_id(symbol)

    try:
        data = await client.get_market_data(coin_id)

        if not data:
            raise HTTPException(status_code=404, detail=f"Coin '{symbol}' not found")

        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch details: {str(e)}"
        )


@router.get("/history/{symbol}")
async def get_price_history(
    symbol: str,
    days: int = Query(
        default=30, ge=1, le=365, description="Number of days of history"
    ),
):
    """
    Get historical price data

    Example: /market/history/BTC?days=7
    """
    client = get_coingecko_client()
    coin_id = get_coin_id(symbol)

    try:
        data = await client.get_historical_data(coin_id, days)

        if not data:
            raise HTTPException(
                status_code=404, detail=f"No history found for '{symbol}'"
            )

        return {
            "symbol": symbol.upper(),
            "coin_id": coin_id,
            "days": days,
            "data": data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch history: {str(e)}"
        )


@router.get("/trending")
async def get_trending():
    """
    Get trending cryptocurrencies

    Example: /market/trending
    """
    client = get_coingecko_client()

    try:
        data = await client.get_trending_coins()
        return {"trending": data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch trending: {str(e)}"
        )


@router.get("/search")
async def search_coins(q: str = Query(..., min_length=1, description="Search query")):
    """
    Search for cryptocurrencies

    Example: /market/search?q=bitcoin
    """
    client = get_coingecko_client()

    try:
        data = await client.search_coins(q)
        return {"results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search: {str(e)}")


@router.get("/supported")
async def get_supported_symbols():
    """
    Get list of supported cryptocurrency symbols
    """
    return {
        "symbols": list(SYMBOL_TO_ID.keys()),
        "count": len(SYMBOL_TO_ID),
        "note": "You can also use CoinGecko IDs directly (e.g., 'bitcoin', 'ethereum')",
    }
