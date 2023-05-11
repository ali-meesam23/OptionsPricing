from DataDownload import ohlc_update
from market_calls import Market
import numpy as np
import talib as ta
from datetime import datetime, timedelta

def volatility(ticker, time_frame='1D', days_back=10, override_refresh=True):
    """
    Calculate the volatility and average true range (ATR) for a given stock.

    Parameters:
        ticker (str): Ticker symbol of the stock.
        time_frame (str, optional): Time frame for OHLC data. Default is '1D' (daily).
        days_back (int, optional): Number of days to consider for volatility calculation. Default is 10.
        override_refresh (bool, optional): Whether to force refreshing the OHLC data. Default is True.

    Returns:
        tuple: A tuple containing the calculated volatility (vol_252) and average true range (ATR) values.

    """
    market = Market()
    
    main_df = ohlc_update(ticker, time_frame, fresh_download=False)
    last_entry_date = main_df.iloc[-1].name.date()
    
    if not override_refresh:
        if last_entry_date != datetime.now().date() or last_entry_date.weekday() not in [5, 6]:
            fresh_download = False
        else:
            fresh_download = True
            print("Updating OHLC DataFrame")
            main_df = ohlc_update(ticker, time_frame, fresh_download=fresh_download)
    
    q = market.quote(ticker)
    last_price = q[ticker].lastTradePrice or main_df.iloc[-1].Open
    
    df = main_df.iloc[-days_back:-1].copy()
    df['deviations'] = np.log(df.Open / df.Open.shift(1))
    df.dropna(inplace=True)
    
    n = len(df)
    df['variance'] = df.deviations ** 2
    
    time_since_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    s = (datetime.now() - time_since_midnight).total_seconds()
    
    r_last = np.log(last_price / df.iloc[-1].Open) ** 2
    r_1 = df.variance.iloc[0]
    r_mid = df.variance[1:-1].sum()
    
    vol_252 = np.sqrt((252 / n) * (((86400 - s) / 86400) * r_1 + r_mid + r_last))
    _atr = ta.ATR(main_df.High, main_df.Low, main_df.Open, 14).values[-1]
    
    return vol_252, _atr

if __name__ == '__main__':
    ticker = 'SPY'
    time_frame = '1D'
    days_back = 12
    print(volatility(ticker, time_frame, days_back, True))
