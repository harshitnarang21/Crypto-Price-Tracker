"""
Data Visualization Module
Creates charts and graphs for cryptocurrency data
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np
from api_service import CryptoAPIService


class Visualizer:
    """Creates visualizations for cryptocurrency data"""
    
    def __init__(self):
        self.api = CryptoAPIService()
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
        except:
            try:
                plt.style.use('seaborn-darkgrid')
            except:
                plt.style.use('default')
    
    def plot_price_history(self, crypto_id: str, days: int = 30, 
                          show_prediction: bool = False, save_path: Optional[str] = None):
        """
        Plot price history chart
        
        Args:
            crypto_id: Crypto ID
            days: Number of days of history
            show_prediction: Whether to show ML prediction
            save_path: Path to save the chart (if None, displays it)
        """
        # Get historical data
        history = self.api.get_price_history(crypto_id, days)
        
        if not history:
            print(f"❌ Could not fetch data for {crypto_id}")
            return
        
        # Get crypto info for title
        crypto_info = self.api.get_crypto_info(crypto_id)
        name = crypto_info.get('name', crypto_id) if crypto_info else crypto_id
        
        # Extract data
        timestamps = [point['timestamp'] for point in history]
        prices = [point['price'] for point in history]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot price history
        ax.plot(timestamps, prices, linewidth=2, color='#2E86AB', label='Price')
        ax.fill_between(timestamps, prices, alpha=0.3, color='#2E86AB')
        
        # Add prediction if requested
        if show_prediction:
            from ml_predictor import MLPredictor
            predictor = MLPredictor()
            prediction = predictor.predict_next_price(crypto_id, days_ahead=3)
            
            if prediction:
                # Extend timeline for predictions
                last_timestamp = timestamps[-1]
                future_timestamps = [
                    last_timestamp + timedelta(days=i+1) 
                    for i in range(len(prediction['predictions']))
                ]
                
                ax.plot(future_timestamps, prediction['predictions'], 
                       '--', linewidth=2, color='#A23B72', label='Prediction')
                ax.scatter(future_timestamps, prediction['predictions'], 
                          color='#A23B72', s=100, zorder=5)
        
        # Formatting
        ax.set_title(f'{name} Price History ({days} days)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (USD)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
        plt.xticks(rotation=45)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_portfolio_performance(self, portfolio_data: Dict, save_path: Optional[str] = None):
        """
        Plot portfolio performance chart
        
        Args:
            portfolio_data: Portfolio value data from portfolio.get_portfolio_value()
            save_path: Path to save the chart
        """
        if not portfolio_data['holdings']:
            print("❌ No holdings to visualize")
            return
        
        holdings = portfolio_data['holdings']
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart: Portfolio allocation
        names = [h['symbol'] for h in holdings]
        values = [h['current_value'] for h in holdings]
        colors = plt.cm.Set3(np.linspace(0, 1, len(holdings)))
        
        ax1.pie(values, labels=names, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Portfolio Allocation', fontsize=14, fontweight='bold')
        
        # Bar chart: Profit/Loss by holding
        symbols = [h['symbol'] for h in holdings]
        profit_loss = [h['profit_loss'] for h in holdings]
        colors_bar = ['#2ECC71' if p >= 0 else '#E74C3C' for p in profit_loss]
        
        bars = ax2.barh(symbols, profit_loss, color=colors_bar)
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
        ax2.set_title('Profit/Loss by Holding', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Profit/Loss (USD)', fontsize=12)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, profit_loss)):
            ax2.text(value, i, f'${value:,.0f}', 
                    va='center', ha='left' if value >= 0 else 'right', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_price_comparison(self, crypto_ids: List[str], days: int = 30, 
                             save_path: Optional[str] = None):
        """
        Compare prices of multiple cryptocurrencies
        
        Args:
            crypto_ids: List of crypto IDs to compare
            days: Number of days of history
            save_path: Path to save the chart
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(crypto_ids)))
        
        for crypto_id, color in zip(crypto_ids, colors):
            history = self.api.get_price_history(crypto_id, days)
            if not history:
                continue
            
            timestamps = [point['timestamp'] for point in history]
            prices = [point['price'] for point in history]
            
            # Normalize prices to percentage change for comparison
            if prices:
                base_price = prices[0]
                normalized_prices = [(p / base_price - 1) * 100 for p in prices]
                
                crypto_info = self.api.get_crypto_info(crypto_id)
                name = crypto_info.get('symbol', crypto_id).upper() if crypto_info else crypto_id
                ax.plot(timestamps, normalized_prices, label=name, linewidth=2, color=color)
        
        ax.set_title(f'Price Comparison ({days} days)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price Change (%)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Chart saved to {save_path}")
        else:
            plt.show()
        
        plt.close()


if __name__ == "__main__":
    # Test visualizer
    print("🧪 Testing Visualizer...\n")
    
    viz = Visualizer()
    
    print("Creating price history chart for Bitcoin...")
    viz.plot_price_history('bitcoin', days=30, show_prediction=True)
    
    print("\n✅ Visualizer is working!")

