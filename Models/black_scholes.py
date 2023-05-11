import numpy as np
from scipy.stats import norm


def option_price(S,K,T,r,stdev,side,*args,**kwargs):
    """
    ===BLACK SHOLES===
        S: Stock Current Price
        K: Strike Price
        T: Time Remaining - Total Seconds (float),
        r: Risk Free Rate
        stdev: Annulized Volatility (float)
        side: c/p
    """
    side = side.upper()
    # Converting seconds to years
    T = T/(60*60*24*365)
    
    def d1(S, K, T):
        return (np.log(S/K) + ((r + (stdev**2)/2) * T)) / (stdev * np.sqrt(T))

    def d2(S, K, T):
        return (np.log(S/K) + ((r - (stdev**2)/2) * T)) / (stdev * np.sqrt(T)) 

    d_uno = d1(S, K, T)
    d_dos = d2(S, K, T)
    
    if side.upper()=='C':
        return (S*norm.cdf(d_uno)) - (K*np.exp(-r*T)*norm.cdf(d_dos))
    elif side.upper()=='P':
        return (K*np.exp(-r*T)*norm.cdf(-d_dos)) - (S*norm.cdf(-d_uno))
    else:
        print("option_price()... !Error In Input Params")
        return 0




if __name__=='__main__':
    from Helpers.realtime_volatility import volatility as rt_v
    S=410
    K = 415
    T = 60*60*10
    r = 0.05
    stdev = rt_v('SPY','1D',days_back=365)[0]
    side = 'c'
    
    pkg = [S,K,T,r,stdev,side]
    print(option_price(*pkg))
