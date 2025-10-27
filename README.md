# AI Stock Trading Advisor

An AI-powered stock trading recommendation system that uses **free AI models** to analyze stock prices and market news, providing intelligent buy/sell/hold recommendations.

## Features

- **Real-time Stock Data**: Fetches live stock prices and historical data using Yahoo Finance API
- **Market News Analysis**: Aggregates news from multiple free sources (Yahoo Finance, MarketWatch, Reuters)
- **AI-Powered Analysis**: Uses Groq's free LLM API (Llama 3.1 70B) for intelligent stock analysis
- **Technical Indicators**: Analyzes moving averages, volatility, volume trends, and more
- **Sentiment Analysis**: Processes news sentiment to inform recommendations
- **Beautiful CLI**: Rich terminal interface with color-coded recommendations and detailed reports

## Why This System?

- **100% Free**: Uses only free APIs (Groq, Yahoo Finance)
- **Fast**: Groq provides the fastest free LLM inference
- **Educational**: Learn about AI in finance and trading strategies
- **Customizable**: Easy to modify and extend

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A free Groq API key

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd claudeCodeFoolery1

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Your Free API Key

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you'll need it in the next step)

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your API key
# You can use any text editor:
nano .env
# or
vim .env
```

Add your API key to the `.env` file:
```
GROQ_API_KEY=your_actual_api_key_here
```

### 5. Run the Advisor

```bash
# Interactive mode (easiest way to start)
python main.py

# Analyze specific stocks
python main.py -s AAPL GOOGL MSFT

# Quick check on a single stock
python main.py --quick TSLA

# Analyze with more historical data
python main.py -s NVDA -d 60

# Skip general market news (faster)
python main.py -s AAPL --no-market-news
```

## Usage Examples

### Interactive Mode

The simplest way to use the advisor:

```bash
python main.py
```

You'll be prompted to:
1. Choose stocks (or use defaults)
2. Select analysis period
3. Review AI recommendations

### Command Line Mode

Analyze specific stocks directly:

```bash
# Analyze Apple, Google, and Microsoft
python main.py -s AAPL GOOGL MSFT

# Tesla with 90 days of data
python main.py -s TSLA -d 90

# Multiple tech stocks
python main.py -s NVDA AMD INTC META AMZN
```

### Quick Check

Fast analysis of a single stock:

```bash
python main.py --quick AAPL
```

### List Default Stocks

```bash
python main.py --list
```

## How It Works

### 1. Data Collection

The system fetches:
- **Stock Prices**: 30 days of historical data (configurable)
- **Technical Indicators**: Moving averages, volatility, volume trends
- **Company Info**: Market cap, P/E ratio, 52-week highs/lows
- **News**: Stock-specific and general market news

### 2. AI Analysis

The AI model analyzes:
- Price trends and momentum
- Technical indicator signals
- News sentiment
- Market context
- Risk factors

### 3. Recommendations

The AI provides:
- **BUY/HOLD/SELL** recommendation
- Confidence level (High/Medium/Low)
- Key factors driving the recommendation
- Potential risks
- Price targets (when applicable)

## Configuration

Edit `.env` to customize:

```bash
# AI Model (Groq options)
AI_MODEL=llama-3.1-70b-versatile
# or
AI_MODEL=mixtral-8x7b-32768

# Default stocks to analyze
DEFAULT_SYMBOLS=AAPL,GOOGL,MSFT,TSLA,NVDA

# Historical data period
ANALYSIS_DAYS=30
```

## Output Format

The advisor provides:

1. **Summary Table**: Quick overview of all recommendations
2. **Detailed Analysis**: For each stock:
   - Current price and metrics
   - AI recommendation with confidence
   - Detailed reasoning
   - Risk assessment
   - News context

Example output:
```
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Recommendation ┃ Stocks              ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ BUY            │ AAPL, GOOGL         │
│ HOLD           │ MSFT, NVDA          │
│ SELL           │ TSLA                │
└────────────────┴─────────────────────┘
```

## Project Structure

```
.
├── main.py              # CLI interface
├── trading_advisor.py   # Main orchestration logic
├── ai_analyzer.py       # AI model integration
├── data_fetcher.py      # Stock data retrieval
├── news_fetcher.py      # News aggregation
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment config
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Costs

All APIs used are **FREE**:

- **Groq**: Free tier includes generous token limits
- **Yahoo Finance**: Completely free, no API key needed
- **News RSS Feeds**: Free public feeds

## Limitations & Disclaimer

### Important Notes

1. **Educational Purpose**: This tool is for learning and research only
2. **Not Financial Advice**: Do not make investment decisions solely based on this tool
3. **AI Limitations**: AI can make mistakes and may not predict market movements
4. **Data Delays**: Free APIs may have delayed data
5. **Rate Limits**: Free APIs have usage limits

### Best Practices

- Always do your own research
- Consult a qualified financial advisor
- Understand the risks of trading
- Never invest more than you can afford to lose
- Past performance doesn't guarantee future results

## Troubleshooting

### "No API key found" Error

Make sure you:
1. Created the `.env` file (copied from `.env.example`)
2. Added your Groq API key to the file
3. Saved the file

### "No data found for symbol" Error

- Check that the stock symbol is correct (e.g., "AAPL" not "Apple")
- Some stocks may not have data available
- Try a different symbol

### Rate Limit Errors

Free APIs have limits. If you hit them:
- Wait a few minutes before trying again
- Analyze fewer stocks at once
- Use `--no-market-news` flag to reduce API calls

### Installation Issues

If you have trouble installing dependencies:

```bash
# Upgrade pip first
pip install --upgrade pip

# Install packages one by one
pip install yfinance
pip install groq
pip install rich
pip install pandas
pip install python-dotenv
```

## Advanced Usage

### Using as a Library

You can import and use the components in your own Python scripts:

```python
from trading_advisor import TradingAdvisor

advisor = TradingAdvisor(days=30)
results = advisor.analyze_stocks(['AAPL', 'GOOGL'])
advisor.display_results(results)
```

### Custom Stock Lists

Create a custom list of stocks:

```bash
# Tech stocks
python main.py -s AAPL GOOGL MSFT AMZN META NVDA

# EV companies
python main.py -s TSLA RIVN LCID NIO

# Banks
python main.py -s JPM BAC WFC GS MS
```

## Contributing

Contributions are welcome! Some ideas:

- Add more data sources
- Implement backtesting
- Add chart generation
- Create a web interface
- Add more AI models
- Improve news sentiment analysis

## License

MIT License - See LICENSE file for details

## Acknowledgments

- **Groq** for providing free, fast LLM inference
- **Yahoo Finance** for free stock data
- **yfinance** library for easy Python access to Yahoo Finance
- **Rich** library for beautiful terminal output

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the Groq documentation: https://console.groq.com/docs
3. Check yfinance docs: https://github.com/ranaroussi/yfinance

## Roadmap

Future improvements:
- [ ] Web dashboard
- [ ] Email alerts
- [ ] Portfolio tracking
- [ ] Backtesting capabilities
- [ ] More AI models (OpenAI, Claude, etc.)
- [ ] Real-time price alerts
- [ ] Options analysis
- [ ] Crypto support

---

**Disclaimer**: This software is for educational purposes only. Not financial advice. Use at your own risk.
