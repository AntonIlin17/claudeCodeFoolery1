"""
Configuration management for the AI Stock Trading Advisor
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # AI Model settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'llama-3.1-70b-versatile')

    # Trading settings
    DEFAULT_SYMBOLS = os.getenv('DEFAULT_SYMBOLS', 'AAPL,GOOGL,MSFT,TSLA,NVDA').split(',')
    ANALYSIS_DAYS = int(os.getenv('ANALYSIS_DAYS', '30'))

    # News settings
    MAX_NEWS_ITEMS = 10

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GROQ_API_KEY and not cls.OPENAI_API_KEY:
            return False, "No API key found. Please set GROQ_API_KEY or OPENAI_API_KEY in .env file"
        return True, "Configuration valid"

    @classmethod
    def get_api_provider(cls):
        """Determine which API provider to use"""
        if cls.GROQ_API_KEY:
            return 'groq'
        elif cls.OPENAI_API_KEY:
            return 'openai'
        return None
