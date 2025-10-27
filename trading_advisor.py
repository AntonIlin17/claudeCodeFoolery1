"""
Main trading advisor that orchestrates data fetching, news gathering, and AI analysis
"""
from typing import List, Dict, Optional
from data_fetcher import StockDataFetcher
from news_fetcher import NewsFetcher
from ai_analyzer import AIAnalyzer
from config import Config
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class TradingAdvisor:
    """Main class that orchestrates the AI stock trading advisory system"""

    def __init__(self, days: int = None):
        """
        Initialize the trading advisor

        Args:
            days: Number of days of historical data to analyze (defaults to config)
        """
        self.days = days or Config.ANALYSIS_DAYS
        self.data_fetcher = StockDataFetcher(days=self.days)
        self.news_fetcher = NewsFetcher(max_items=Config.MAX_NEWS_ITEMS)
        self.ai_analyzer = None  # Initialized on demand

    def analyze_stocks(self, symbols: List[str], include_market_news: bool = True) -> Dict:
        """
        Complete analysis pipeline for multiple stocks

        Args:
            symbols: List of stock ticker symbols
            include_market_news: Whether to include general market news context

        Returns:
            Dictionary containing all analysis results
        """
        console.print("\n[bold cyan]AI Stock Trading Advisor[/bold cyan]")
        console.print(f"[dim]Analyzing {len(symbols)} stocks with {self.days}-day historical data[/dim]\n")

        # Step 1: Fetch stock data
        console.print("[bold]Step 1: Fetching Stock Data[/bold]")
        stocks_data = self.data_fetcher.fetch_multiple_stocks(symbols)

        if not stocks_data:
            console.print("[red]No stock data could be fetched. Exiting.[/red]")
            return {}

        # Step 2: Fetch news
        console.print("\n[bold]Step 2: Gathering News[/bold]")
        stocks_news = self.news_fetcher.fetch_news_for_symbols(symbols)

        market_news_text = ""
        if include_market_news:
            market_news_items = self.news_fetcher.fetch_general_market_news()
            market_news_text = self.news_fetcher.format_news_summary(market_news_items, limit=5)

        # Step 3: Initialize AI analyzer
        console.print("\n[bold]Step 3: AI Analysis[/bold]")
        valid, msg = Config.validate()
        if not valid:
            console.print(f"[red]Configuration Error: {msg}[/red]")
            return {}

        self.ai_analyzer = AIAnalyzer()

        # Step 4: Analyze each stock with AI
        stocks_news_formatted = {}
        for symbol in stocks_data.keys():
            news_items = stocks_news.get(symbol, [])
            stocks_news_formatted[symbol] = self.news_fetcher.format_news_summary(news_items, limit=3)

        analysis_results = self.ai_analyzer.batch_analyze(
            stocks_data,
            stocks_news_formatted,
            market_news_text
        )

        # Step 5: Compile results
        results = {
            'stocks': stocks_data,
            'news': stocks_news,
            'market_news': market_news_items if include_market_news else [],
            'analysis': analysis_results,
            'summary': self._create_summary(analysis_results)
        }

        return results

    def _create_summary(self, analysis_results: Dict[str, Dict]) -> Dict:
        """
        Create a summary of recommendations

        Args:
            analysis_results: Dictionary of AI analysis results

        Returns:
            Summary dictionary with counts and lists
        """
        buy_stocks = []
        hold_stocks = []
        sell_stocks = []
        error_stocks = []

        for symbol, analysis in analysis_results.items():
            rec = analysis['recommendation']
            if rec == 'BUY':
                buy_stocks.append(symbol)
            elif rec == 'HOLD':
                hold_stocks.append(symbol)
            elif rec == 'SELL':
                sell_stocks.append(symbol)
            else:
                error_stocks.append(symbol)

        return {
            'buy': buy_stocks,
            'hold': hold_stocks,
            'sell': sell_stocks,
            'error': error_stocks
        }

    def display_results(self, results: Dict):
        """
        Display analysis results in a formatted way

        Args:
            results: Results dictionary from analyze_stocks
        """
        if not results:
            return

        console.print("\n[bold green]Analysis Complete![/bold green]\n")

        # Display summary table
        summary = results['summary']
        table = Table(title="Recommendations Summary", show_header=True, header_style="bold magenta")
        table.add_column("Recommendation", style="cyan", width=15)
        table.add_column("Stocks", style="white")

        table.add_row("BUY", ", ".join(summary['buy']) if summary['buy'] else "None")
        table.add_row("HOLD", ", ".join(summary['hold']) if summary['hold'] else "None")
        table.add_row("SELL", ", ".join(summary['sell']) if summary['sell'] else "None")

        if summary['error']:
            table.add_row("ERROR", ", ".join(summary['error']))

        console.print(table)

        # Display detailed analysis for each stock
        console.print("\n[bold]Detailed Analysis:[/bold]\n")

        for symbol, analysis in results['analysis'].items():
            stock_data = results['stocks'][symbol]

            # Create panel header with key metrics
            header = f"{stock_data['company_name']} ({symbol})"
            metrics = f"Price: ${stock_data['current_price']:.2f} | Change: {stock_data['price_change_pct']:.2f}% | Volatility: {stock_data['volatility']:.2f}%"

            # Color code the recommendation
            rec = analysis['recommendation']
            if rec == 'BUY':
                rec_style = "[bold green]BUY[/bold green]"
            elif rec == 'SELL':
                rec_style = "[bold red]SELL[/bold red]"
            elif rec == 'HOLD':
                rec_style = "[bold yellow]HOLD[/bold yellow]"
            else:
                rec_style = "[bold white]UNKNOWN[/bold white]"

            # Create panel content
            panel_content = f"""[bold]Recommendation:[/bold] {rec_style}

[dim]{metrics}[/dim]

[bold]AI Analysis:[/bold]
{analysis['analysis']}

[dim]Model: {analysis['model_used']}[/dim]
"""

            panel = Panel(
                panel_content,
                title=header,
                border_style="cyan",
                expand=False
            )

            console.print(panel)
            console.print()

        # Disclaimer
        console.print(Panel(
            "[bold yellow]DISCLAIMER[/bold yellow]\n\n"
            "This analysis is generated by AI and is for educational purposes only. "
            "It should not be considered financial advice. Always conduct your own research "
            "and consult with a qualified financial advisor before making investment decisions. "
            "Past performance does not guarantee future results.",
            border_style="yellow",
            expand=False
        ))

    def quick_check(self, symbol: str) -> Optional[Dict]:
        """
        Quick analysis of a single stock

        Args:
            symbol: Stock ticker symbol

        Returns:
            Analysis result dictionary or None
        """
        results = self.analyze_stocks([symbol], include_market_news=False)

        if results and 'analysis' in results and symbol in results['analysis']:
            return results['analysis'][symbol]

        return None
