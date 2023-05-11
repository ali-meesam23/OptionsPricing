import py_vollib.black_scholes.implied_volatility as iv
import pandas as pd
from market_calls import Market #Custom Questrade API Module


def calculate_volatility(asset_price, option_price, strike_price, risk_free_rate, time_to_maturity):
    """Calculate implied volatility using py_vollib."""
    try:
        implied_vol = iv.implied_volatility(option_price, asset_price, strike_price, risk_free_rate,
                                            time_to_maturity, 'c')
        return implied_vol
    except:
        return None

# Read historical price and option data from a CSV file
market = Market()

ticker = 'SPY'
time_frame = '1m'
strike = '410'
side = 'C'
expiry = '2023-05-12'

data = market.get_options_ohlc(ticker,time_frame,strike,side,expiry)

# Extract relevant columns from the data
dates = data['Date']
asset_prices = data['Underlying_Price']
option_prices = data['Option_Price']
strike_prices = data['Strike']
risk_free_rate = 0.05

# Calculate volatility for each weekly option
for i in range(len(data)):
    date = dates[i]
    asset_price = asset_prices[i]
    option_price = option_prices[i]
    strike_price = strike_prices[i]
    time_to_maturity = 7  # Assuming options expire in 7 days (weekly options)

    volatility = calculate_volatility(asset_price, option_price, strike_price, risk_free_rate, time_to_maturity)
    
    if volatility is not None:
        print(f"Date: {date} - Volatility: {volatility:.4f}")
    else:
        print(f"Date: {date} - Unable to calculate volatility")