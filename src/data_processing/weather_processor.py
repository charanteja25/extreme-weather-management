import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict

class WeatherDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        
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
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Add derived features
        df = self._add_derived_features(df)
        
        # Remove outliers
        df = self._remove_outliers(df)
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        # Fill missing values with forward fill, then backward fill
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(method='ffill').fillna(method='bfill')
        
        # If any missing values remain, fill with column mean
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        
        return df
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features to the dataset"""
        # Add time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        
        # Add weather condition score (example)
        df['weather_score'] = (
            df['temperature'] * 0.3 +
            df['wind_speed'] * 0.3 +
            df['precipitation'] * 0.4
        )
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame, threshold: float = 3) -> pd.DataFrame:
        """Remove outliers using z-score method"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df = df[z_scores < threshold]
            
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, list]:
        """
        Prepare features for model training
        
        Args:
            df: Preprocessed DataFrame
            
        Returns:
            Tuple containing feature array and feature names
        """
        feature_columns = ['temperature', 'humidity', 'wind_speed', 
                         'precipitation', 'pressure', 'weather_score']
        
        # Scale features
        X = self.scaler.fit_transform(df[feature_columns])
        
        return X, feature_columns
    
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
