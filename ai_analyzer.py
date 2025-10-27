"""
AI-powered stock analysis using free LLM APIs
"""
from groq import Groq
from typing import Dict, Optional
from rich.console import Console
from config import Config

console = Console()

class AIAnalyzer:
    """Uses AI models to analyze stock data and news for trading recommendations"""

    def __init__(self):
        """Initialize the AI analyzer with the configured API"""
        self.provider = Config.get_api_provider()

        if self.provider == 'groq':
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = Config.AI_MODEL
        elif self.provider == 'openai':
            # Could add OpenAI support here
            raise NotImplementedError("OpenAI provider not yet implemented. Please use Groq.")
        else:
            raise ValueError("No valid API provider configured. Please set GROQ_API_KEY in .env")

    def analyze_stock(self, stock_data: Dict, news_summary: str, market_news: str = "") -> Dict:
        """
        Analyze a single stock using AI

        Args:
            stock_data: Dictionary containing stock data
            news_summary: Formatted news summary for the stock
            market_news: General market news context

        Returns:
            Dictionary with AI analysis and recommendation
        """
        try:
            # Construct the analysis prompt
            prompt = self._build_analysis_prompt(stock_data, news_summary, market_news)

            # Call the AI model
            console.print(f"\n[cyan]Analyzing {stock_data['symbol']} with AI...[/cyan]")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert stock market analyst. Analyze the provided stock data and news,
                        then provide a clear trading recommendation. Be specific, data-driven, and consider both
                        technical indicators and news sentiment. Format your response with:
                        1. RECOMMENDATION: (BUY/HOLD/SELL)
                        2. CONFIDENCE: (High/Medium/Low)
                        3. KEY FACTORS: (List main reasons)
                        4. RISKS: (Potential concerns)
                        5. PRICE TARGET: (If applicable)

                        Remember: This is for educational purposes. Always emphasize that users should do their own research."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )

            analysis_text = response.choices[0].message.content

            # Parse the recommendation
            recommendation = self._extract_recommendation(analysis_text)

            return {
                'symbol': stock_data['symbol'],
                'recommendation': recommendation,
                'analysis': analysis_text,
                'model_used': self.model,
                'provider': self.provider
            }

        except Exception as e:
            console.print(f"[red]Error analyzing {stock_data['symbol']}: {str(e)}[/red]")
            return {
                'symbol': stock_data['symbol'],
                'recommendation': 'ERROR',
                'analysis': f"Failed to analyze: {str(e)}",
                'model_used': self.model,
                'provider': self.provider
            }

    def _build_analysis_prompt(self, stock_data: Dict, news_summary: str, market_news: str) -> str:
        """
        Build a comprehensive prompt for the AI model

        Args:
            stock_data: Stock data dictionary
            news_summary: Stock-specific news
            market_news: General market news

        Returns:
            Formatted prompt string
        """
        prompt = f"""
Please analyze the following stock and provide a trading recommendation:

STOCK DATA:
{self._format_stock_data(stock_data)}

STOCK-SPECIFIC NEWS:
{news_summary if news_summary else "No recent news available."}

GENERAL MARKET CONTEXT:
{market_news if market_news else "No general market news available."}

Based on this information, provide your analysis and recommendation.
"""
        return prompt.strip()

    def _format_stock_data(self, data: Dict) -> str:
        """Format stock data for the AI prompt"""
        return f"""
Company: {data['company_name']} ({data['symbol']})
Sector: {data['sector']}
Current Price: ${data['current_price']:.2f}
Price Change (30 days): {data['price_change_pct']:.2f}%
7-Day MA: ${data['ma_7']:.2f}
30-Day MA: ${data['ma_30']:.2f}
Volume Trend: {data['volume_trend']}
Volatility: {data['volatility']:.2f}%
52-Week High: ${data['high_52week'] if isinstance(data['high_52week'], (int, float)) else data['high_52week']}
52-Week Low: ${data['low_52week'] if isinstance(data['low_52week'], (int, float)) else data['low_52week']}
P/E Ratio: {data['pe_ratio'] if isinstance(data['pe_ratio'], (int, float)) else data['pe_ratio']}
""".strip()

    def _extract_recommendation(self, analysis_text: str) -> str:
        """
        Extract the main recommendation from AI response

        Args:
            analysis_text: Full AI analysis text

        Returns:
            Recommendation (BUY/HOLD/SELL/UNKNOWN)
        """
        text_upper = analysis_text.upper()

        # Look for explicit recommendations
        if 'RECOMMENDATION: BUY' in text_upper or 'RECOMMEND BUYING' in text_upper:
            return 'BUY'
        elif 'RECOMMENDATION: SELL' in text_upper or 'RECOMMEND SELLING' in text_upper:
            return 'SELL'
        elif 'RECOMMENDATION: HOLD' in text_upper or 'RECOMMEND HOLDING' in text_upper:
            return 'HOLD'

        # Fallback: look for keywords in first part of response
        first_lines = text_upper.split('\n')[:5]
        first_text = ' '.join(first_lines)

        if 'BUY' in first_text and 'SELL' not in first_text:
            return 'BUY'
        elif 'SELL' in first_text and 'BUY' not in first_text:
            return 'SELL'
        elif 'HOLD' in first_text:
            return 'HOLD'

        return 'UNKNOWN'

    def batch_analyze(self, stocks_data: Dict[str, Dict], stocks_news: Dict[str, str],
                     market_news: str = "") -> Dict[str, Dict]:
        """
        Analyze multiple stocks

        Args:
            stocks_data: Dictionary mapping symbols to stock data
            stocks_news: Dictionary mapping symbols to news summaries
            market_news: General market news context

        Returns:
            Dictionary mapping symbols to analysis results
        """
        results = {}

        for symbol, stock_data in stocks_data.items():
            news = stocks_news.get(symbol, "No recent news available.")
            analysis = self.analyze_stock(stock_data, news, market_news)
            results[symbol] = analysis

        return results
