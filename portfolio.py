"""
Portfolio Management Module
Handles user's cryptocurrency portfolio with buy/sell operations
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from api_service import CryptoAPIService


class Portfolio:
    """Manages user's cryptocurrency portfolio"""
    
    PORTFOLIO_FILE = "portfolio.json"
    
    def __init__(self):
        self.api = CryptoAPIService()
        self.holdings = self._load_portfolio()
    
    def _load_portfolio(self) -> Dict:
        """Load portfolio from JSON file"""
        if os.path.exists(self.PORTFOLIO_FILE):
            try:
                with open(self.PORTFOLIO_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_portfolio(self):
        """Save portfolio to JSON file"""
        try:
            with open(self.PORTFOLIO_FILE, 'w') as f:
                json.dump(self.holdings, f, indent=2, default=str)
        except IOError as e:
            print(f"❌ Error saving portfolio: {e}")
    
    def add_holding(self, crypto_id: str, amount: float, buy_price: Optional[float] = None):
        """
        Add cryptocurrency to portfolio
        
        Args:
            crypto_id: Crypto ID (e.g., 'bitcoin')
            amount: Amount of crypto to add
            buy_price: Price at which it was bought (if None, uses current price)
        """
        # Get current price if not provided
        if buy_price is None:
            prices = self.api.get_live_prices([crypto_id])
            if not prices:
                print(f"❌ Could not fetch price for {crypto_id}")
                return False
            buy_price = prices[0]['price']
        
        # Get crypto info for display name
        crypto_info = self.api.get_crypto_info(crypto_id)
        name = crypto_info.get('name', crypto_id) if crypto_info else crypto_id
        symbol = crypto_info.get('symbol', '').upper() if crypto_info else ''
        
        # Add or update holding
        if crypto_id in self.holdings:
            # Calculate weighted average price
            old_amount = self.holdings[crypto_id]['amount']
            old_price = self.holdings[crypto_id]['average_buy_price']
            total_cost = (old_amount * old_price) + (amount * buy_price)
            new_amount = old_amount + amount
            new_avg_price = total_cost / new_amount
            
            self.holdings[crypto_id]['amount'] = new_amount
            self.holdings[crypto_id]['average_buy_price'] = new_avg_price
            self.holdings[crypto_id]['last_updated'] = datetime.now().isoformat()
        else:
            self.holdings[crypto_id] = {
                'name': name,
                'symbol': symbol,
                'amount': amount,
                'average_buy_price': buy_price,
                'first_purchased': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        
        self._save_portfolio()
        print(f"✅ Added {amount} {name} ({symbol}) to portfolio at ${buy_price:,.2f}")
        return True
    
    def remove_holding(self, crypto_id: str, amount: Optional[float] = None):
        """
        Remove cryptocurrency from portfolio
        
        Args:
            crypto_id: Crypto ID
            amount: Amount to remove (if None, removes all)
        """
        if crypto_id not in self.holdings:
            print(f"❌ {crypto_id} not found in portfolio")
            return False
        
        holding = self.holdings[crypto_id]
        current_amount = holding['amount']
        
        if amount is None or amount >= current_amount:
            # Remove completely
            del self.holdings[crypto_id]
            print(f"✅ Removed {holding['name']} from portfolio")
        else:
            # Remove partial amount
            holding['amount'] -= amount
            holding['last_updated'] = datetime.now().isoformat()
            print(f"✅ Removed {amount} {holding['name']} from portfolio")
        
        self._save_portfolio()
        return True
    
    def get_portfolio_value(self) -> Dict:
        """
        Calculate current portfolio value and profit/loss
        
        Returns:
            Dictionary with portfolio statistics
        """
        if not self.holdings:
            return {
                'total_value': 0,
                'total_cost': 0,
                'total_profit_loss': 0,
                'total_profit_loss_percent': 0,
                'holdings': []
            }
        
        # Get current prices for all holdings
        crypto_ids = list(self.holdings.keys())
        current_prices = self.api.get_live_prices(crypto_ids)
        # Handle case where API returns None or empty list
        if current_prices is None:
            current_prices = []
        price_dict = {crypto['id']: crypto['price'] for crypto in current_prices}
        
        total_value = 0
        total_cost = 0
        holdings_detail = []
        
        for crypto_id, holding in self.holdings.items():
            current_price = price_dict.get(crypto_id, 0)
            amount = holding['amount']
            avg_buy_price = holding['average_buy_price']
            
            current_value = amount * current_price
            cost_basis = amount * avg_buy_price
            profit_loss = current_value - cost_basis
            # Avoid division by zero
            if avg_buy_price > 0:
                profit_loss_percent = ((current_price - avg_buy_price) / avg_buy_price) * 100
            else:
                profit_loss_percent = 0.0
            
            total_value += current_value
            total_cost += cost_basis
            
            holdings_detail.append({
                'id': crypto_id,
                'name': holding.get('name', crypto_id),
                'symbol': holding.get('symbol', ''),
                'amount': amount,
                'average_buy_price': avg_buy_price,
                'current_price': current_price,
                'current_value': current_value,
                'cost_basis': cost_basis,
                'profit_loss': profit_loss,
                'profit_loss_percent': profit_loss_percent
            })
        
        total_profit_loss = total_value - total_cost
        total_profit_loss_percent = (total_profit_loss / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_percent': total_profit_loss_percent,
            'holdings': holdings_detail
        }
    
    def get_holdings(self) -> Dict:
        """Get all holdings"""
        return self.holdings
    
    def clear_portfolio(self):
        """Clear entire portfolio"""
        self.holdings = {}
        self._save_portfolio()
        print("✅ Portfolio cleared")


if __name__ == "__main__":
    # Test portfolio functionality
    print("🧪 Testing Portfolio Management...\n")
    
    portfolio = Portfolio()
    
    # Add some test holdings
    print("Adding test holdings...")
    portfolio.add_holding('bitcoin', 0.001, 45000)
    portfolio.add_holding('ethereum', 0.01, 3000)
    
    # Get portfolio value
    print("\n📊 Portfolio Summary:")
    summary = portfolio.get_portfolio_value()
    print(f"Total Value: ${summary['total_value']:,.2f}")
    print(f"Total Cost: ${summary['total_cost']:,.2f}")
    print(f"Profit/Loss: ${summary['total_profit_loss']:,.2f} ({summary['total_profit_loss_percent']:.2f}%)")
    
    print("\n✅ Portfolio Management is working!")

