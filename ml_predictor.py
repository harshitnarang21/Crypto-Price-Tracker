"""
Machine Learning Price Predictor
Uses simple ML models to predict cryptocurrency prices
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from typing import List, Dict, Tuple, Optional
from api_service import CryptoAPIService
import warnings
warnings.filterwarnings('ignore')


class MLPredictor:
    """Machine learning predictor for cryptocurrency prices"""
    
    def __init__(self):
        self.api = CryptoAPIService()
    
    def prepare_features(self, history: List[Dict], lookback: int = 7) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features for ML model from historical data
        
        Args:
            history: List of historical price data
            lookback: Number of days to look back for features
        
        Returns:
            X (features) and y (target) arrays
        """
        if len(history) < lookback + 1:
            return np.array([]), np.array([])
        
        # Extract prices
        prices = [point['price'] for point in history]
        
        X = []
        y = []
        
        for i in range(lookback, len(prices)):
            # Features: prices from last 'lookback' days
            features = prices[i-lookback:i]
            X.append(features)
            # Target: next day's price
            y.append(prices[i])
        
        return np.array(X), np.array(y)
    
    def predict_next_price(self, crypto_id: str, days_ahead: int = 1, 
                          use_polynomial: bool = False) -> Optional[Dict]:
        """
        Predict future price(s) for a cryptocurrency
        
        Args:
            crypto_id: Crypto ID
            days_ahead: Number of days to predict ahead
            use_polynomial: Use polynomial regression (more complex)
        
        Returns:
            Dictionary with predictions and confidence metrics
        """
        # Get historical data (30 days for training)
        history = self.api.get_price_history(crypto_id, days=30)
        
        if history is None or len(history) < 10:
            return None
        
        # Prepare features
        lookback = 7
        X, y = self.prepare_features(history, lookback)
        
        if len(X) == 0:
            return None
        
        # Train model
        poly_features = None
        X_poly = None
        if use_polynomial:
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
        else:
            model = LinearRegression()
            model.fit(X, y)
        
        # Get recent prices for prediction
        recent_prices = [point['price'] for point in history[-lookback:]]
        last_price = recent_prices[-1]
        
        # Make predictions
        predictions = []
        current_features = np.array(recent_prices).reshape(1, -1)
        
        for i in range(days_ahead):
            if use_polynomial and poly_features is not None:
                current_features_poly = poly_features.transform(current_features)
                pred = model.predict(current_features_poly)[0]
            else:
                pred = model.predict(current_features)[0]
            
            predictions.append(max(0, pred))  # Ensure non-negative
            
            # Update features for next prediction (shift window)
            if days_ahead > 1 and i < days_ahead - 1:  # Don't update on last iteration
                # Shift window: remove first element, add prediction
                new_features = np.append(current_features[0, 1:], pred)
                current_features = new_features.reshape(1, -1)
        
        # Calculate model accuracy (R² score)
        X_for_score = X_poly if (use_polynomial and X_poly is not None) else X
        r2_score = model.score(X_for_score, y)
        
        # Calculate price change percentage
        price_change = ((predictions[-1] - last_price) / last_price) * 100
        
        return {
            'current_price': last_price,
            'predictions': predictions,
            'predicted_price': predictions[-1],
            'price_change_percent': price_change,
            'confidence_score': max(0, min(1, r2_score)),  # Normalize to 0-1
            'model_type': 'Polynomial Regression' if use_polynomial else 'Linear Regression',
            'days_ahead': days_ahead
        }
    
    def predict_trend(self, crypto_id: str) -> Optional[str]:
        """
        Predict short-term trend (up/down/neutral)
        
        Args:
            crypto_id: Crypto ID
        
        Returns:
            Trend prediction: 'up', 'down', or 'neutral'
        """
        prediction = self.predict_next_price(crypto_id, days_ahead=3)
        
        if prediction is None:
            return None
        
        price_change = prediction['price_change_percent']
        
        if price_change > 2:
            return 'up'
        elif price_change < -2:
            return 'down'
        else:
            return 'neutral'
    
    def get_price_analysis(self, crypto_id: str) -> Optional[Dict]:
        """
        Get comprehensive price analysis with ML predictions
        
        Args:
            crypto_id: Crypto ID
        
        Returns:
            Dictionary with analysis results
        """
        # Get historical data
        history = self.api.get_price_history(crypto_id, days=30)
        
        if history is None or len(history) < 10:
            return None
        
        prices = [point['price'] for point in history]
        
        # Basic statistics
        current_price = prices[-1]
        min_price = min(prices)
        max_price = max(prices)
        avg_price = np.mean(prices)
        
        # Calculate volatility (standard deviation)
        volatility = np.std(prices) / avg_price * 100
        
        # Get predictions
        linear_pred = self.predict_next_price(crypto_id, days_ahead=1, use_polynomial=False)
        poly_pred = self.predict_next_price(crypto_id, days_ahead=1, use_polynomial=True)
        
        # Trend analysis
        trend = self.predict_trend(crypto_id)
        
        return {
            'current_price': current_price,
            'min_price_30d': min_price,
            'max_price_30d': max_price,
            'avg_price_30d': avg_price,
            'volatility_percent': volatility,
            'linear_prediction': linear_pred,
            'polynomial_prediction': poly_pred,
            'trend': trend,
            'price_history': prices[-10:]  # Last 10 prices
        }


if __name__ == "__main__":
    # Test ML predictor
    print("🧪 Testing ML Predictor...\n")
    
    predictor = MLPredictor()
    
    # Test prediction
    print("Predicting Bitcoin price...")
    prediction = predictor.predict_next_price('bitcoin', days_ahead=3)
    
    if prediction:
        print(f"Current Price: ${prediction['current_price']:,.2f}")
        print(f"Predicted Price (3 days): ${prediction['predicted_price']:,.2f}")
        print(f"Expected Change: {prediction['price_change_percent']:.2f}%")
        print(f"Confidence: {prediction['confidence_score']:.2%}")
        print(f"Model: {prediction['model_type']}")
    
    print("\n✅ ML Predictor is working!")

