#!/usr/bin/env python3
"""
AI Stock Trading Advisor - Main CLI Interface

A free AI-powered stock trading recommendation system
"""
import sys
import argparse
from typing import List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from config import Config
from trading_advisor import TradingAdvisor

console = Console()

def print_banner():
    """Display the application banner"""
    banner = """
[bold cyan]╔═══════════════════════════════════════════╗
║   AI Stock Trading Advisor                ║
║   Powered by Free AI Models               ║
╚═══════════════════════════════════════════╝[/bold cyan]

[dim]Get AI-powered stock recommendations based on
real-time data and market news analysis[/dim]
"""
    console.print(banner)

def validate_config() -> bool:
    """Validate configuration and guide user if needed"""
    valid, msg = Config.validate()

    if not valid:
        console.print(Panel(
            f"[bold red]Configuration Error[/bold red]\n\n{msg}\n\n"
            "[bold]Setup Instructions:[/bold]\n"
            "1. Copy .env.example to .env\n"
            "2. Get a free API key from https://console.groq.com/\n"
            "3. Add your API key to the .env file\n"
            "4. Run this program again",
            title="Setup Required",
            border_style="red"
        ))
        return False

    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='AI Stock Trading Advisor - Get AI-powered stock recommendations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Interactive mode with default stocks
  %(prog)s -s AAPL GOOGL MSFT      # Analyze specific stocks
  %(prog)s -s TSLA -d 60            # Analyze TSLA with 60 days of data
  %(prog)s --quick NVDA             # Quick check on NVDA
  %(prog)s --list                   # Show default stocks

Free API Key: https://console.groq.com/
        """
    )

    parser.add_argument(
        '-s', '--symbols',
        nargs='+',
        help='Stock symbols to analyze (e.g., AAPL GOOGL MSFT)'
    )

    parser.add_argument(
        '-d', '--days',
        type=int,
        default=Config.ANALYSIS_DAYS,
        help=f'Number of days of historical data (default: {Config.ANALYSIS_DAYS})'
    )

    parser.add_argument(
        '--quick',
        type=str,
        metavar='SYMBOL',
        help='Quick analysis of a single stock'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List default stock symbols'
    )

    parser.add_argument(
        '--no-market-news',
        action='store_true',
        help='Skip general market news (faster)'
    )

    return parser.parse_args()

def interactive_mode(advisor: TradingAdvisor):
    """Run in interactive mode"""
    console.print("\n[bold]Interactive Mode[/bold]")
    console.print(f"[dim]Default stocks: {', '.join(Config.DEFAULT_SYMBOLS)}[/dim]\n")

    # Ask if user wants to use default stocks or specify their own
    use_default = Confirm.ask(
        "Use default stocks?",
        default=True
    )

    if use_default:
        symbols = Config.DEFAULT_SYMBOLS
    else:
        symbols_input = Prompt.ask(
            "Enter stock symbols (comma-separated)",
            default=",".join(Config.DEFAULT_SYMBOLS)
        )
        symbols = [s.strip().upper() for s in symbols_input.split(',')]

    # Ask about analysis period
    days_input = Prompt.ask(
        "Days of historical data to analyze",
        default=str(Config.ANALYSIS_DAYS)
    )

    try:
        days = int(days_input)
        advisor.days = days
        advisor.data_fetcher.days = days
    except ValueError:
        console.print("[yellow]Invalid days value, using default[/yellow]")

    # Run analysis
    console.print(f"\n[cyan]Analyzing {len(symbols)} stocks...[/cyan]\n")
    results = advisor.analyze_stocks(symbols, include_market_news=True)

    if results:
        advisor.display_results(results)

def quick_mode(advisor: TradingAdvisor, symbol: str):
    """Run quick analysis on a single stock"""
    console.print(f"\n[bold]Quick Analysis: {symbol}[/bold]\n")

    results = advisor.analyze_stocks([symbol.upper()], include_market_news=False)

    if results:
        advisor.display_results(results)

def main():
    """Main entry point"""
    print_banner()

    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Parse arguments
    args = parse_arguments()

    # Handle --list
    if args.list:
        console.print("\n[bold]Default Stock Symbols:[/bold]")
        for symbol in Config.DEFAULT_SYMBOLS:
            console.print(f"  - {symbol}")
        console.print(f"\n[dim]You can change these in the .env file (DEFAULT_SYMBOLS)[/dim]")
        sys.exit(0)

    # Initialize advisor
    advisor = TradingAdvisor(days=args.days)

    try:
        # Handle --quick
        if args.quick:
            quick_mode(advisor, args.quick)

        # Handle explicit symbols
        elif args.symbols:
            symbols = [s.upper() for s in args.symbols]
            console.print(f"\n[cyan]Analyzing {len(symbols)} stocks...[/cyan]\n")
            results = advisor.analyze_stocks(
                symbols,
                include_market_news=not args.no_market_news
            )
            if results:
                advisor.display_results(results)

        # Interactive mode
        else:
            interactive_mode(advisor)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis interrupted by user[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if "--debug" in sys.argv:
            raise
        sys.exit(1)

if __name__ == "__main__":
    main()
