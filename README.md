# 🚀 Crypto Price Tracker & Portfolio Simulator

A comprehensive Python application for tracking cryptocurrency prices, managing portfolios, and predicting price trends using machine learning. Features real-time price tracking, portfolio management with profit/loss calculations, ML-based price predictions, and interactive data visualizations.

## ✨ Features

- 📊 **Live Crypto Prices**: Fetch real-time prices for top cryptocurrencies
- 💼 **Portfolio Management**: Track your investments with buy/sell functionality
- 🤖 **ML Predictions**: Simple machine learning models to predict price trends
- 📈 **Price History**: View historical price data and trends
- 💰 **Profit/Loss Tracking**: Calculate your gains and losses automatically
- 📉 **Visualizations**: Beautiful charts and graphs for price analysis

## 🛠️ Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the main application:
```bash
python main.py
```

## 📚 Project Structure

```
crypto-tracker/
├── main.py                 # Main application entry point
├── api_service.py          # Crypto API integration
├── portfolio.py            # Portfolio management
├── ml_predictor.py         # Machine learning predictions
├── visualizer.py           # Data visualization
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Key Learning Concepts

- **API Integration**: Fetching data from external APIs (CoinGecko)
- **Data Management**: Storing and managing portfolio data
- **Machine Learning**: Linear regression for price prediction
- **Data Visualization**: Creating charts with matplotlib
- **Object-Oriented Programming**: Clean code structure
- **Error Handling**: Robust error management

## 📖 How It Works

1. **Price Fetching**: Uses CoinGecko API (free, no API key required)
2. **Portfolio**: Stores your holdings in a JSON file
3. **ML Predictions**: Uses scikit-learn's Linear Regression on historical data
4. **Visualizations**: Matplotlib for price charts and trends

## 🔧 Configuration

The app uses CoinGecko's free API. No API key is required for basic usage.

## 📝 Example Usage

```python
# View live prices
python main.py

# The interactive menu will guide you through:
# - Viewing crypto prices
# - Adding to portfolio
# - Viewing portfolio
# - Getting price predictions
# - Viewing charts

# Crypto-Price-Tracker
