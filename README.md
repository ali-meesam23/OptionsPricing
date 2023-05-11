# Options
Option pricing and predicting underlying price swings using black scholes

![alt text](Pattern.png)

## Models
* Black Scholes
* Monte Carlos
* Option Greeks +

## Scripts
* Option Price Projection
    ```
    ticker="SPY"
    days_to_expire=1
    strike = 414
    side = 'c'
    s_prime = 3 #$
    _t = 100 #minutes
    d_prime = 1

    get_option_price_projection(v.ticker,v.days_to_expire,v.strike,v.side,v.s_prime,v._t,v.d_prime)

    """
    >>>
    Reading Bundle...
    Old File: Last Updated 2023-04-19... Refreshing
    Retry # 1
    Reading Bundle...
    Found: $414.0 Strike!
    Time left: 84616.858995seconds
    Optimized Sigma: 0.1376584389593062

    Current SPY Price: $412.18 ---> $415.18 < DD: 410.68 >
    __________________________________________________
    SPY12May23C414.00

    Pricing: 0.49 ---> 0.64 < DD: 0.34
    __________________________________________________
    Profit: +$15.0 /Contract | ~ +30.6%
    __________________________________________________
    Loss: -$15.0 /Contract | ~ -30.6%
    """

    ```


