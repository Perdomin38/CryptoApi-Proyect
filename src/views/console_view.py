# src/views/console_view.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
import pandas as pd
from typing import Dict

console = Console()

class ConsoleView:
    """Handles all terminal input/output using the rich library."""
    
    @staticmethod
    def print_menu():
        console.print("\n[bold cyan]=== CryptoTerminal Pro ===[/bold cyan]")
        console.print("[1] Fetch Live Price")
        console.print("[2] Download Historical Data (Last X Days)")
        console.print("[3] Analyze Local Database")
        console.print("[4] Exit")
        console.print("===============================\n")

    @staticmethod
    def get_menu_choice() -> str:
        return Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

    @staticmethod
    def prompt_live_price_inputs() -> tuple[str, str]:
        coin = Prompt.ask("[bold yellow]Enter cryptocurrency[/bold yellow]", default="bitcoin")
        currency = Prompt.ask("[bold yellow]Enter display currency[/bold yellow]", default="eur")
        return coin, currency

    @staticmethod
    def prompt_history_inputs() -> tuple[str, int]:
        coin = Prompt.ask("[bold yellow]Enter cryptocurrency[/bold yellow]", default="bitcoin")
        days = IntPrompt.ask("[bold yellow]How many days of history?[/bold yellow]", default=30)
        return coin, days

    @staticmethod
    def prompt_analyze_inputs() -> str:
        return Prompt.ask("[bold yellow]Which coin do you want to analyze?[/bold yellow]", default="bitcoin")

    @staticmethod
    def show_fetching_message(coin: str, currency: str = ""):
        msg = f"Fetching live data for {coin} in {currency}..." if currency else f"Fetching data for {coin}..."
        console.print(msg, style="dim")

    @staticmethod
    def show_live_data_table(coin: str, currency: str, display_price: float, total_records: int):
        table = Table(title="Live Market Data", show_header=True, header_style="bold magenta")
        table.add_column("Cryptocurrency", style="cyan")
        table.add_column("Display Price", style="bold green")
        table.add_column("Database Status", style="dim")
        
        table.add_row(
            coin.capitalize(), 
            f"{display_price:,.2f} {currency.upper()}",
            f"Saved in USD (Total records: {total_records})"
        )
        console.print(table)

    @staticmethod
    def show_history_success(records_count: int):
        console.print(f"[bold cyan]✅ Successfully saved {records_count} days of data to the database.[/bold cyan]")

    @staticmethod
    def show_analysis_table(coin: str, stats: Dict[str, float]):
        table = Table(title=f"Local Database Analysis: {coin.capitalize()}", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value (USD)", style="bold yellow")
        
        table.add_row("Total Records Found", str(stats['records']))
        table.add_row("Maximum Price", f"${stats['max_price']:,.2f}")
        table.add_row("Minimum Price", f"${stats['min_price']:,.2f}")
        table.add_row("Average Price", f"${stats['avg_price']:,.2f}")
        console.print(table)

    @staticmethod
    def show_error(message: str):
        console.print(f"[bold red]❌ {message}[/bold red]")
        
    @staticmethod
    def show_goodbye():
        console.print("[bold green]Goodbye! [/bold green]")