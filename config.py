import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Zillow API settings
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = "zillow56.p.rapidapi.com"

# Financial assumptions
LOAN_INTEREST_PERCENT = 0.04  # 4%
LOAN_TERM_YEARS = 30 # 30 Years
DOWN_PAYMENT_PERCENT = 0.20  # 20%
CLOSING_COSTS_PERCENT = 0.04 # 4%
PROPERTY_MGMT_PERCENT = 0.10  # 10%
VACANCY_PERCENT = 0.05  # 5%
MAINTENANCE_PERCENT = 0.05  # 5%
CAPEX_PERCENT = 0.05  # 5%
INSURANCE_PERCENT = 0.01  # 1%
PROPERTY_TAX_PERCENT = 0.01  # 1%
