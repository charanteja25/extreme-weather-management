import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict

class WeatherDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'pressure', 'hour']
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load weather data from file
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Pandas DataFrame containing weather data
        """
        try:
            df = pd.read_csv(file_path)
            required_columns = ['timestamp', 'temperature', 'humidity', 
                             'wind_speed', 'precipitation', 'pressure']
            
            # Verify all required columns are present
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            return df
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess weather data
        
        Args:
            df: Input DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        df = df.copy()
        df = self._handle_missing_values(df)
        df = self._remove_outliers(df)
        df = self._add_derived_features(df)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        df = df.copy()
        numeric_columns = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'pressure']
        
        # Forward fill then backward fill for missing values
        df[numeric_columns] = df[numeric_columns].ffill().bfill()
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove or adjust extreme outliers"""
        df = df.copy()
        
        # Define reasonable limits for each feature
        limits = {
            'temperature': (-30, 50),  # °C
            'humidity': (0, 100),      # %
            'wind_speed': (0, 200),    # km/h
            'precipitation': (0, 500),  # mm
            'pressure': (900, 1100)    # hPa
        }
        
        # Clip values to their reasonable ranges
        for column, (min_val, max_val) in limits.items():
            if column in df.columns:
                df[column] = df[column].clip(min_val, max_val)
        
        return df
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features like hour, month, and weather score"""
        df = df.copy()
        
        # Extract time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['month'] = df['timestamp'].dt.month
        
        # Calculate weather score (example: higher score means more severe weather)
        df['weather_score'] = (
            ((df['temperature'] - 20).abs() / 10) +  # Temperature deviation from 20°C
            (df['wind_speed'] / 20) +                # Wind contribution
            (df['precipitation'] * 2) +              # Precipitation contribution
            ((df['humidity'] - 60).abs() / 20)       # Humidity deviation from 60%
        )
        
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, list]:
        """
        Prepare features for model training
        
        Args:
            df: Preprocessed DataFrame
            
        Returns:
            Tuple containing feature array and feature names
        """
        df = df.copy()
        
        # Scale the features
        X = self.scaler.fit_transform(df[self.feature_columns])
        
        return X, self.feature_columns
    
    def get_feature_importance(self, model, feature_names: list) -> Dict[str, float]:
        """
        Get feature importance scores
        
        Args:
            model: Trained model
            feature_names: List of feature names
            
        Returns:
            Dictionary of feature importance scores
        """
        try:
            importance = model.feature_importances_
            return dict(zip(feature_names, importance))
        except:
            return {}
