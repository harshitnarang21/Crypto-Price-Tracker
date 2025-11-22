# 📚 Complete Code Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [API Documentation](#api-documentation)
4. [Dependencies & Libraries](#dependencies--libraries)
5. [Module Documentation](#module-documentation)
6. [Data Flow](#data-flow)
7. [Features Breakdown](#features-breakdown)
8. [Code Architecture](#code-architecture)

---

## Project Overview

**Crypto Price Tracker & Portfolio Simulator** is a Python-based command-line application that provides real-time cryptocurrency price tracking, portfolio management, machine learning-based price predictions, and data visualization capabilities.

### Key Capabilities:
- Real-time cryptocurrency price fetching
- Portfolio tracking with profit/loss calculations
- ML-based price predictions using Linear and Polynomial Regression
- Interactive charts and visualizations
- Search and trending cryptocurrency discovery

---

## Project Structure

```
crypto-tracker/
├── main.py              # Main application entry point and CLI interface
├── api_service.py       # CoinGecko API integration module
├── portfolio.py         # Portfolio management and tracking
├── ml_predictor.py      # Machine learning price prediction models
├── visualizer.py        # Data visualization and chart generation
├── utils.py             # Utility functions for formatting and display
├── requirements.txt     # Python package dependencies
├── README.md           # Project documentation
├── RUN.md              # Quick run guide
├── run.sh              # Automated run script
├── .gitignore          # Git ignore configuration
└── portfolio.json      # User portfolio data (auto-generated)
```

---

## API Documentation

### External API: CoinGecko API

**Base URL:** `https://api.coingecko.com/api/v3`

**API Type:** REST API (Free Tier)
**Rate Limit:** 10-50 calls per minute
**Authentication:** None required (public API)

### API Endpoints Used:

#### 1. **GET /coins/markets**
   - **Purpose:** Fetch live cryptocurrency market data
   - **Parameters:**
     - `ids`: Comma-separated list of crypto IDs
     - `vs_currency`: Currency for price (default: 'usd')
     - `order`: Sort order (default: 'market_cap_desc')
     - `per_page`: Results per page (default: 100)
     - `page`: Page number (default: 1)
     - `sparkline`: Include sparkline data (default: false)
     - `price_change_percentage`: Time period for price change (default: '24h')
   - **Returns:** Array of cryptocurrency market data objects
   - **Used in:** `api_service.py::get_live_prices()`

#### 2. **GET /coins/{id}/market_chart**
   - **Purpose:** Get historical price data for a cryptocurrency
   - **Parameters:**
     - `id`: Cryptocurrency ID (e.g., 'bitcoin')
     - `vs_currency`: Currency for price (default: 'usd')
     - `days`: Number of days of history (1, 7, 14, 30, 90, 180, 365, max)
   - **Returns:** Object containing price, market_cap, and volume arrays
   - **Used in:** `api_service.py::get_price_history()`

#### 3. **GET /coins/{id}**
   - **Purpose:** Get detailed information about a specific cryptocurrency
   - **Parameters:**
     - `id`: Cryptocurrency ID
     - `localization`: Include localized data (default: false)
     - `tickers`: Include ticker data (default: false)
     - `market_data`: Include market data (default: true)
     - `community_data`: Include community data (default: false)
     - `developer_data`: Include developer data (default: false)
     - `sparkline`: Include sparkline (default: false)
   - **Returns:** Detailed cryptocurrency information object
   - **Used in:** `api_service.py::get_crypto_info()`

#### 4. **GET /search**
   - **Purpose:** Search for cryptocurrencies by name or symbol
   - **Parameters:**
     - `query`: Search query string
   - **Returns:** Object containing arrays of matching coins, exchanges, and categories
   - **Used in:** `api_service.py::search_crypto()`

#### 5. **GET /search/trending**
   - **Purpose:** Get currently trending cryptocurrencies
   - **Parameters:** None
   - **Returns:** Object containing trending coins with scores
   - **Used in:** `api_service.py::get_trending()`

### Default Tracked Cryptocurrencies:
- bitcoin (BTC)
- ethereum (ETH)
- binancecoin (BNB)
- ripple (XRP)
- cardano (ADA)
- solana (SOL)
- polkadot (DOT)
- dogecoin (DOGE)
- matic-network (MATIC)
- litecoin (LTC)
- chainlink (LINK)
- avalanche-2 (AVAX)
- uniswap (UNI)
- cosmos (ATOM)
- algorand (ALGO)

---

## Dependencies & Libraries

### Core Dependencies:

#### 1. **requests** (>=2.31.0)
   - **Purpose:** HTTP library for making API requests
   - **Usage:** 
     - Making GET requests to CoinGecko API
     - Session management for API calls
     - Error handling for HTTP requests
   - **Used in:** `api_service.py`

#### 2. **pandas** (>=2.2.0)
   - **Purpose:** Data manipulation and analysis
   - **Usage:** 
     - Data processing (though minimal direct usage)
     - Potential future data analysis features
   - **Used in:** Implicitly through other libraries

#### 3. **numpy** (>=1.26.0)
   - **Purpose:** Numerical computing and array operations
   - **Usage:**
     - Array operations for ML features
     - Mathematical calculations in predictions
     - Data manipulation for ML models
   - **Used in:** `ml_predictor.py`, `visualizer.py`

#### 4. **scikit-learn** (>=1.3.0)
   - **Purpose:** Machine learning library
   - **Usage:**
     - `LinearRegression`: Linear regression model for price prediction
     - `PolynomialFeatures`: Feature transformation for polynomial regression
   - **Used in:** `ml_predictor.py`

#### 5. **matplotlib** (>=3.8.0)
   - **Purpose:** Data visualization and plotting
   - **Usage:**
     - Creating price history charts
     - Portfolio allocation pie charts
     - Profit/loss bar charts
     - Multi-crypto comparison charts
   - **Used in:** `visualizer.py`

#### 6. **colorama** (>=0.4.6)
   - **Purpose:** Cross-platform colored terminal text
   - **Usage:**
     - Colored output for better UX
     - Success/error/warning message formatting
     - Price change indicators (green/red)
   - **Used in:** `utils.py`, `main.py`

#### 7. **python-dotenv** (>=1.0.0)
   - **Purpose:** Environment variable management
   - **Usage:** 
     - Loading environment variables (if needed for future API keys)
     - Configuration management
   - **Note:** Currently not actively used but included for future extensibility

### Standard Library Modules Used:

- **sys**: System-specific parameters and functions
- **json**: JSON data encoding/decoding (portfolio storage)
- **os**: Operating system interface (file operations)
- **datetime**: Date and time handling
- **typing**: Type hints for better code documentation
- **time**: Time-related functions (potential rate limiting)

---

## Module Documentation

### 1. **main.py** - Main Application

**Purpose:** Entry point and CLI interface for the application

**Key Components:**
- `CryptoTrackerApp` class: Main application controller
- Menu system with 7 options
- User input handling and validation
- Error handling and graceful exits

**Main Methods:**
- `display_menu()`: Shows main menu
- `view_live_prices()`: Displays live crypto prices
- `portfolio_menu()`: Portfolio management interface
- `add_to_portfolio()`: Add crypto to portfolio
- `remove_from_portfolio()`: Remove crypto from portfolio
- `prediction_menu()`: ML prediction interface
- `view_charts_menu()`: Chart visualization menu
- `search_cryptos()`: Search functionality
- `view_trending()`: Trending cryptos display
- `run()`: Main application loop

**Dependencies:**
- All other modules (api_service, portfolio, ml_predictor, visualizer, utils)
- colorama for styling

---

### 2. **api_service.py** - API Integration

**Purpose:** Handles all communication with CoinGecko API

**Key Components:**
- `CryptoAPIService` class: API service wrapper
- Session management for efficient API calls
- Error handling and rate limit management
- Data formatting and normalization

**Main Methods:**
- `_make_request()`: Core HTTP request handler with error handling
- `get_live_prices()`: Fetch current market prices
- `get_price_history()`: Get historical price data
- `get_crypto_info()`: Get detailed crypto information
- `search_crypto()`: Search for cryptocurrencies
- `get_trending()`: Get trending cryptocurrencies

**Data Structures:**
- Returns lists of dictionaries with formatted crypto data
- Handles None values and missing data gracefully

**Error Handling:**
- HTTP errors (429 rate limiting, 404, etc.)
- Network timeouts
- Invalid responses
- Missing data fields

---

### 3. **portfolio.py** - Portfolio Management

**Purpose:** Manages user's cryptocurrency portfolio

**Key Components:**
- `Portfolio` class: Portfolio manager
- JSON-based data persistence
- Weighted average price calculation
- Profit/loss calculations

**Main Methods:**
- `_load_portfolio()`: Load portfolio from JSON file
- `_save_portfolio()`: Save portfolio to JSON file
- `add_holding()`: Add or update cryptocurrency holding
- `remove_holding()`: Remove or reduce holding
- `get_portfolio_value()`: Calculate current portfolio value and P/L
- `get_holdings()`: Get all holdings
- `clear_portfolio()`: Clear entire portfolio

**Data Storage:**
- File: `portfolio.json`
- Format: JSON with structure:
  ```json
  {
    "crypto_id": {
      "name": "Bitcoin",
      "symbol": "BTC",
      "amount": 0.001,
      "average_buy_price": 45000.00,
      "first_purchased": "2024-01-01T00:00:00",
      "last_updated": "2024-01-15T00:00:00"
    }
  }
  ```

**Features:**
- Automatic weighted average price calculation
- Real-time value calculation using current prices
- Profit/loss tracking per holding and total
- Percentage gain/loss calculations

---

### 4. **ml_predictor.py** - Machine Learning Predictions

**Purpose:** Provides ML-based price predictions

**Key Components:**
- `MLPredictor` class: ML prediction engine
- Linear Regression model
- Polynomial Regression model
- Feature engineering from historical data

**Main Methods:**
- `prepare_features()`: Convert historical data to ML features
- `predict_next_price()`: Predict future prices (1-3 days ahead)
- `predict_trend()`: Predict short-term trend (up/down/neutral)
- `get_price_analysis()`: Comprehensive price analysis

**ML Models Used:**
1. **Linear Regression** (scikit-learn)
   - Simple linear model
   - Fast predictions
   - Good baseline

2. **Polynomial Regression** (scikit-learn)
   - Degree 2 polynomial features
   - More complex patterns
   - Better for non-linear trends

**Feature Engineering:**
- Lookback window: 7 days
- Features: Last 7 days of prices
- Target: Next day's price
- Sliding window approach for multi-day predictions

**Metrics:**
- R² score for model confidence
- Price change percentage
- Trend classification

**Limitations:**
- Requires minimum 10 days of historical data
- Predictions are short-term (1-3 days)
- Market volatility affects accuracy

---

### 5. **visualizer.py** - Data Visualization

**Purpose:** Creates charts and visualizations

**Key Components:**
- `Visualizer` class: Chart generator
- Matplotlib integration
- Multiple chart types

**Main Methods:**
- `plot_price_history()`: Price history line chart
- `plot_portfolio_performance()`: Portfolio allocation and P/L charts
- `plot_price_comparison()`: Multi-crypto comparison chart

**Chart Types:**
1. **Price History Chart**
   - Line chart with filled area
   - Optional ML prediction overlay
   - Date formatting
   - Currency formatting

2. **Portfolio Performance**
   - Pie chart: Portfolio allocation
   - Bar chart: Profit/loss by holding
   - Color-coded (green/red)

3. **Price Comparison**
   - Normalized percentage change
   - Multiple cryptocurrencies
   - Comparative analysis

**Styling:**
- Seaborn darkgrid style (with fallback)
- Custom colors for different data types
- Professional formatting

---

### 6. **utils.py** - Utility Functions

**Purpose:** Helper functions for formatting and display

**Key Functions:**

**Formatting Functions:**
- `format_currency()`: Format numbers as currency ($X,XXX.XX)
- `format_percentage()`: Format as percentage (+X.XX%)
- `format_large_number()`: Format with K/M/B suffixes

**Display Functions:**
- `print_header()`: Formatted section headers
- `print_success()`: Green success messages
- `print_error()`: Red error messages
- `print_warning()`: Yellow warning messages
- `print_info()`: Blue info messages
- `get_color_for_change()`: Color based on price change
- `clear_screen()`: Clear terminal screen

**Input Validation:**
- `validate_float_input()`: Validate and get float input
- `validate_int_input()`: Validate and get integer input

**Features:**
- Handles None values gracefully
- Cross-platform color support (colorama)
- User-friendly error messages

---

## Data Flow

### 1. **Price Fetching Flow:**
```
User selects "View Live Prices"
    ↓
main.py::view_live_prices()
    ↓
api_service.py::get_live_prices()
    ↓
HTTP GET request to CoinGecko API
    ↓
API returns JSON data
    ↓
Data formatting and None handling
    ↓
Display formatted prices in terminal
```

### 2. **Portfolio Management Flow:**
```
User adds crypto to portfolio
    ↓
main.py::add_to_portfolio()
    ↓
api_service.py::get_live_prices() [for current price]
    ↓
portfolio.py::add_holding()
    ↓
Calculate weighted average price
    ↓
Save to portfolio.json
    ↓
Display confirmation
```

### 3. **ML Prediction Flow:**
```
User requests prediction
    ↓
main.py::prediction_menu()
    ↓
api_service.py::get_price_history() [30 days]
    ↓
ml_predictor.py::prepare_features() [7-day lookback]
    ↓
Train Linear/Polynomial Regression model
    ↓
Generate predictions (1-3 days ahead)
    ↓
Calculate confidence scores
    ↓
Display predictions and analysis
```

### 4. **Visualization Flow:**
```
User requests chart
    ↓
main.py::view_charts_menu()
    ↓
api_service.py::get_price_history() [if needed]
    ↓
visualizer.py::plot_*()
    ↓
matplotlib creates chart
    ↓
Display chart window
```

---

## Features Breakdown

### 1. **Live Price Tracking**
- Real-time prices for top 20 cryptocurrencies
- 24-hour price change percentage
- Market capitalization
- Color-coded price changes (green/red)
- Formatted currency display

### 2. **Portfolio Management**
- Add cryptocurrencies with amount and buy price
- Automatic weighted average price calculation
- Real-time portfolio value calculation
- Individual holding profit/loss
- Total portfolio profit/loss
- Remove holdings (full or partial)
- Clear entire portfolio

### 3. **ML Predictions**
- Linear Regression predictions
- Polynomial Regression predictions
- 1-3 day ahead forecasts
- Confidence scores (R²)
- Trend prediction (up/down/neutral)
- Price analysis with statistics

### 4. **Visualizations**
- Price history charts (7-365 days)
- Charts with ML prediction overlays
- Portfolio allocation pie charts
- Profit/loss bar charts
- Multi-crypto comparison charts

### 5. **Search & Discovery**
- Search cryptocurrencies by name/symbol
- View trending cryptocurrencies
- Top 10 search results
- Trending with scores

---

## Code Architecture

### Design Patterns:
- **Service Pattern**: API service abstraction
- **Repository Pattern**: Portfolio data persistence
- **MVC-like**: Separation of concerns (Model: data, View: display, Controller: main.py)
- **Singleton-like**: Single instances of services

### Error Handling Strategy:
- Try-except blocks in API calls
- Graceful degradation (None handling)
- User-friendly error messages
- Rate limit detection and warnings

### Data Validation:
- Input validation for user entries
- Type checking with type hints
- None value handling throughout
- Safe dictionary access with `.get()`

### Code Quality:
- Type hints for better documentation
- Docstrings for all classes and methods
- Modular design for maintainability
- Clear separation of concerns

---

## File Descriptions

### **main.py** (413 lines)
- Main application entry point
- CLI interface and menu system
- User interaction handling
- Coordinates all modules

### **api_service.py** (221 lines)
- CoinGecko API integration
- HTTP request handling
- Data formatting
- Error handling

### **portfolio.py** (216 lines)
- Portfolio data management
- JSON file I/O
- Calculations (P/L, averages)
- CRUD operations

### **ml_predictor.py** (218 lines)
- Machine learning models
- Feature engineering
- Prediction generation
- Analysis functions

### **visualizer.py** (214 lines)
- Matplotlib chart generation
- Multiple chart types
- Styling and formatting
- Data visualization

### **utils.py** (121 lines)
- Utility functions
- Formatting helpers
- Display functions
- Input validation

---

## Configuration

### Environment Variables:
- None currently required (API is public)
- Future: Can use `.env` file for API keys if needed

### Configuration Files:
- `portfolio.json`: User portfolio data (auto-generated)
- `.gitignore`: Excludes venv, __pycache__, portfolio.json

### Default Settings:
- Default cryptocurrencies: 15 popular coins
- Price currency: USD
- Historical data: 30 days default
- ML lookback: 7 days
- Chart style: Seaborn darkgrid

---

## Future Enhancement Possibilities

1. **API Enhancements:**
   - Support for multiple currencies
   - WebSocket for real-time updates
   - More API endpoints

2. **ML Improvements:**
   - LSTM models for better predictions
   - More features (volume, market cap)
   - Ensemble methods

3. **Features:**
   - Price alerts
   - Export portfolio to CSV/Excel
   - Multiple portfolios
   - Historical portfolio tracking

4. **UI/UX:**
   - Web interface
   - Mobile app
   - Better chart interactivity

---

## Technical Notes

### Rate Limiting:
- CoinGecko free API: 10-50 calls/minute
- Application handles 429 errors gracefully
- User warnings for rate limits

### Data Persistence:
- Portfolio data stored in JSON
- No database required
- Easy to backup/restore

### Performance:
- Efficient API session reuse
- Minimal data processing overhead
- Fast ML predictions (simple models)

### Compatibility:
- Python 3.7+ (tested on 3.14)
- Cross-platform (Windows, macOS, Linux)
- Terminal-based (no GUI dependencies for core features)

---

## Summary

This application demonstrates:
- **API Integration**: RESTful API consumption
- **Data Management**: JSON file I/O and persistence
- **Machine Learning**: Regression models for predictions
- **Data Visualization**: Professional charts and graphs
- **Software Engineering**: Clean code, error handling, modular design
- **User Experience**: Interactive CLI with colored output

**Total Lines of Code:** ~1,400+ lines
**Modules:** 6 main Python files
**External APIs:** 1 (CoinGecko)
**Dependencies:** 7 main packages
**Features:** 5 major feature sets

---

*Last Updated: 2024*
*Version: 1.0*

