import numpy as np
from scipy.stats import norm

def monte_carlo_option_price(S, K, r, sigma, T, num_paths):
    """Calculate the option price using Monte Carlo simulation."""
    np.random.seed(0)  # Set a seed for reproducibility
    dt = T / 252  # Assuming 252 trading days in a year
    S_paths = np.zeros((num_paths, 252))
    S_paths[:, 0] = S

    # Generate stock price paths
    for i in range(num_paths):
        for j in range(1, 252):
            z = np.random.standard_normal()
            S_paths[i, j] = S_paths[i, j-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)

    # Calculate option payoffs
    option_payoffs = np.maximum(S_paths[:, -1] - K, 0)

    # Discounted expected payoff
    option_price = np.exp(-r * T) * np.mean(option_payoffs)

    return option_price

# Parameters
stock_price = 100
strike_price = 105
risk_free_rate = 0.05
volatility = 0.2
time_to_maturity = 0.01 #Years
num_simulations = 100000

# Calculate option price using Monte Carlo simulation
option_price = monte_carlo_option_price(stock_price, strike_price, risk_free_rate, volatility, time_to_maturity, num_simulations)

print(f"The option price is: {option_price:.4f}")
