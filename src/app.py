"""
Flask Backend for Brent Oil Price Analysis Dashboard
Provides API endpoints for serving analysis results and data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PLOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plots')

def load_data():
    """Load Brent oil price data"""
    df = pd.read_csv(os.path.join(DATA_DIR, 'BrentOilPrices.csv'))
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price']
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df

def load_events():
    """Load events data"""
    events_df = pd.read_csv(os.path.join(DATA_DIR, 'key_events_oil_prices.csv'))
    events_df['date'] = pd.to_datetime(events_df['date'])
    return events_df

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Brent Oil Price Analysis API is running'
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data"""
    try:
        df = load_data()
        
        # Optional date range filtering
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        # Convert to JSON-serializable format
        data = []
        for date, row in df.iterrows():
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': float(row['price'])
            })
        
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/prices/summary', methods=['GET'])
def get_price_summary():
    """Get price summary statistics"""
    try:
        df = load_data()
        
        summary = {
            'mean': float(df['price'].mean()),
            'median': float(df['price'].median()),
            'std': float(df['price'].std()),
            'min': float(df['price'].min()),
            'max': float(df['price'].max()),
            'count': len(df),
            'start_date': df.index.min().strftime('%Y-%m-%d'),
            'end_date': df.index.max().strftime('%Y-%m-%d')
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get events data"""
    try:
        events_df = load_events()
        
        # Convert to JSON-serializable format
        events = []
        for _, row in events_df.iterrows():
            events.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'event_description': row['event_description'],
                'event_type': row['event_type'],
                'expected_impact': row['expected_impact']
            })
        
        return jsonify({
            'success': True,
            'events': events,
            'count': len(events)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/change-point', methods=['GET'])
def get_change_point():
    """Get change point analysis results"""
    try:
        # These results would normally come from the PyMC model
        # For now, we'll return the results from our analysis
        change_point_results = {
            'change_point_date': '2005-02-24',
            'change_point_index': 4521,
            'mean_before': 21.43,
            'mean_after': 75.60,
            'price_change': 54.17,
            'percentage_change': 252.9,
            'hdi_lower': '2005-02-16',
            'hdi_upper': '2005-03-07',
            'model_convergence': True,
            'r_hat_values': [1.00, 1.00, 1.00, 1.00]
        }
        
        return jsonify({
            'success': True,
            'results': change_point_results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analysis/eda', methods=['GET'])
def get_eda_results():
    """Get EDA analysis results"""
    try:
        df = load_data()
        
        # Calculate log returns
        df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
        df_returns = df.dropna()
        
        eda_results = {
            'data_period': {
                'start': df.index.min().strftime('%Y-%m-%d'),
                'end': df.index.max().strftime('%Y-%m-%d'),
                'observations': len(df)
            },
            'price_statistics': {
                'mean': float(df['price'].mean()),
                'median': float(df['price'].median()),
                'std': float(df['price'].std()),
                'min': float(df['price'].min()),
                'max': float(df['price'].max())
            },
            'volatility_statistics': {
                'mean_daily_volatility': float(df_returns['log_returns'].std()),
                'max_daily_gain': float(df_returns['log_returns'].max()),
                'max_daily_loss': float(df_returns['log_returns'].min())
            },
            'stationarity': {
                'raw_prices_stationary': False,
                'log_returns_stationary': True
            }
        }
        
        return jsonify({
            'success': True,
            'eda_results': eda_results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/plots/<plot_name>', methods=['GET'])
def get_plot(plot_name):
    """Get information about available plots"""
    try:
        # List of available plots
        available_plots = [
            'price_series.png',
            'log_returns_analysis.png', 
            'volatility_analysis.png',
            'prices_with_events.png',
            'trace_plots.png',
            'change_point_posterior.png',
            'parameter_posteriors.png',
            'price_with_change_point.png'
        ]
        
        if plot_name in available_plots:
            plot_path = os.path.join(PLOTS_DIR, plot_name)
            if os.path.exists(plot_path):
                return jsonify({
                    'success': True,
                    'plot_exists': True,
                    'plot_path': plot_path
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Plot file not found'
                }), 404
        else:
            return jsonify({
                'success': False,
                'error': 'Plot not found',
                'available_plots': available_plots
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/plots', methods=['GET'])
def list_plots():
    """List all available plots"""
    try:
        available_plots = [
            'price_series.png',
            'log_returns_analysis.png',
            'volatility_analysis.png', 
            'prices_with_events.png',
            'trace_plots.png',
            'change_point_posterior.png',
            'parameter_posteriors.png',
            'price_with_change_point.png'
        ]
        
        return jsonify({
            'success': True,
            'plots': available_plots,
            'count': len(available_plots)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Brent Oil Price Analysis API...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)