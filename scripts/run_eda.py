"""
Run Exploratory Data Analysis on Brent Oil Prices
This script performs comprehensive EDA on the full Brent oil price dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create plots directory if it doesn't exist
plots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'plots')
os.makedirs(plots_dir, exist_ok=True)

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS - BRENT OIL PRICES")
print("=" * 60)

# Load the Brent oil price data
print("\n1. Loading data...")
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
df = pd.read_csv(os.path.join(data_dir, 'BrentOilPrices.csv'))

# Convert date column to datetime
df['date'] = pd.to_datetime(df['Date'])
df['price'] = df['Price']
df.set_index('date', inplace=True)

# Sort by date
df.sort_index(inplace=True)

# Display basic information
print(f"   Dataset Shape: {df.shape}")
print(f"   Date Range: {df.index.min()} to {df.index.max()}")
print(f"   Total Observations: {len(df)}")

print("\n2. Basic Statistics:")
print(df['price'].describe())

# Calculate log returns
print("\n3. Calculating log returns...")
df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
df_returns = df.dropna()

print(f"   Log Returns Statistics:")
print(df_returns['log_returns'].describe())
print(f"   Skewness: {df_returns['log_returns'].skew():.4f}")
print(f"   Kurtosis: {df_returns['log_returns'].kurtosis():.4f}")

# Stationarity tests
print("\n4. Stationarity Testing:")

def adf_test(series):
    result = adfuller(series.dropna())
    print('   Augmented Dickey-Fuller Test:')
    print(f'   ADF Statistic: {result[0]:.4f}')
    print(f'   p-value: {result[1]:.4f}')
    if result[1] < 0.05:
        print('   Result: Reject H0 - Series is stationary')
    else:
        print('   Result: Fail to reject H0 - Series is non-stationary')

def kpss_test(series):
    result = kpss(series.dropna())
    print('   KPSS Test:')
    print(f'   KPSS Statistic: {result[0]:.4f}')
    print(f'   p-value: {result[1]:.4f}')
    if result[1] < 0.05:
        print('   Result: Reject H0 - Series is non-stationary')
    else:
        print('   Result: Fail to reject H0 - Series is stationary')

print("\n   Raw Price Series:")
adf_test(df['price'])
kpss_test(df['price'])

print("\n   Log Returns Series:")
adf_test(df_returns['log_returns'])
kpss_test(df_returns['log_returns'])

# Volatility analysis
print("\n5. Volatility Analysis:")
window = 30
df_returns['rolling_volatility'] = df_returns['log_returns'].rolling(window=window).std()
print(f"   Mean Volatility (30-day window): {df_returns['rolling_volatility'].mean():.4f}")
print(f"   Max Volatility: {df_returns['rolling_volatility'].max():.4f}")
print(f"   Min Volatility: {df_returns['rolling_volatility'].min():.4f}")

# Load events data
print("\n6. Loading events data...")
events_df = pd.read_csv(os.path.join(data_dir, 'key_events_oil_prices.csv'))
events_df['date'] = pd.to_datetime(events_df['date'])
events_in_range = events_df[(events_df['date'] >= df.index.min()) & (events_df['date'] <= df.index.max())]
print(f"   Total Events: {len(events_df)}")
print(f"   Events within data range: {len(events_in_range)}")

# Generate visualizations
print("\n7. Generating visualizations...")

# Plot 1: Price series
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['price'], linewidth=1.5, alpha=0.8)
plt.title('Brent Oil Prices Over Time (1987-2022)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD per barrel)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'price_series.png'), dpi=300, bbox_inches='tight')
print("   Saved: price_series.png")

# Plot 2: Log returns
fig, axes = plt.subplots(2, 1, figsize=(14, 10))
axes[0].plot(df_returns.index, df_returns['log_returns'], linewidth=0.5, alpha=0.6)
axes[0].axhline(y=0, color='r', linestyle='--', linewidth=1)
axes[0].set_title('Log Returns of Brent Oil Prices', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date', fontsize=12)
axes[0].set_ylabel('Log Returns', fontsize=12)
axes[0].grid(True, alpha=0.3)

axes[1].hist(df_returns['log_returns'], bins=50, edgecolor='black', alpha=0.7)
axes[1].axvline(x=df_returns['log_returns'].mean(), color='r', linestyle='--', linewidth=2, 
                label=f'Mean: {df_returns["log_returns"].mean():.4f}')
axes[1].set_title('Distribution of Log Returns', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Log Returns', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'log_returns_analysis.png'), dpi=300, bbox_inches='tight')
print("   Saved: log_returns_analysis.png")

# Plot 3: Volatility
plt.figure(figsize=(14, 6))
plt.plot(df_returns.index, df_returns['rolling_volatility'], linewidth=1.5, color='orange')
plt.title(f'Rolling Volatility (Window = {window} days)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility (Std Dev)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'volatility_analysis.png'), dpi=300, bbox_inches='tight')
print("   Saved: volatility_analysis.png")

# Plot 4: Price with events
plt.figure(figsize=(16, 8))
plt.plot(df.index, df['price'], linewidth=1.5, label='Brent Oil Price', alpha=0.7)

# Add vertical lines for events
for idx, event in events_in_range.iterrows():
    color = 'red' if event['expected_impact'] == 'Positive' else 'blue'
    plt.axvline(x=event['date'], color=color, linestyle='--', alpha=0.5, linewidth=1)
    plt.text(event['date'], df['price'].max()*0.9, event['event_description'][:15] + '...', 
            rotation=90, fontsize=7, alpha=0.7)

plt.title('Brent Oil Prices with Key Events', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD per barrel)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'prices_with_events.png'), dpi=300, bbox_inches='tight')
print("   Saved: prices_with_events.png")

# Summary
print("\n" + "=" * 60)
print("EDA SUMMARY")
print("=" * 60)
print(f"Data Period: {df.index.min()} to {df.index.max()}")
print(f"Total Observations: {len(df)}")
print(f"\nPrice Statistics:")
print(f"  Mean: ${df['price'].mean():.2f}")
print(f"  Median: ${df['price'].median():.2f}")
print(f"  Std Dev: ${df['price'].std():.2f}")
print(f"  Min: ${df['price'].min():.2f}")
print(f"  Max: ${df['price'].max():.2f}")
print(f"  Total Change: ${df['price'].iloc[-1] - df['price'].iloc[0]:.2f} ({((df['price'].iloc[-1] / df['price'].iloc[0]) - 1) * 100:.1f}%)")
print(f"\nVolatility Statistics:")
print(f"  Mean Daily Volatility: {df_returns['log_returns'].std():.4f}")
print(f"  Max Daily Gain: {df_returns['log_returns'].max():.4f}")
print(f"  Max Daily Loss: {df_returns['log_returns'].min():.4f}")
print(f"\nKey Events in Dataset: {len(events_df)}")
print(f"Events within price data range: {len(events_in_range)}")
print("\nEDA completed successfully!")
print("=" * 60)