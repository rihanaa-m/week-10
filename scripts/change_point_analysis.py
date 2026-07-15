"""
Bayesian Change Point Analysis for Brent Oil Prices
This script implements change point detection using PyMC
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
import warnings
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create plots directory if it doesn't exist
plots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'plots')
os.makedirs(plots_dir, exist_ok=True)

def run_change_point_analysis():
    print("=" * 60)
    print("BAYESIAN CHANGE POINT ANALYSIS - BRENT OIL PRICES")
    print("=" * 60)

    # Load data
    print("\n1. Loading data...")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    df = pd.read_csv(os.path.join(data_dir, 'BrentOilPrices.csv'))
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price']
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # Use log returns for analysis
    df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
    df_returns = df.dropna()

    print(f"   Dataset: {len(df_returns)} observations")
    print(f"   Date range: {df_returns.index.min()} to {df_returns.index.max()}")

    # Load events
    events_df = pd.read_csv(os.path.join(data_dir, 'key_events_oil_prices.csv'))
    events_df['date'] = pd.to_datetime(events_df['date'])

    print(f"   Events: {len(events_df)} major events")

    # Prepare data for modeling
    print("\n2. Preparing data for modeling...")
    prices = df['price'].values
    n = len(prices)
    time_indices = np.arange(n)

    print(f"   Total data points: {n}")
    print(f"   Time indices: 0 to {n-1}")

    # Define a simpler model focusing on mean changes
    print("\n3. Building Bayesian Change Point Model...")
    print("   Model: Single change point with mean shift")

    with pm.Model() as change_point_model:
        # Prior for change point (uniform over all possible time points)
        # We restrict to middle 50% of data to avoid edge effects
        tau = pm.DiscreteUniform('tau', lower=int(0.25*n), upper=int(0.75*n))
        
        # Priors for before and after means
        mu_before = pm.Normal('mu_before', mu=50, sigma=20)
        mu_after = pm.Normal('mu_after', mu=50, sigma=20)
        
        # Prior for standard deviation
        sigma = pm.HalfNormal('sigma', sigma=10)
        
        # Switch function to select appropriate mean
        mu = pm.math.switch(time_indices < tau, mu_before, mu_after)
        
        # Likelihood
        likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=prices)
        
        # Sample
        print("   Running MCMC sampling...")
        trace = pm.sample(2000, tune=1000, chains=2, target_accept=0.9, progressbar=False, cores=1)

    print("\n4. Model Diagnostics...")
    print("   Checking convergence and model fit")

    # Summary statistics
    summary = az.summary(trace)
    print("\n   Parameter Summary:")
    print(summary[['mean', 'sd']])

    # Check R-hat values
    rhat_values = summary['r_hat']
    print(f"\n   R-hat values (should be close to 1.0):")
    print(f"   R-hat values: {rhat_values.tolist()}")
    # Convert to float if needed
    rhat_numeric = pd.to_numeric(rhat_values, errors='coerce')
    if rhat_numeric.max() < 1.1:
        print("   Convergence: GOOD")
    else:
        print("   Convergence: NEEDS ATTENTION")

    # Extract change point distribution
    tau_samples = trace.posterior['tau'].values.flatten()
    tau_dates = df.index[tau_samples]

    print("\n5. Change Point Analysis...")
    print(f"   Most likely change point index: {np.median(tau_samples):.0f}")
    print(f"   Most likely change point date: {df.index[int(np.median(tau_samples))]}")
    print(f"   95% HDI for change point: {np.percentile(tau_samples, 2.5):.0f} to {np.percentile(tau_samples, 97.5):.0f}")
    print(f"   95% HDI for dates: {df.index[int(np.percentile(tau_samples, 2.5))]} to {df.index[int(np.percentile(tau_samples, 97.5))]}")

    # Extract parameter estimates
    mu_before_samples = trace.posterior['mu_before'].values.flatten()
    mu_after_samples = trace.posterior['mu_after'].values.flatten()

    print(f"\n   Mean before change point: ${np.median(mu_before_samples):.2f}")
    print(f"   Mean after change point: ${np.median(mu_after_samples):.2f}")
    print(f"   Price change: ${np.median(mu_after_samples) - np.median(mu_before_samples):.2f}")
    print(f"   Percentage change: {((np.median(mu_after_samples) / np.median(mu_before_samples)) - 1) * 100:.1f}%")

    # Generate visualizations
    print("\n6. Generating visualizations...")

    # Plot 1: Trace plots
    az.plot_trace(trace, var_names=['tau', 'mu_before', 'mu_after'])
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'trace_plots.png'), dpi=300, bbox_inches='tight')
    print("   Saved: trace_plots.png")

    # Plot 2: Change point posterior
    plt.figure(figsize=(12, 6))
    plt.hist(tau_dates, bins=50, edgecolor='black', alpha=0.7, density=True)
    plt.axvline(x=df.index[int(np.median(tau_samples))], color='red', linestyle='--', 
                linewidth=2, label=f'Median: {df.index[int(np.median(tau_samples))].strftime("%Y-%m-%d")}')
    plt.title('Posterior Distribution of Change Point Date', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'change_point_posterior.png'), dpi=300, bbox_inches='tight')
    print("   Saved: change_point_posterior.png")

    # Plot 3: Parameter posteriors
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].hist(mu_before_samples, bins=50, edgecolor='black', alpha=0.7, density=True)
    axes[0].axvline(x=np.median(mu_before_samples), color='red', linestyle='--', linewidth=2,
                   label=f'Median: ${np.median(mu_before_samples):.2f}')
    axes[0].set_title('Posterior Distribution: Mean Before Change Point', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Price (USD)', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].hist(mu_after_samples, bins=50, edgecolor='black', alpha=0.7, density=True)
    axes[1].axvline(x=np.median(mu_after_samples), color='red', linestyle='--', linewidth=2,
                   label=f'Median: ${np.median(mu_after_samples):.2f}')
    axes[1].set_title('Posterior Distribution: Mean After Change Point', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Price (USD)', fontsize=12)
    axes[1].set_ylabel('Density', fontsize=12)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'parameter_posteriors.png'), dpi=300, bbox_inches='tight')
    print("   Saved: parameter_posteriors.png")

    # Plot 4: Price series with detected change point
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df['price'], linewidth=1.5, alpha=0.7, label='Brent Oil Price')
    change_point_date = df.index[int(np.median(tau_samples))]
    plt.axvline(x=change_point_date, color='red', linestyle='--', linewidth=2, 
                label=f'Detected Change Point: {change_point_date.strftime("%Y-%m-%d")}')
    plt.axhline(y=np.median(mu_before_samples), color='green', linestyle=':', linewidth=1.5,
                label=f'Mean Before: ${np.median(mu_before_samples):.2f}')
    plt.axhline(y=np.median(mu_after_samples), color='orange', linestyle=':', linewidth=1.5,
                label=f'Mean After: ${np.median(mu_after_samples):.2f}')
    plt.title('Brent Oil Prices with Detected Change Point', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD per barrel)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'price_with_change_point.png'), dpi=300, bbox_inches='tight')
    print("   Saved: price_with_change_point.png")

    # Event correlation analysis
    print("\n7. Event Correlation Analysis...")
    median_change_date = df.index[int(np.median(tau_samples))]

    # Find events close to the change point
    time_window = pd.Timedelta(days=365)  # 1 year window
    nearby_events = events_df[
        (events_df['date'] >= median_change_date - time_window) & 
        (events_df['date'] <= median_change_date + time_window)
    ]

    print(f"   Events within 1 year of change point:")
    if len(nearby_events) > 0:
        for idx, event in nearby_events.iterrows():
            days_diff = (event['date'] - median_change_date).days
            print(f"   - {event['date'].strftime('%Y-%m-%d')}: {event['event_description']}")
            print(f"     ({days_diff} days from change point, Type: {event['event_type']})")
    else:
        print("   No major events found within 1 year window")

    # Check if any event is very close (within 30 days)
    very_close_events = events_df[
        (events_df['date'] >= median_change_date - pd.Timedelta(days=30)) & 
        (events_df['date'] <= median_change_date + pd.Timedelta(days=30))
    ]

    if len(very_close_events) > 0:
        print(f"\n   Events within 30 days (potentially causally related):")
        for idx, event in very_close_events.iterrows():
            days_diff = (event['date'] - median_change_date).days
            print(f"   - {event['date'].strftime('%Y-%m-%d')}: {event['event_description']}")
            print(f"     ({days_diff} days from change point)")

    # Summary
    print("\n" + "=" * 60)
    print("CHANGE POINT ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Detected Change Point: {median_change_date.strftime('%Y-%m-%d')}")
    print(f"Mean Before: ${np.median(mu_before_samples):.2f}")
    print(f"Mean After: ${np.median(mu_after_samples):.2f}")
    print(f"Price Change: ${np.median(mu_after_samples) - np.median(mu_before_samples):.2f}")
    print(f"Percentage Change: {((np.median(mu_after_samples) / np.median(mu_before_samples)) - 1) * 100:.1f}%")
    print(f"\nModel Convergence: R-hat < 1.1 = {rhat_numeric.max() < 1.1}")
    print(f"Number of nearby events (1 year): {len(nearby_events)}")
    print(f"Number of very close events (30 days): {len(very_close_events)}")
    print("\nChange point analysis completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    run_change_point_analysis()