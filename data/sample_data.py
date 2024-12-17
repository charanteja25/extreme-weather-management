import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(n_samples=1000):
    """Generate sample weather data for testing"""
    np.random.seed(42)
    
    # Generate timestamps
    start_date = datetime(2023, 1, 1)
    timestamps = [start_date + timedelta(hours=x) for x in range(n_samples)]
    
    # Generate weather data
    data = {
        'timestamp': timestamps,
        'temperature': np.random.normal(20, 5, n_samples),  # Mean 20°C, std 5°C
        'humidity': np.clip(np.random.normal(60, 15, n_samples), 0, 100),  # 0-100%
        'wind_speed': np.abs(np.random.normal(15, 8, n_samples)),  # Mean 15 km/h
        'precipitation': np.abs(np.random.exponential(1, n_samples)),  # Exponential distribution
        'pressure': np.random.normal(1013, 5, n_samples)  # Mean 1013 hPa
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some extreme weather events
    extreme_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    df.loc[extreme_indices, 'temperature'] += np.random.uniform(10, 15, len(extreme_indices))
    df.loc[extreme_indices, 'wind_speed'] += np.random.uniform(20, 30, len(extreme_indices))
    
    return df

if __name__ == "__main__":
    # Generate and save sample data
    df = generate_sample_data()
    df.to_csv('weather_data.csv', index=False)
    print("Sample data generated and saved to weather_data.csv")
