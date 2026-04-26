import pytest
import os
import sys

# Add the main project path so pytest can discover the src module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.processor import DataProcessor
from src.models.data_models import LivePriceData, HistoricalData

# --- LIVE DATA TESTS ---

def test_process_valid_live_data(tmp_path):
    test_file = tmp_path / "test_history.parquet"
    processor = DataProcessor(file_path=str(test_file))
    
    # Create a mock object using our strongly-typed model
    mock_data = LivePriceData(
        coin_id="bitcoin",
        usd_price=60000.0,
        display_currency="eur", # Display currency set to EUR to match the mocked price
        display_price=55000.0
    )
    
    df, display_price = processor.process_and_save(mock_data)
    
    assert df is not None
    assert len(df) == 1
    assert df.iloc[0]['price'] == 60000.0
    assert df.iloc[0]['currency'] == "usd"
    assert display_price == 55000.0
    assert os.path.exists(test_file)

def test_process_invalid_live_data():
    processor = DataProcessor(file_path="dummy_path.parquet")
    df_empty, price_empty = processor.process_and_save(None)
    
    assert df_empty is None
    assert price_empty is None


# --- HISTORICAL DATA TESTS ---

def test_process_history_bulk(tmp_path):
    test_file = tmp_path / "test_bulk.parquet"
    processor = DataProcessor(file_path=str(test_file))

    # Mock historical data as it would be returned by the API
    mock_history = HistoricalData(
        coin_id="ethereum",
        prices_usd=[
            [1672531200000, 1500.0], # Day 1
            [1672617600000, 1600.0]  # Day 2
        ]
    )

    df = processor.process_history_bulk(mock_history)

    assert df is not None
    assert len(df) == 2
    assert df.iloc[0]['coin_id'] == "ethereum"
    assert df.iloc[0]['price'] == 1500.0


# --- DATA ANALYSIS TESTS ---

def test_analyze_local_data_success(tmp_path):
    test_file = tmp_path / "test_analyze.parquet"
    processor = DataProcessor(file_path=str(test_file))

    # First, seed the mock database to analyze it later
    mock_history = HistoricalData(
        coin_id="solana",
        prices_usd=[
            [1000000000000, 20.0],
            [2000000000000, 30.0],
            [3000000000000, 40.0]
        ]
    )
    processor.process_history_bulk(mock_history)

    # Now, execute the function we want to test
    stats = processor.analyze_local_data("solana")

    assert stats is not None
    assert stats['records'] == 3
    assert stats['max_price'] == 40.0
    assert stats['min_price'] == 20.0
    assert stats['avg_price'] == 30.0  # The exact average between 20, 30, and 40

def test_analyze_local_data_empty():
    processor = DataProcessor(file_path="non_existent_file.parquet")
    stats = processor.analyze_local_data("bitcoin")
    
    assert stats is None