import pandas as pd
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from visualization.weather_visualization import generate_sample_weather_data

def export_data_for_tableau():
    # Generate sample data
    data = generate_sample_weather_data()
    df = pd.DataFrame(data)
    
    # Convert timestamp to proper datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Add some additional calculated fields for Tableau
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['month'] = df['timestamp'].dt.month
    df['day_of_week'] = df['timestamp'].dt.day_name()
    
    # Calculate some aggregated metrics
    df['feels_like'] = df['temperature'] - 0.5 * (1 - df['humidity']/100)
    df['weather_severity'] = (
        (df['temperature'] - df['temperature'].mean()) / df['temperature'].std() +
        (df['wind_speed'] - df['wind_speed'].mean()) / df['wind_speed'].std() +
        (df['precipitation'] - df['precipitation'].mean()) / df['precipitation'].std()
    ) / 3
    
    # Export to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'weather_data_for_tableau.csv')
    df.to_csv(output_path, index=False)
    print(f"Data exported to {output_path}")

if __name__ == "__main__":
    export_data_for_tableau()
