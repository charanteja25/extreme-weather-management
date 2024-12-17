import pandas as pd
import numpy as np
import folium
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import requests
from typing import List, Dict
import json
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.data_processing.weather_processor import WeatherDataProcessor

# WeatherAPI.com configuration
BASE_URL = "http://api.weatherapi.com/v1"

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather data for a location"""
        url = f"{BASE_URL}/current.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "aqi": "no"
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def get_forecast(self, lat: float, lon: float) -> Dict:
        """Get 5-day forecast data for a location"""
        url = f"{BASE_URL}/forecast.json"
        params = {
            "key": self.api_key,
            "q": f"{lat},{lon}",
            "days": 5,
            "aqi": "no"
        }
        response = requests.get(url, params=params)
        return response.json()

def generate_sample_locations():
    """Generate locations around the world"""
    return pd.DataFrame({
        'city': [
            'New York', 'London', 'Tokyo', 'Sydney', 'Mumbai', 
            'Cairo', 'Rio de Janeiro', 'Moscow', 'Beijing', 'Cape Town',
            'Dubai', 'Singapore', 'Paris', 'Toronto', 'Mexico City',
            'Buenos Aires', 'Berlin', 'Istanbul', 'Bangkok', 'Seoul'
        ],
        'lat': [
            40.7128, 51.5074, 35.6762, -33.8688, 19.0760,
            30.0444, -22.9068, 55.7558, 39.9042, -33.9249,
            25.2048, 1.3521, 48.8566, 43.6532, 19.4326,
            -34.6037, 52.5200, 41.0082, 13.7563, 37.5665
        ],
        'lon': [
            -74.0060, -0.1278, 139.6503, 151.2093, 72.8777,
            31.2357, -43.1729, 37.6173, 116.4074, 18.4241,
            55.2708, 103.8198, 2.3522, -79.3832, -99.1332,
            -58.3816, 13.4050, 28.9784, 100.5018, 126.9780
        ]
    })

def fetch_weather_data(locations: pd.DataFrame, api: WeatherAPI) -> pd.DataFrame:
    """Fetch real weather data for all locations"""
    all_data = []
    
    for _, row in locations.iterrows():
        try:
            # Get current weather
            current = api.get_current_weather(row['lat'], row['lon'])
            
            # Extract current weather data
            current_data = {
                'timestamp': datetime.fromtimestamp(current['current']['last_updated_epoch']),
                'city': row['city'],
                'lat': row['lat'],
                'lon': row['lon'],
                'temperature': current['current']['temp_c'],
                'humidity': current['current']['humidity'],
                'wind_speed': current['current']['wind_kph'] / 3.6,  # Convert to m/s
                'precipitation': current['current']['precip_mm'],
                'pressure': current['current']['pressure_mb']
            }
            all_data.append(current_data)
            
            # Get forecast
            forecast = api.get_forecast(row['lat'], row['lon'])
            
            # Process forecast data
            for day in forecast['forecast']['forecastday']:
                for hour in day['hour']:
                    forecast_data = {
                        'timestamp': datetime.fromtimestamp(hour['time_epoch']),
                        'city': row['city'],
                        'lat': row['lat'],
                        'lon': row['lon'],
                        'temperature': hour['temp_c'],
                        'humidity': hour['humidity'],
                        'wind_speed': hour['wind_kph'] / 3.6,  # Convert to m/s
                        'precipitation': hour['precip_mm'],
                        'pressure': hour['pressure_mb']
                    }
                    all_data.append(forecast_data)
                
        except Exception as e:
            print(f"Error fetching data for {row['city']}: {str(e)}")
            continue
    
    return pd.DataFrame(all_data)

def create_weather_map(weather_data: pd.DataFrame):
    """Create an interactive map with weather information"""
    # Create a base map centered on the mean coordinates
    center_lat = weather_data['lat'].mean()
    center_lon = weather_data['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    # Get the latest weather data for each city
    latest_data = weather_data.groupby('city').last().reset_index()
    
    # Add markers for each city
    for _, row in latest_data.iterrows():
        # Create popup content
        popup_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px;">
            <h3>{row['city']}</h3>
            <table style="width: 100%;">
                <tr><td><b>Temperature:</b></td><td>{row['temperature']:.1f}°C</td></tr>
                <tr><td><b>Humidity:</b></td><td>{row['humidity']:.1f}%</td></tr>
                <tr><td><b>Wind Speed:</b></td><td>{row['wind_speed']:.1f} m/s</td></tr>
                <tr><td><b>Precipitation:</b></td><td>{row['precipitation']:.1f} mm</td></tr>
                <tr><td><b>Pressure:</b></td><td>{row['pressure']:.1f} hPa</td></tr>
                <tr><td><b>Weather Score:</b></td><td>{row['weather_score']:.1f}</td></tr>
            </table>
        </div>
        """
        
        # Color marker based on weather score
        color = 'red' if row['weather_score'] > 10 else 'orange' if row['weather_score'] > 5 else 'green'
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=folium.Popup(popup_content, max_width=300),
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)
    
    # Save the map
    m.save('src/static/weather_map.html')

def create_time_series_plots(weather_data: pd.DataFrame):
    """Create time series plots for weather metrics"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            'Temperature Over Time (°C)',
            'Wind Speed Over Time (m/s)',
            'Weather Score Over Time'
        ),
        vertical_spacing=0.1
    )
    
    # Create a color map for cities
    cities = weather_data['city'].unique()
    colors = px.colors.qualitative.Set3[:len(cities)]
    city_colors = dict(zip(cities, colors))
    
    for city in cities:
        city_data = weather_data[weather_data['city'] == city]
        color = city_colors[city]
        
        # Temperature plot
        fig.add_trace(
            go.Scatter(
                x=city_data['timestamp'],
                y=city_data['temperature'],
                name=f'{city} - Temp',
                line=dict(color=color),
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Wind speed plot
        fig.add_trace(
            go.Scatter(
                x=city_data['timestamp'],
                y=city_data['wind_speed'],
                name=f'{city} - Wind',
                line=dict(color=color),
                showlegend=True
            ),
            row=2, col=1
        )
        
        # Weather score plot
        fig.add_trace(
            go.Scatter(
                x=city_data['timestamp'],
                y=city_data['weather_score'],
                name=f'{city} - Score',
                line=dict(color=color),
                showlegend=True
            ),
            row=3, col=1
        )
    
    # Update layout
    fig.update_layout(
        height=1200,
        showlegend=True,
        title_text="Weather Metrics Over Time",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Time", row=3, col=1)
    fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_yaxes(title_text="Wind Speed (m/s)", row=2, col=1)
    fig.update_yaxes(title_text="Weather Score", row=3, col=1)
    
    # Save the plot
    fig.write_html('src/static/weather_trends.html')

def generate_sample_weather_data():
    """Generate sample weather data for various cities"""
    cities = [
        'New York', 'London', 'Tokyo', 'Sydney', 'Mumbai', 
        'Cairo', 'Rio de Janeiro', 'Moscow', 'Beijing', 'Cape Town'
    ]
    
    # Generate 24 hours of data for each city
    data = []
    base_time = datetime.now()
    
    for city in cities:
        # Generate different temperature patterns for different regions
        if city in ['Cairo', 'Mumbai']:
            temp_base = 30
        elif city in ['Moscow', 'London']:
            temp_base = 5
        else:
            temp_base = 20
            
        for hour in range(24):
            time = base_time + timedelta(hours=hour)
            # Add some random variation to make it interesting
            temp = temp_base + np.sin(hour/12 * np.pi) * 5 + np.random.normal(0, 1)
            humidity = 60 + np.random.normal(0, 10)
            wind_speed = 5 + np.random.normal(0, 2)
            precipitation = max(0, np.random.normal(2, 3))
            
            data.append({
                'city': city,
                'timestamp': time,
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'precipitation': precipitation
            })
    
    return pd.DataFrame(data)

def create_temperature_heatmap(data):
    """Create a temperature heatmap across cities and time"""
    # Pivot the data for the heatmap
    pivot_data = data.pivot(index='city', columns=data['timestamp'].dt.hour, values='temperature')
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    sns.heatmap(pivot_data, 
                cmap='RdYlBu_r',
                center=20,
                annot=True,
                fmt='.1f',
                cbar_kws={'label': 'Temperature (°C)'})
    
    plt.title('Temperature Variation Across Cities (24 Hours)')
    plt.xlabel('Hour of Day')
    plt.ylabel('City')
    plt.tight_layout()
    plt.savefig('src/static/temperature_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_weather_distributions(data):
    """Create distribution plots for different weather metrics"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Weather Metrics Distribution by City', fontsize=16)
    
    # Temperature distribution
    sns.boxplot(x='city', y='temperature', data=data, ax=axes[0,0])
    axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=45)
    axes[0,0].set_title('Temperature Distribution')
    
    # Humidity distribution
    sns.violinplot(x='city', y='humidity', data=data, ax=axes[0,1])
    axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=45)
    axes[0,1].set_title('Humidity Distribution')
    
    # Wind speed distribution
    sns.boxplot(x='city', y='wind_speed', data=data, ax=axes[1,0])
    axes[1,0].set_xticklabels(axes[1,0].get_xticklabels(), rotation=45)
    axes[1,0].set_title('Wind Speed Distribution')
    
    # Precipitation distribution
    sns.violinplot(x='city', y='precipitation', data=data, ax=axes[1,1])
    axes[1,1].set_xticklabels(axes[1,1].get_xticklabels(), rotation=45)
    axes[1,1].set_title('Precipitation Distribution')
    
    plt.tight_layout()
    plt.savefig('src/static/weather_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_correlation_matrix(data):
    """Create a correlation matrix heatmap of weather metrics"""
    # Calculate mean values for each city
    city_means = data.groupby('city').agg({
        'temperature': 'mean',
        'humidity': 'mean',
        'wind_speed': 'mean',
        'precipitation': 'mean'
    }).reset_index()
    
    # Create correlation matrix
    corr_matrix = city_means.select_dtypes(include=[np.number]).corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix,
                annot=True,
                cmap='coolwarm',
                center=0,
                square=True,
                fmt='.2f',
                cbar_kws={'label': 'Correlation Coefficient'})
    
    plt.title('Correlation Matrix of Weather Metrics')
    plt.tight_layout()
    plt.savefig('src/static/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_time_series_plot(data):
    """Create time series plots for each weather metric"""
    metrics = ['temperature', 'humidity', 'wind_speed', 'precipitation']
    
    fig, axes = plt.subplots(len(metrics), 1, figsize=(15, 20))
    fig.suptitle('Weather Metrics Over Time', fontsize=16)
    
    for i, metric in enumerate(metrics):
        sns.lineplot(data=data, x='timestamp', y=metric, hue='city', ax=axes[i])
        axes[i].set_title(f'{metric.capitalize()} Variation')
        axes[i].set_xlabel('Time')
        axes[i].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
    plt.tight_layout()
    plt.savefig('src/static/time_series.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_pair_plot(data):
    """Create a pair plot to show relationships between weather metrics"""
    # Calculate hourly means for each city to reduce data points
    hourly_means = data.groupby(['city', data['timestamp'].dt.hour]).agg({
        'temperature': 'mean',
        'humidity': 'mean',
        'wind_speed': 'mean',
        'precipitation': 'mean'
    }).reset_index()
    
    # Create pair plot
    sns.set_style("whitegrid")
    pair_plot = sns.pairplot(hourly_means,
                            hue='city',
                            vars=['temperature', 'humidity', 'wind_speed', 'precipitation'],
                            diag_kind='kde')
    
    pair_plot.fig.suptitle('Relationships Between Weather Metrics', y=1.02)
    plt.tight_layout()
    pair_plot.savefig('src/static/pair_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Check for API key in environment or config file
    config_file = Path(__file__).parent.parent / 'config' / 'config.json'
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            api_key = config.get('weatherapi_key', '')
    else:
        api_key = os.getenv('WEATHERAPI_KEY', '')
    
    if not api_key:
        print("Warning: No WeatherAPI.com API key found. Please set your API key.")
        return
    
    # Initialize API client
    api = WeatherAPI(api_key)
    
    # Generate locations and fetch weather data
    locations = generate_sample_locations()
    weather_data = fetch_weather_data(locations, api)
    
    if weather_data.empty:
        print("Error: No weather data was fetched. Please check your API key and internet connection.")
        return
    
    # Process the weather data
    processor = WeatherDataProcessor()
    processed_data = processor.preprocess_data(weather_data)
    
    # Create visualizations
    create_weather_map(processed_data)
    create_time_series_plots(processed_data)
    
    print("Visualizations have been created in the src/static directory:")
    print("1. weather_map.html - Interactive map with current weather conditions")
    print("2. weather_trends.html - Time series plots of weather metrics")
    
    # Set the style for all plots
    sns.set_theme(style="whitegrid")
    plt.style.use('seaborn')
    
    # Generate sample data
    print("Generating sample weather data...")
    sample_weather_data = generate_sample_weather_data()
    
    # Create visualizations
    print("Creating visualizations...")
    
    print("1. Creating temperature heatmap...")
    create_temperature_heatmap(sample_weather_data)
    
    print("2. Creating weather distribution plots...")
    create_weather_distributions(sample_weather_data)
    
    print("3. Creating correlation matrix...")
    create_correlation_matrix(sample_weather_data)
    
    print("4. Creating time series plots...")
    create_time_series_plot(sample_weather_data)
    
    print("5. Creating pair plot...")
    create_pair_plot(sample_weather_data)
    
    print("\nVisualizations have been created in the src/static directory:")
    print("1. temperature_heatmap.png - Shows temperature variation across cities over 24 hours")
    print("2. weather_distributions.png - Shows distributions of weather metrics for each city")
    print("3. correlation_matrix.png - Shows correlations between different weather metrics")
    print("4. time_series.png - Shows how weather metrics change over time")
    print("5. pair_plot.png - Shows relationships between different weather metrics")

if __name__ == "__main__":
    main()
