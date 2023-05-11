import numpy as np
import pandas as pd
from Models.black_scholes import option_price

def closest_value_idx(input_list, input_value):
     
  arr = np.asarray(input_list)
 
  i = (np.abs(arr - input_value)).argmin()
 
  return i


def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
 
        # If x is greater, ignore left half
        if round(arr[mid],2) < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif round(arr[mid],2) > x:
            high = mid - 1
 
        # means x is present at mid
        else:
            return mid
 
    # If we reach here, then the element was not present
    return -1

import numpy as np
import pandas as pd

def true_sigma(s, k, t, r, side, opt_price, *args, **kwargs):
    """
    Estimate the implied volatility of an option.

    Parameters:
        s (float): Stock price.
        k (float): Strike price.
        t (float): Total seconds to expiry.
        r (float): Interest rate (risk-free rate).
        side (str): 'c' for a call option or 'p' for a put option.
        opt_price (float): Actual option price at the time.

    Returns:
        float: Estimated implied volatility (sigma) of the option.

    """
    stdevs = np.linspace(0.01, 3, 1500)  # Range of standard deviations

    prices = [option_price(s, k, t, r, x, side) for x in stdevs]
    std_df = pd.DataFrame({'stdev': stdevs, 'prices': prices})

    closest_idx = np.abs(std_df.prices - opt_price).idxmin()
    true_stdev = std_df.loc[closest_idx, 'stdev']

    return true_stdev

