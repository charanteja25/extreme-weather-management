import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from datetime import datetime, timedelta
from streamlit_folium import folium_static
from visualization.weather_visualization import generate_sample_weather_data

# Set page config
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for PowerBI-like styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: white;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0078D4;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Generate data
data = generate_sample_weather_data()
df = pd.DataFrame(data)

# Convert timestamps to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
min_date = df['timestamp'].min().to_pydatetime()
max_date = df['timestamp'].max().to_pydatetime()

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-BI.svg", width=50)
    st.title("Weather Analytics")
    
    # Date filter
    st.subheader("📅 Time Range")
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Convert dates to datetime for filtering
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = datetime.combine(date_range[1], datetime.max.time())
    
    # City filter
    st.subheader("🌍 Cities")
    selected_cities = st.multiselect(
        "Select Cities",
        options=df['city'].unique(),
        default=df['city'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['timestamp'].dt.date.between(date_range[0], date_range[1])) &
        (df['city'].isin(selected_cities))
    ]

# Main dashboard
st.title("🌤️ Weather Analytics Dashboard")

# Key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    avg_temp = filtered_df['temperature'].mean()
    st.metric("Average Temperature", f"{avg_temp:.1f}°C")
with col2:
    avg_humidity = filtered_df['humidity'].mean()
    st.metric("Average Humidity", f"{avg_humidity:.1f}%")
with col3:
    avg_wind = filtered_df['wind_speed'].mean()
    st.metric("Average Wind Speed", f"{avg_wind:.1f} m/s")
with col4:
    total_precip = filtered_df['precipitation'].sum()
    st.metric("Total Precipitation", f"{total_precip:.1f} mm")

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "Geographic View"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature heatmap
        st.subheader("Temperature Variation")
        # Group by city and hour for better visualization
        filtered_df['hour'] = filtered_df['timestamp'].dt.hour
        temp_pivot = filtered_df.groupby(['city', 'hour'])['temperature'].mean().reset_index()
        temp_pivot = temp_pivot.pivot(index='city', columns='hour', values='temperature')
        
        fig_heatmap = px.imshow(
            temp_pivot,
            color_continuous_scale='RdYlBu_r',
            title='Temperature Heatmap by Hour',
            labels={'color': 'Temperature (°C)'},
            x=temp_pivot.columns.astype(str) + ':00',  # Add hour format
            y=temp_pivot.index
        )
        fig_heatmap.update_layout(
            height=400,
            xaxis_title="Hour of Day",
            yaxis_title="City"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        # Weather metrics distribution
        st.subheader("Weather Metrics Distribution")
        fig_dist = px.box(
            filtered_df,
            x='city',
            y=['temperature', 'humidity', 'wind_speed', 'precipitation'],
            facet_col='variable',
            facet_col_wrap=2,
            title='Distribution of Weather Metrics by City'
        )
        fig_dist.update_layout(height=400)
        st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation matrix
        st.subheader("Correlation Analysis")
        corr_matrix = filtered_df[['temperature', 'humidity', 'wind_speed', 'precipitation']].corr()
        fig_corr = px.imshow(
            corr_matrix,
            color_continuous_scale='RdBu',
            title='Correlation Matrix',
            text=corr_matrix.round(2)
        )
        fig_corr.update_layout(height=400)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Time series
        st.subheader("Time Series Analysis")
        fig_time = px.line(
            filtered_df,
            x='timestamp',
            y='temperature',
            color='city',
            title='Temperature Over Time'
        )
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Scatter matrix
    st.subheader("Relationship Analysis")
    fig_scatter = px.scatter_matrix(
        filtered_df,
        dimensions=['temperature', 'humidity', 'wind_speed', 'precipitation'],
        color='city',
        title='Weather Metrics Relationships'
    )
    fig_scatter.update_layout(height=800)
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    # Interactive map
    st.subheader("Geographic Weather Distribution")
    latest_data = filtered_df.sort_values('timestamp').groupby('city').last().reset_index()
    
    # Create map
    center_lat = latest_data['latitude'].mean()
    center_lon = latest_data['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    for _, row in latest_data.iterrows():
        popup_content = f"""
        <div style='font-family: Arial; width: 200px;'>
            <h4 style='margin-bottom: 10px;'>{row['city']}</h4>
            <p><b>Temperature:</b> {row['temperature']:.1f}°C</p>
            <p><b>Humidity:</b> {row['humidity']:.1f}%</p>
            <p><b>Wind Speed:</b> {row['wind_speed']:.1f} m/s</p>
            <p><b>Precipitation:</b> {row['precipitation']:.1f} mm</p>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=10,
            popup=folium.Popup(popup_content, max_width=300),
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)
    
    folium_static(m)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Weather Analytics Dashboard | Built with Streamlit & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)
