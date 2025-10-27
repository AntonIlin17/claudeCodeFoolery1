"""
Market news fetching from free sources
"""
import feedparser
import requests
from typing import List, Dict
from datetime import datetime
from rich.console import Console

console = Console()

class NewsFetcher:
    """Fetches market and stock-related news from free sources"""

    # Free RSS feeds for financial news
    NEWS_SOURCES = {
        'yahoo_finance': 'https://finance.yahoo.com/news/rssindex',
        'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories/',
        'reuters_business': 'https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best',
        'seeking_alpha': 'https://seekingalpha.com/market_currents.xml',
    }

    def __init__(self, max_items: int = 10):
        """
        Initialize news fetcher

        Args:
            max_items: Maximum number of news items to fetch per source
        """
        self.max_items = max_items

    def fetch_general_market_news(self) -> List[Dict]:
        """
        Fetch general market news from multiple sources

        Returns:
            List of news items with title, summary, link, and published date
        """
        all_news = []

        console.print("\n[cyan]Fetching market news...[/cyan]")

        for source_name, url in self.NEWS_SOURCES.items():
            try:
                console.print(f"  {source_name}...", end=" ")
                feed = feedparser.parse(url)

                for entry in feed.entries[:self.max_items]:
                    news_item = {
                        'source': source_name,
                        'title': entry.get('title', 'No title'),
                        'summary': entry.get('summary', entry.get('description', 'No summary')),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', 'Unknown date')
                    }
                    all_news.append(news_item)

                console.print(f"[green]✓ ({len(feed.entries[:self.max_items])} items)[/green]")

            except Exception as e:
                console.print(f"[yellow]✗ (Error: {str(e)})[/yellow]")

        return all_news

    def fetch_symbol_specific_news(self, symbol: str) -> List[Dict]:
        """
        Fetch news specific to a stock symbol using Yahoo Finance

        Args:
            symbol: Stock ticker symbol

        Returns:
            List of news items related to the symbol
        """
        news_items = []

        try:
            # Yahoo Finance provides RSS feeds for specific symbols
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
            feed = feedparser.parse(url)

            for entry in feed.entries[:self.max_items]:
                news_item = {
                    'source': 'yahoo_finance',
                    'symbol': symbol,
                    'title': entry.get('title', 'No title'),
                    'summary': entry.get('summary', 'No summary'),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', 'Unknown date')
                }
                news_items.append(news_item)

        except Exception as e:
            console.print(f"[yellow]Warning: Could not fetch news for {symbol}: {str(e)}[/yellow]")

        return news_items

    def fetch_news_for_symbols(self, symbols: List[str]) -> Dict[str, List[Dict]]:
        """
        Fetch news for multiple stock symbols

        Args:
            symbols: List of stock ticker symbols

        Returns:
            Dictionary mapping symbols to their news items
        """
        results = {}

        console.print("\n[cyan]Fetching symbol-specific news...[/cyan]")

        for symbol in symbols:
            console.print(f"  {symbol}...", end=" ")
            news = self.fetch_symbol_specific_news(symbol.strip().upper())
            if news:
                results[symbol] = news
                console.print(f"[green]✓ ({len(news)} items)[/green]")
            else:
                console.print("[yellow]✗ (No news)[/yellow]")
                results[symbol] = []

        return results

    def format_news_summary(self, news_items: List[Dict], limit: int = 5) -> str:
        """
        Format news items into a readable summary for AI analysis

        Args:
            news_items: List of news items
            limit: Maximum number of items to include

        Returns:
            Formatted string summary
        """
        if not news_items:
            return "No recent news available."

        summary = "Recent News:\n\n"

        for i, item in enumerate(news_items[:limit], 1):
            summary += f"{i}. {item['title']}\n"
            summary += f"   Source: {item['source']}\n"
            summary += f"   Published: {item['published']}\n"

            # Clean up summary text
            item_summary = item['summary'].replace('<p>', '').replace('</p>', '').strip()
            if len(item_summary) > 200:
                item_summary = item_summary[:200] + "..."

            summary += f"   Summary: {item_summary}\n\n"

        return summary.strip()

    def get_news_sentiment_keywords(self, news_items: List[Dict]) -> Dict[str, int]:
        """
        Extract basic sentiment keywords from news (simple implementation)

        Args:
            news_items: List of news items

        Returns:
            Dictionary with counts of positive/negative keywords
        """
        positive_keywords = ['surge', 'gain', 'rise', 'up', 'growth', 'profit', 'beat', 'strong', 'bullish', 'record', 'high']
        negative_keywords = ['fall', 'drop', 'down', 'loss', 'decline', 'weak', 'bearish', 'concern', 'risk', 'low', 'crash']

        positive_count = 0
        negative_count = 0

        for item in news_items:
            text = (item['title'] + ' ' + item['summary']).lower()

            for keyword in positive_keywords:
                positive_count += text.count(keyword)

            for keyword in negative_keywords:
                negative_count += text.count(keyword)

        return {
            'positive': positive_count,
            'negative': negative_count,
            'sentiment': 'positive' if positive_count > negative_count else 'negative' if negative_count > positive_count else 'neutral'
        }
