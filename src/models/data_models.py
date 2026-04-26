from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class LivePriceData:
    """Clean data model for a live price fetch."""
    coin_id: str
    usd_price: float
    display_currency: str
    display_price: float
    
    # Use default_factory to generate a new timestamp on each instance creation (avoids fixed datetime.now value)
    timestamp: datetime = field(default_factory=datetime.now) 


@dataclass
class HistoricalData:
    """Clean data model for bulk historical data."""
    coin_id: str
    prices_usd: List[List[float]] # Format by CoinGecko: [[timestamp_ms, price], ...]