import pandas as pd
import os
from typing import Optional, Tuple, Dict
from src.models.data_models import LivePriceData, HistoricalData

class DataProcessor:
    def __init__(self, file_path: str = "crypto_history.parquet"):
        """
        Initializes the DataProcessor with the target Parquet file path.
        """
        self.file_path = file_path

    def _append_and_save(self, new_data: pd.DataFrame) -> pd.DataFrame:
        """
        Helper method to safely append new data to the existing database
        and remove any accidental duplicates (Idempotency).
        """
        if os.path.exists(self.file_path):
            existing_df = pd.read_parquet(self.file_path)
            # Concatenate the existing database with the new incoming data
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            
            # Drop duplicates based on timestamp and coin_id.
            # This ensures that fetching the same historical data multiple times doesn't pollute or clutter the database.
            updated_df = updated_df.drop_duplicates(subset=['timestamp', 'coin_id'], keep='last')
        else:
            updated_df = new_data
            
        # Overwrite the file with the consolidated, clean version
        updated_df.to_parquet(self.file_path, index=False)
        return updated_df

    def process_and_save(self, data: LivePriceData) -> Tuple[Optional[pd.DataFrame], Optional[float]]:
        """
        Transforms live price data into a DataFrame and safely appends it to the database.
        Returns the updated DataFrame and the original display price.
        """
        if not data:
            return None, None
            
        new_data = pd.DataFrame([{
            "timestamp": data.timestamp,
            "coin_id": data.coin_id,
            "currency": "usd", 
            "price": data.usd_price
        }])
        
        # Use our secure helper function to append the new record
        updated_df = self._append_and_save(new_data)
        return updated_df, data.display_price
    
    def process_history_bulk(self, history: HistoricalData) -> Optional[pd.DataFrame]:
        """
        Transforms a bulk of historical data into a Pandas DataFrame, normalizes timestamps,
        and appends it safely to the local Parquet database.
        """
        if not history or not history.prices_usd:
            return None

        df = pd.DataFrame(history.prices_usd, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df["coin_id"] = history.coin_id
        df["currency"] = "usd"
        df = df[["timestamp", "coin_id", "currency", "price"]]
        
        # Use the safe append function instead of overwriting the file directly
        updated_df = self._append_and_save(df)
        return updated_df

    def analyze_local_data(self, coin_id: str) -> Optional[Dict[str, float]]:
        """
        Reads the local Parquet database and calculates basic statistical metrics
        (max, min, average prices, and record count) for a specific cryptocurrency.
        """
        if not os.path.exists(self.file_path):
            return None
            
        df = pd.read_parquet(self.file_path)
        df_filtered = df[df['coin_id'] == coin_id.lower()]
        
        if df_filtered.empty:
            return None
            
        return {
            "max_price": df_filtered['price'].max(),
            "min_price": df_filtered['price'].min(),
            "avg_price": df_filtered['price'].mean(),
            "records": len(df_filtered)
        }