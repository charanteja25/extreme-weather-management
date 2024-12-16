import pytest
import pandas as pd
import numpy as np
from src.data_processing.weather_processor import WeatherDataProcessor

@pytest.fixture
def sample_data():
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=n_samples, freq='H'),
        'temperature': np.random.normal(20, 5, n_samples),
        'humidity': np.random.normal(60, 10, n_samples),
        'wind_speed': np.random.normal(15, 5, n_samples),
        'precipitation': np.random.exponential(1, n_samples),
        'pressure': np.random.normal(1013, 5, n_samples)
    }
    
    return pd.DataFrame(data)

@pytest.fixture
def processor():
    return WeatherDataProcessor()

def test_preprocess_data(processor, sample_data):
    processed_df = processor.preprocess_data(sample_data)
    
    # Check if all required columns are present
    required_columns = ['temperature', 'humidity', 'wind_speed', 
                       'precipitation', 'pressure', 'weather_score']
    assert all(col in processed_df.columns for col in required_columns)
    
    # Check if there are no missing values
    assert not processed_df.isnull().any().any()
    
    # Check if derived features are created
    assert 'hour' in processed_df.columns
    assert 'day_of_week' in processed_df.columns
    assert 'month' in processed_df.columns

def test_prepare_features(processor, sample_data):
    processed_df = processor.preprocess_data(sample_data)
    X, feature_names = processor.prepare_features(processed_df)
    
    # Check output shapes and types
    assert isinstance(X, np.ndarray)
    assert isinstance(feature_names, list)
    assert len(feature_names) == X.shape[1]
    
    # Check if features are scaled
    assert np.abs(X.mean()) < 1e-10  # Close to 0
    assert np.abs(X.std() - 1) < 1e-10  # Close to 1

def test_handle_missing_values(processor):
    # Create data with missing values
    data = pd.DataFrame({
        'temperature': [20, np.nan, 22, np.nan],
        'humidity': [60, 65, np.nan, 70],
        'wind_speed': [15, np.nan, np.nan, 18],
        'precipitation': [1, 2, np.nan, 4],
        'pressure': [1013, np.nan, 1015, 1016],
        'timestamp': pd.date_range(start='2023-01-01', periods=4)
    })
    
    processed_data = processor._handle_missing_values(data)
    
    # Check if there are no missing values
    assert not processed_data.isnull().any().any()
    
    # Check if values are within reasonable ranges
    assert processed_data['temperature'].between(0, 50).all()
    assert processed_data['humidity'].between(0, 100).all()
    assert processed_data['wind_speed'].between(0, 100).all()
    assert processed_data['precipitation'].between(0, 1000).all()
    assert processed_data['pressure'].between(900, 1100).all()

def test_remove_outliers(processor, sample_data):
    # Add some outliers
    sample_data.loc[0, 'temperature'] = 1000  # Unrealistic temperature
    sample_data.loc[1, 'wind_speed'] = -500   # Negative wind speed
    
    processed_data = processor._remove_outliers(sample_data)
    
    # Check if outliers are removed
    assert processed_data['temperature'].max() < 50  # Reasonable max temperature
    assert processed_data['wind_speed'].min() >= 0   # Non-negative wind speed
    
    # Check if normal data is preserved
    assert len(processed_data) >= len(sample_data) - 2  # At most 2 rows removed

def test_add_derived_features(processor, sample_data):
    processed_data = processor._add_derived_features(sample_data)
    
    # Check if all derived features are present
    derived_features = ['hour', 'day_of_week', 'month', 'weather_score']
    assert all(feature in processed_data.columns for feature in derived_features)
    
    # Check derived feature ranges
    assert processed_data['hour'].between(0, 23).all()
    assert processed_data['day_of_week'].between(0, 6).all()
    assert processed_data['month'].between(1, 12).all()
    assert processed_data['weather_score'].notna().all()
