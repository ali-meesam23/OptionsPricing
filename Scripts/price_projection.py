import os
import sys
# sys.path.append(os.path.join(os.getenv("HOME"),"Options","SourceCode"))

import pandas as pd
import numpy as np
import pytz
from datetime import datetime
from market_calls import Market
from Helpers.true_sigma import true_sigma
from Models.black_scholes import option_price


def get_option_price_projection(ticker,days_to_expire,strike,side,s_prime,_t,d_prime=None,limitOrderStyle='last',*args,**kwargs):
    """
    ticker: Underlying
    days_to_expire: int (closed expiry to number of days to expire)
    stirke: int * closed strike available
    side: c/p
    s_prime: dollar basis (final underlying price)
    _t: Total minutes going forward from now
    limitOrderStyle: aggresive, passive, last
    """
    if d_prime !=None:
        # Further increse stop loss >> too close to the execution price
        d_prime = s_prime/2 if abs(s_prime/d_prime)>2 else d_prime

    side = side.lower()
    ZONE = 'US/Eastern'

    EASTERN =  pytz.timezone(ZONE)
    
    self = Market()

    # INIT
    pkg = ticker,days_to_expire,strike,side

    
    # Conversion to Seconds
    _t*=60
    
    
    # GET ACTUAL PARAMETERS - FIRST CALL
    q, expiry, strike = self.get_option_quote(*pkg)
    # print(q)
    # expiry to datetime
    _expiry = datetime.fromordinal(expiry.toordinal()).replace(hour=16)

    s = q.at['lastTradePrice',ticker]
    
    # $ price heading to in Dollars (final price)
    if side.lower()=='c':
        s_prime = s + s_prime 
    else:
        s_prime = s - s_prime 
        
    k = strike
    t = (_expiry-datetime.now(tz=EASTERN).replace(tzinfo=None)).total_seconds()
    print(f"Time left: {t}seconds")
    r = 0.03
    if limitOrderStyle=='last':
        opt_price = q.at['lastTradePrice',q.columns.tolist()[0]]
    elif limitOrderStyle=='aggressive':
        opt_price = q.at['askPrice',q.columns.tolist()[0]]
    elif limitOrderStyle=='passive':
        opt_price = q.at['bidPrice',q.columns.tolist()[0]]

    _pkg = s, k, t, r, side, opt_price

    sigma = true_sigma(s, k, t, r, side, opt_price)
    print(f"Optimized Sigma: {sigma}")
    
    opt_price_calculated = round(option_price(s,k,t,r,sigma,side),2)

    if opt_price==0:
        print("Using Calculated Option Price...")
        opt_price = opt_price_calculated
    
    # predict pricing (simple method - with latest optimized sigma)
    t_prime = t-_t

    # opt_price_prime = option_price(s_prime,strike,t_prime,r,sigma,side)
    opt_price_prime = opt_price+0.15

    if d_prime!=None:
        if side=='c':
            dd = s-d_prime
        else:
            dd = s+d_prime

        # opt_price_drawdown = option_price(dd,strike,t_prime,r,sigma,side)
        opt_price_drawdown = opt_price-0.15
        sl_delta = opt_price_drawdown - opt_price
    else:
        opt_price_drawdown = None

    price_delta = opt_price_prime - opt_price
    print()
    print(f"Current {ticker} Price: ${s} ---> ${round(s_prime,2)} < DD: {dd} >")
    print("_"*50)
    print(f"{q.columns.tolist()[0]}\n")
    print(f"Pricing: {opt_price} ---> {round(opt_price_prime,2)} < DD: {round(opt_price_drawdown,2)}")
    print("_"*50)
    _price_delta = f"+${round(price_delta*100,2)}" if price_delta>0 else f"-${round(price_delta*100,2)}" 
    print("Profit: "+ _price_delta + " /Contract" + f" | ~ {_price_delta[0]}{round(((opt_price_prime/opt_price) - 1)*100,1)}%")
    print("_"*50)
    try:
        print("Loss: "+ f"-${round(abs(sl_delta)*100,2)}" + " /Contract" + f" | ~ {round(((opt_price_drawdown/opt_price) - 1)*100,1)}%")
    except:
        None

    return expiry, strike, opt_price, opt_price_calculated, round(opt_price_prime,2), round(opt_price_drawdown,2)

if __name__=='__main__':
    ticker=(input("defualt - SPY >> Enter a ticker:" ) or "SPY").upper()
    days_to_expire=int(input("default - 0 >> Enter total Days to Expire: ") or 0)
    strike = int(input("Enter strike: "))
    side = input("Call (c) or Put (p)? ")
    s_prime = float(input("How much is underlying rising ($)? "))
    _t = float(input("default - 60 >> How many minutes will this swing last? ") or 60)
    d_prime = float(input("defualt -$1 >> How much DrawDown is expecged? ") or 1)
    get_option_price_projection(ticker,days_to_expire,strike,side,s_prime,_t,d_prime)

