import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from datetime import datetime, timedelta

def generate_sample_weather_data():
    """Generate sample weather data for various cities"""
    cities = {
        'New York': (40.7128, -74.0060),
        'London': (51.5074, -0.1278),
        'Tokyo': (35.6762, 139.6503),
        'Sydney': (-33.8688, 151.2093),
        'Mumbai': (19.0760, 72.8777),
        'Cairo': (30.0444, 31.2357),
        'Rio de Janeiro': (-22.9068, -43.1729),
        'Moscow': (55.7558, 37.6173),
        'Beijing': (39.9042, 116.4074),
        'Cape Town': (-33.9249, 18.4241)
    }
    
    # Generate 24 hours of data for each city
    data = []
    base_time = datetime.now()
    
    for city, (lat, lon) in cities.items():
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
                'latitude': lat,
                'longitude': lon,
                'timestamp': time,
                'temperature': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'precipitation': precipitation
            })
    
    return pd.DataFrame(data)

def create_temperature_heatmap(data):
    """Create a temperature heatmap across cities and time"""
    # Convert timestamp to hour
    data['hour'] = data['timestamp'].dt.hour
    
    # Pivot the data for the heatmap
    pivot_data = data.pivot(index='city', columns='hour', values='temperature')
    
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
    plt.savefig('static/temperature_heatmap.png', dpi=300, bbox_inches='tight')
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
    plt.savefig('static/weather_distributions.png', dpi=300, bbox_inches='tight')
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
    plt.savefig('static/correlation_matrix.png', dpi=300, bbox_inches='tight')
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
    plt.savefig('static/time_series.png', dpi=300, bbox_inches='tight')
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
    pair_plot.savefig('static/pair_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_weather_map(data):
    """Create an interactive map with weather information"""
    # Get the latest data for each city
    latest_data = data.groupby('city').last().reset_index()
    
    # Create base map
    m = folium.Map(location=[0, 0], zoom_start=2)
    
    # Add markers for each city
    for _, row in latest_data.iterrows():
        # Create popup content
        popup_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h4>{row['city']}</h4>
            <p>Temperature: {row['temperature']:.1f}°C</p>
            <p>Humidity: {row['humidity']:.1f}%</p>
            <p>Wind Speed: {row['wind_speed']:.1f} m/s</p>
            <p>Precipitation: {row['precipitation']:.1f} mm</p>
        </div>
        """
        
        # Add marker
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            popup=folium.Popup(popup_content, max_width=200),
            color='red' if row['temperature'] > 25 else 'blue',
            fill=True
        ).add_to(m)
    
    # Save map
    m.save('static/weather_map.html')

def main():
    # Set the style for all plots
    sns.set_theme(style="whitegrid")
    
    # Generate sample data
    print("Generating sample weather data...")
    weather_data = generate_sample_weather_data()
    
    # Create visualizations
    print("Creating visualizations...")
    
    print("1. Creating temperature heatmap...")
    create_temperature_heatmap(weather_data)
    
    print("2. Creating weather distribution plots...")
    create_weather_distributions(weather_data)
    
    print("3. Creating correlation matrix...")
    create_correlation_matrix(weather_data)
    
    print("4. Creating time series plots...")
    create_time_series_plot(weather_data)
    
    print("5. Creating pair plot...")
    create_pair_plot(weather_data)
    
    print("6. Creating interactive weather map...")
    create_weather_map(weather_data)
    
    print("\nAll visualizations have been created!")
    print("You can find the following files in the static directory:")
    print("1. temperature_heatmap.png - Temperature variations across cities")
    print("2. weather_distributions.png - Distribution of weather metrics")
    print("3. correlation_matrix.png - Correlations between metrics")
    print("4. time_series.png - Weather changes over time")
    print("5. pair_plot.png - Relationships between metrics")
    print("6. weather_map.html - Interactive weather map")

if __name__ == "__main__":
    main()
