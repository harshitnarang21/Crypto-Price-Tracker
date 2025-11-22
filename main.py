"""
Crypto Price Tracker & Portfolio Simulator
Main application entry point
"""

import sys
from api_service import CryptoAPIService
from portfolio import Portfolio
from ml_predictor import MLPredictor
from visualizer import Visualizer
from utils import (
    print_header, print_success, print_error, print_warning, print_info,
    format_currency, format_percentage, format_large_number,
    get_color_for_change, validate_float_input, validate_int_input,
    clear_screen
)
from colorama import Style


class CryptoTrackerApp:
    """Main application class"""
    
    def __init__(self):
        self.api = CryptoAPIService()
        self.portfolio = Portfolio()
        self.predictor = MLPredictor()
        self.visualizer = Visualizer()
        self.running = True
    
    def display_menu(self):
        """Display main menu"""
        print_header("🚀 Crypto Price Tracker & Portfolio Simulator")
        print("1. 📊 View Live Crypto Prices")
        print("2. 💼 Portfolio Management")
        print("3. 🤖 Price Predictions & Analysis")
        print("4. 📈 View Charts & Visualizations")
        print("5. 🔍 Search Cryptocurrencies")
        print("6. 🔥 View Trending Cryptos")
        print("7. ❌ Exit")
        print()
    
    def view_live_prices(self):
        """Display live cryptocurrency prices"""
        print_header("📊 Live Cryptocurrency Prices")
        
        print_info("Fetching latest prices...")
        prices = self.api.get_live_prices()
        
        if not prices:
            print_error("Failed to fetch prices. Please check your internet connection.")
            return
        
        print(f"\n{'Rank':<6} {'Name':<20} {'Symbol':<10} {'Price':<15} {'24h Change':<12} {'Market Cap':<15}")
        print("-" * 90)
        
        for idx, crypto in enumerate(prices[:20], 1):  # Show top 20
            change = crypto.get('change_24h', 0) or 0
            change_color = get_color_for_change(change)
            price = crypto.get('price', 0) or 0
            market_cap = crypto.get('market_cap', 0) or 0
            
            print(f"{idx:<6} {crypto.get('name', 'N/A'):<20} {crypto.get('symbol', 'N/A'):<10} "
                  f"{format_currency(price):<15} "
                  f"{change_color}{format_percentage(change):<12}{Style.RESET_ALL} "
                  f"{format_large_number(market_cap):<15}")
        
        print()
        input("Press Enter to continue...")
    
    def portfolio_menu(self):
        """Portfolio management menu"""
        while True:
            print_header("💼 Portfolio Management")
            
            # Show current portfolio summary
            summary = self.portfolio.get_portfolio_value()
            
            if summary['holdings']:
                print(f"Total Portfolio Value: {format_currency(summary['total_value'])}")
                print(f"Total Cost Basis: {format_currency(summary['total_cost'])}")
                
                profit_loss = summary['total_profit_loss']
                profit_color = get_color_for_change(profit_loss)
                print(f"Total Profit/Loss: {profit_color}{format_currency(profit_loss)} "
                      f"({format_percentage(summary['total_profit_loss_percent'])}){Style.RESET_ALL}")
                print()
                
                print("Your Holdings:")
                print(f"{'Symbol':<10} {'Amount':<15} {'Avg Buy Price':<15} {'Current Price':<15} "
                      f"{'Value':<15} {'P/L':<15}")
                print("-" * 90)
                
                for holding in summary['holdings']:
                    p_l = holding['profit_loss']
                    p_l_color = get_color_for_change(p_l)
                    print(f"{holding['symbol']:<10} {holding['amount']:<15.8f} "
                          f"{format_currency(holding['average_buy_price']):<15} "
                          f"{format_currency(holding['current_price']):<15} "
                          f"{format_currency(holding['current_value']):<15} "
                          f"{p_l_color}{format_currency(p_l):<15}{Style.RESET_ALL}")
            else:
                print_info("Your portfolio is empty. Add some cryptocurrencies to get started!")
            
            print("\nOptions:")
            print("1. Add to Portfolio")
            print("2. Remove from Portfolio")
            print("3. View Portfolio Chart")
            print("4. Clear Portfolio")
            print("5. Back to Main Menu")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_to_portfolio()
            elif choice == '2':
                self.remove_from_portfolio()
            elif choice == '3':
                self.view_portfolio_chart()
            elif choice == '4':
                confirm = input("Are you sure you want to clear your portfolio? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.portfolio.clear_portfolio()
                    print_success("Portfolio cleared!")
                input("Press Enter to continue...")
            elif choice == '5':
                break
            else:
                print_error("Invalid choice!")
                input("Press Enter to continue...")
    
    def add_to_portfolio(self):
        """Add cryptocurrency to portfolio"""
        print_header("Add to Portfolio")
        
        crypto_id = input("Enter crypto ID (e.g., 'bitcoin', 'ethereum'): ").strip().lower()
        
        # Verify crypto exists
        prices = self.api.get_live_prices([crypto_id])
        if not prices:
            print_error(f"Could not find cryptocurrency: {crypto_id}")
            input("Press Enter to continue...")
            return
        
        crypto = prices[0]
        print(f"\n{crypto['name']} ({crypto['symbol']})")
        print(f"Current Price: {format_currency(crypto['price'])}")
        
        amount = validate_float_input("Enter amount to add: ", min_value=0.00000001)
        
        use_current_price = input("Use current price? (yes/no): ").strip().lower()
        if use_current_price == 'yes':
            buy_price = None  # Will use current price
        else:
            buy_price = validate_float_input("Enter buy price: ", min_value=0)
        
        self.portfolio.add_holding(crypto_id, amount, buy_price)
        input("Press Enter to continue...")
    
    def remove_from_portfolio(self):
        """Remove cryptocurrency from portfolio"""
        print_header("Remove from Portfolio")
        
        holdings = self.portfolio.get_holdings()
        if not holdings:
            print_error("Portfolio is empty!")
            input("Press Enter to continue...")
            return
        
        print("Your Holdings:")
        crypto_list = list(holdings.keys())
        for idx, crypto_id in enumerate(crypto_list, 1):
            holding = holdings[crypto_id]
            print(f"{idx}. {holding['name']} ({holding['symbol']}) - Amount: {holding['amount']:.8f}")
        
        try:
            choice = int(input("\nSelect crypto to remove (number): "))
            if 1 <= choice <= len(crypto_list):
                crypto_id = crypto_list[choice - 1]
                holding = holdings[crypto_id]
                
                remove_all = input(f"Remove all {holding['amount']:.8f} {holding['symbol']}? (yes/no): ")
                if remove_all.lower() == 'yes':
                    self.portfolio.remove_holding(crypto_id)
                else:
                    amount = validate_float_input("Enter amount to remove: ", 
                                                 min_value=0.00000001, 
                                                 max_value=holding['amount'])
                    self.portfolio.remove_holding(crypto_id, amount)
            else:
                print_error("Invalid selection!")
        except ValueError:
            print_error("Invalid input!")
        
        input("Press Enter to continue...")
    
    def view_portfolio_chart(self):
        """Display portfolio visualization"""
        print_header("Portfolio Visualization")
        
        summary = self.portfolio.get_portfolio_value()
        if not summary['holdings']:
            print_error("Portfolio is empty!")
            input("Press Enter to continue...")
            return
        
        print_info("Generating portfolio chart...")
        self.visualizer.plot_portfolio_performance(summary)
        input("Press Enter to continue...")
    
    def prediction_menu(self):
        """Price prediction and analysis menu"""
        print_header("🤖 Price Predictions & Analysis")
        
        crypto_id = input("Enter crypto ID (e.g., 'bitcoin'): ").strip().lower()
        
        print_info("Analyzing cryptocurrency...")
        
        # Get analysis
        analysis = self.predictor.get_price_analysis(crypto_id)
        if not analysis:
            print_error(f"Could not analyze {crypto_id}")
            input("Press Enter to continue...")
            return
        
        # Display analysis
        print(f"\n📊 Price Analysis for {crypto_id.upper()}")
        print("-" * 60)
        print(f"Current Price: {format_currency(analysis['current_price'])}")
        print(f"30-Day High: {format_currency(analysis['max_price_30d'])}")
        print(f"30-Day Low: {format_currency(analysis['min_price_30d'])}")
        print(f"30-Day Average: {format_currency(analysis['avg_price_30d'])}")
        print(f"Volatility: {format_percentage(analysis['volatility_percent'])}")
        
        # Display predictions
        print("\n🤖 ML Predictions:")
        print("-" * 60)
        
        if analysis['linear_prediction']:
            pred = analysis['linear_prediction']
            change_color = get_color_for_change(pred['price_change_percent'])
            print(f"\nLinear Regression:")
            print(f"  Predicted Price (1 day): {format_currency(pred['predicted_price'])}")
            print(f"  Expected Change: {change_color}{format_percentage(pred['price_change_percent'])}{Style.RESET_ALL}")
            print(f"  Confidence: {pred['confidence_score']:.1%}")
        
        if analysis['polynomial_prediction']:
            pred = analysis['polynomial_prediction']
            change_color = get_color_for_change(pred['price_change_percent'])
            print(f"\nPolynomial Regression:")
            print(f"  Predicted Price (1 day): {format_currency(pred['predicted_price'])}")
            print(f"  Expected Change: {change_color}{format_percentage(pred['price_change_percent'])}{Style.RESET_ALL}")
            print(f"  Confidence: {pred['confidence_score']:.1%}")
        
        # Trend prediction
        trend = analysis['trend']
        if trend:
            trend_emoji = "📈" if trend == 'up' else "📉" if trend == 'down' else "➡️"
            print(f"\nTrend Prediction: {trend_emoji} {trend.upper()}")
        
        print("\nOptions:")
        print("1. View Price Chart with Prediction")
        print("2. Get Extended Prediction (3 days)")
        print("3. Back")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            print_info("Generating chart...")
            self.visualizer.plot_price_history(crypto_id, days=30, show_prediction=True)
        elif choice == '2':
            print_info("Generating extended prediction...")
            extended = self.predictor.predict_next_price(crypto_id, days_ahead=3, use_polynomial=True)
            if extended:
                print(f"\n3-Day Predictions:")
                for i, pred_price in enumerate(extended['predictions'], 1):
                    print(f"  Day {i}: {format_currency(pred_price)}")
                change_color = get_color_for_change(extended['price_change_percent'])
                print(f"  Total Change: {change_color}{format_percentage(extended['price_change_percent'])}{Style.RESET_ALL}")
        
        input("\nPress Enter to continue...")
    
    def view_charts_menu(self):
        """Charts and visualizations menu"""
        print_header("📈 Charts & Visualizations")
        
        print("1. Price History Chart")
        print("2. Price History with ML Prediction")
        print("3. Compare Multiple Cryptos")
        print("4. Back")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            crypto_id = input("Enter crypto ID: ").strip().lower()
            days = validate_int_input("Enter number of days (7/30/90/180/365): ", min_value=7, max_value=365)
            print_info("Generating chart...")
            self.visualizer.plot_price_history(crypto_id, days=days)
            input("Press Enter to continue...")
        
        elif choice == '2':
            crypto_id = input("Enter crypto ID: ").strip().lower()
            days = validate_int_input("Enter number of days: ", min_value=7, max_value=365)
            print_info("Generating chart with prediction...")
            self.visualizer.plot_price_history(crypto_id, days=days, show_prediction=True)
            input("Press Enter to continue...")
        
        elif choice == '3':
            print("Enter crypto IDs (comma-separated, e.g., bitcoin,ethereum,solana):")
            crypto_ids = [c.strip().lower() for c in input().split(',')]
            days = validate_int_input("Enter number of days: ", min_value=7, max_value=365)
            print_info("Generating comparison chart...")
            self.visualizer.plot_price_comparison(crypto_ids, days=days)
            input("Press Enter to continue...")
    
    def search_cryptos(self):
        """Search for cryptocurrencies"""
        print_header("🔍 Search Cryptocurrencies")
        
        query = input("Enter search query: ").strip()
        if not query:
            return
        
        print_info("Searching...")
        results = self.api.search_crypto(query)
        
        if not results:
            print_error("No results found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nFound {len(results)} results:\n")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result['name']} ({result['symbol'].upper()}) - ID: {result['id']}")
        
        input("\nPress Enter to continue...")
    
    def view_trending(self):
        """View trending cryptocurrencies"""
        print_header("🔥 Trending Cryptocurrencies")
        
        print_info("Fetching trending cryptos...")
        trending = self.api.get_trending()
        
        if not trending:
            print_error("Could not fetch trending data")
            input("Press Enter to continue...")
            return
        
        print(f"\n{'Rank':<6} {'Name':<25} {'Symbol':<10} {'Score':<10}")
        print("-" * 55)
        
        for idx, crypto in enumerate(trending[:10], 1):
            print(f"{idx:<6} {crypto['name']:<25} {crypto['symbol']:<10} {crypto['score']:<10.2f}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        while self.running:
            try:
                clear_screen()
                self.display_menu()
                
                choice = input("Enter your choice: ").strip()
                
                if choice == '1':
                    clear_screen()
                    self.view_live_prices()
                elif choice == '2':
                    clear_screen()
                    self.portfolio_menu()
                elif choice == '3':
                    clear_screen()
                    self.prediction_menu()
                elif choice == '4':
                    clear_screen()
                    self.view_charts_menu()
                elif choice == '5':
                    clear_screen()
                    self.search_cryptos()
                elif choice == '6':
                    clear_screen()
                    self.view_trending()
                elif choice == '7':
                    print_success("Thank you for using Crypto Tracker! Goodbye! 👋")
                    self.running = False
                else:
                    print_error("Invalid choice! Please try again.")
                    input("Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n")
                print_success("Thank you for using Crypto Tracker! Goodbye! 👋")
                self.running = False
            except Exception as e:
                print_error(f"An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Application entry point"""
    try:
        app = CryptoTrackerApp()
        app.run()
    except Exception as e:
        print_error(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

