import pandas as pd
import os
from typing import Optional, Tuple, Dict
from src.models.data_models import LivePriceData, HistoricalData

class DataProcessor:
    def __init__(self, file_path: str = "crypto_history.parquet"):
        self.file_path = file_path

    def _append_and_save(self, new_data: pd.DataFrame) -> pd.DataFrame:
        """
        Helper method to safely append new data to the existing database
        and remove any accidental duplicates.
        """
        if os.path.exists(self.file_path):
            existing_df = pd.read_parquet(self.file_path)
            # Concatenamos la base de datos vieja con los datos nuevos
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            
            # ¡TRUCO PRO! Eliminamos duplicados basándonos en fecha y moneda
            # Así, si descargas el historial de 30 días dos veces, no se ensucia la BD.
            updated_df = updated_df.drop_duplicates(subset=['timestamp', 'coin_id'], keep='last')
        else:
            updated_df = new_data
            
        # Sobreescribimos el archivo con la versión consolidada y limpia
        updated_df.to_parquet(self.file_path, index=False)
        return updated_df

    def process_and_save(self, data: LivePriceData) -> Tuple[Optional[pd.DataFrame], Optional[float]]:
        if not data:
            return None, None
            
        new_data = pd.DataFrame([{
            "timestamp": data.timestamp,
            "coin_id": data.coin_id,
            "currency": "usd", 
            "price": data.usd_price
        }])
        
        # Usamos nuestra nueva función segura
        updated_df = self._append_and_save(new_data)
        return updated_df, data.display_price
    
    def process_history_bulk(self, history: HistoricalData) -> Optional[pd.DataFrame]:
        if not history or not history.prices_usd:
            return None

        df = pd.DataFrame(history.prices_usd, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df["coin_id"] = history.coin_id
        df["currency"] = "usd"
        df = df[["timestamp", "coin_id", "currency", "price"]]
        
        # Usamos nuestra nueva función segura en lugar de sobreescribir directamente
        updated_df = self._append_and_save(df)
        return updated_df

    def analyze_local_data(self, coin_id: str) -> Optional[Dict[str, float]]:
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