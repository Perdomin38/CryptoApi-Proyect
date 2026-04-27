# src/main.py
import argparse
import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.controller import MainController

def main():
    """Application entry point."""
    parser = argparse.ArgumentParser(description="CryptoTerminal Pro CLI")
    parser.add_argument("--action", choices=["fetch", "history", "analyze", "interactive"], default="interactive", help="Action to perform")
    parser.add_argument("--coin", type=str, default="bitcoin", help="Cryptocurrency ID")
    parser.add_argument("--currency", type=str, default="usd", help="Display currency")
    parser.add_argument("--days", type=int, default=30, help="Days of history to download")

    args = parser.parse_args()
    
    # Initialize the Controller
    controller = MainController()

    if args.action == "interactive":
        if len(sys.argv) == 1:
            controller.run_interactive_mode()
        else:
            controller.run_interactive_mode()
    elif args.action == "fetch":
        controller.handle_live_price(args.coin, args.currency)
    elif args.action == "history":
        controller.handle_download_history(args.coin, args.days)
    elif args.action == "analyze":
        controller.handle_analyze_database(args.coin)

if __name__ == "__main__":
    main()