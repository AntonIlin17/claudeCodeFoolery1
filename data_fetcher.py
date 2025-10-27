"""
Stock data fetching using yfinance (Yahoo Finance API)
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from rich.console import Console

console = Console()

class StockDataFetcher:
    """Fetches and processes stock market data"""

    def __init__(self, days: int = 30):
        """
        Initialize the stock data fetcher

        Args:
            days: Number of days of historical data to fetch
        """
        self.days = days

    def fetch_stock_data(self, symbol: str) -> Optional[Dict]:
        """
        Fetch comprehensive stock data for a given symbol

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            Dictionary containing stock data or None if fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)

            # Get historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.days)
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                console.print(f"[yellow]Warning: No data found for {symbol}[/yellow]")
                return None

            # Get current info
            info = ticker.info

            # Calculate key metrics
            current_price = hist['Close'].iloc[-1]
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[0]
            price_change_pct = (price_change / hist['Close'].iloc[0]) * 100

            # Calculate moving averages
            ma_7 = hist['Close'].tail(7).mean()
            ma_30 = hist['Close'].tail(30).mean() if len(hist) >= 30 else hist['Close'].mean()

            # Volume analysis
            avg_volume = hist['Volume'].mean()
            recent_volume = hist['Volume'].tail(5).mean()
            volume_trend = "increasing" if recent_volume > avg_volume else "decreasing"

            # Volatility (standard deviation)
            volatility = hist['Close'].pct_change().std() * 100

            return {
                'symbol': symbol,
                'current_price': current_price,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'ma_7': ma_7,
                'ma_30': ma_30,
                'volume_trend': volume_trend,
                'avg_volume': avg_volume,
                'recent_volume': recent_volume,
                'volatility': volatility,
                'high_52week': info.get('fiftyTwoWeekHigh', 'N/A'),
                'low_52week': info.get('fiftyTwoWeekLow', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'company_name': info.get('longName', symbol),
                'sector': info.get('sector', 'N/A'),
                'historical_data': hist
            }

        except Exception as e:
            console.print(f"[red]Error fetching data for {symbol}: {str(e)}[/red]")
            return None

    def fetch_multiple_stocks(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Fetch data for multiple stocks

        Args:
            symbols: List of stock ticker symbols

        Returns:
            Dictionary mapping symbols to their data
        """
        results = {}

        console.print(f"\n[cyan]Fetching data for {len(symbols)} stocks...[/cyan]")

        for symbol in symbols:
            console.print(f"  Fetching {symbol}...", end=" ")
            data = self.fetch_stock_data(symbol.strip().upper())
            if data:
                results[symbol] = data
                console.print("[green]✓[/green]")
            else:
                console.print("[red]✗[/red]")

        return results

    def format_stock_summary(self, data: Dict) -> str:
        """
        Format stock data into a readable summary for AI analysis

        Args:
            data: Stock data dictionary

        Returns:
            Formatted string summary
        """
        summary = f"""
Stock: {data['company_name']} ({data['symbol']})
Sector: {data['sector']}
Current Price: ${data['current_price']:.2f}
Price Change ({self.days} days): ${data['price_change']:.2f} ({data['price_change_pct']:.2f}%)
7-Day Moving Average: ${data['ma_7']:.2f}
30-Day Moving Average: ${data['ma_30']:.2f}
Volume Trend: {data['volume_trend']}
Volatility: {data['volatility']:.2f}%
52-Week High: ${data['high_52week']:.2f if isinstance(data['high_52week'], (int, float)) else data['high_52week']}
52-Week Low: ${data['low_52week']:.2f if isinstance(data['low_52week'], (int, float)) else data['low_52week']}
P/E Ratio: {data['pe_ratio']:.2f if isinstance(data['pe_ratio'], (int, float)) else data['pe_ratio']}
"""
        return summary.strip()
