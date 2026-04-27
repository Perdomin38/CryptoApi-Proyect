# src/controllers/controller.py
import sys
# Update imports based on your new folder structure
from src.services.api_client import CryptoAPI
from src.services.processor import DataProcessor
from src.views.console_view import ConsoleView

class MainController:
    """Orchestrates interactions between Views and Services."""
    
    def __init__(self):
        self.api = CryptoAPI()
        self.processor = DataProcessor()
        self.view = ConsoleView()

    def handle_live_price(self, coin: str, currency: str):
        self.view.show_fetching_message(coin, currency)
        live_data = self.api.get_price(coin, currency)
        
        if live_data:
            df, display_price = self.processor.process_and_save(live_data)
            self.view.show_live_data_table(coin, currency, display_price, len(df))
        else:
            self.view.show_error(f"Failed to retrieve live data for {coin}.")

    def handle_download_history(self, coin: str, days: int):
        self.view.show_fetching_message(coin)
        history_data = self.api.get_historical_data(coin, days)
        
        if history_data:
            df = self.processor.process_history_bulk(history_data)
            self.view.show_history_success(len(df))
        else:
            self.view.show_error("Failed to fetch historical data.")

    def handle_analyze_database(self, coin: str):
        stats = self.processor.analyze_local_data(coin)
        
        if stats:
            self.view.show_analysis_table(coin, stats)
        else:
            self.view.show_error(f"No data found for {coin} in the local database.")

    def run_interactive_mode(self):
        while True:
            self.view.print_menu()
            choice = self.view.get_menu_choice()
            
            if choice == "1":
                coin, currency = self.view.prompt_live_price_inputs()
                self.handle_live_price(coin, currency)
            elif choice == "2":
                coin, days = self.view.prompt_history_inputs()
                self.handle_download_history(coin, days)
            elif choice == "3":
                coin = self.view.prompt_analyze_inputs()
                self.handle_analyze_database(coin)
            elif choice == "4":
                self.view.show_goodbye()
                sys.exit(0)