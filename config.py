import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'expenses.db')

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Default date format
DATE_FORMAT = '%Y-%m-%d'

# Default currency
CURRENCY = '₹'  # Indian Rupee symbol

# Default payment methods
DEFAULT_PAYMENT_METHODS = [
    'Cash',
    'Credit Card',
    'Debit Card',
    'UPI',
    'Net Banking',
    'Other'
]

# Color scheme for charts
CHART_COLORS = [
    '#4CAF50',  # Green
    '#2196F3',  # Blue
    '#FFC107',  # Amber
    '#FF5722',  # Deep Orange
    '#9C27B0',  # Purple
    '#607D8B',  # Blue Grey
    '#E91E63',  # Pink
    '#FF9800',  # Orange
    '#795548',  # Brown
    '#00BCD4'   # Cyan
]
