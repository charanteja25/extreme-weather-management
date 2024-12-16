import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class WeatherVisualizer:
    def __init__(self):
        self.color_scheme = {
            'temperature': 'red',
            'humidity': 'blue',
            'wind_speed': 'green',
            'precipitation': 'purple',
            'pressure': 'orange'
        }

    def create_time_series_plot(self, df: pd.DataFrame, variables: list = None):
        """
        Create an interactive time series plot for weather variables
        
        Args:
            df: DataFrame with weather data
            variables: List of variables to plot
        
        Returns:
            Plotly figure object
        """
        if variables is None:
            variables = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'pressure']
        
        fig = make_subplots(rows=len(variables), cols=1,
                           subplot_titles=variables,
                           shared_xaxes=True)
        
        for idx, var in enumerate(variables, 1):
            fig.add_trace(
                go.Scatter(x=df['timestamp'], y=df[var],
                          name=var,
                          line=dict(color=self.color_scheme.get(var, 'gray'))),
                row=idx, col=1
            )
        
        fig.update_layout(height=200*len(variables),
                         title_text="Weather Variables Time Series",
                         showlegend=False)
        
        return fig

    def create_risk_heatmap(self, df: pd.DataFrame):
        """
        Create a heatmap showing risk levels across different weather conditions
        
        Args:
            df: DataFrame with weather data and risk levels
            
        Returns:
            Plotly figure object
        """
        pivot_table = pd.pivot_table(
            df,
            values='risk_level',
            index=pd.qcut(df['temperature'], q=10),
            columns=pd.qcut(df['wind_speed'], q=10),
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns.astype(str),
            y=pivot_table.index.astype(str),
            colorscale='RdYlBu_r'
        ))
        
        fig.update_layout(
            title='Risk Level Heatmap: Temperature vs Wind Speed',
            xaxis_title='Wind Speed Ranges',
            yaxis_title='Temperature Ranges'
        )
        
        return fig

    def create_risk_dashboard(self, df: pd.DataFrame):
        """
        Create a comprehensive dashboard with multiple visualizations
        
        Args:
            df: DataFrame with weather data
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperature vs Humidity',
                          'Wind Speed Distribution',
                          'Precipitation Over Time',
                          'Risk Level Distribution'),
            specs=[[{'type': 'scatter'}, {'type': 'histogram'}],
                  [{'type': 'scatter'}, {'type': 'pie'}]]
        )
        
        # Temperature vs Humidity scatter plot
        fig.add_trace(
            go.Scatter(x=df['temperature'], y=df['humidity'],
                      mode='markers',
                      marker=dict(color=df['risk_level'],
                                colorscale='RdYlBu_r'),
                      name='Temp vs Humidity'),
            row=1, col=1
        )
        
        # Wind Speed distribution
        fig.add_trace(
            go.Histogram(x=df['wind_speed'],
                        name='Wind Speed Dist'),
            row=1, col=2
        )
        
        # Precipitation over time
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['precipitation'],
                      name='Precipitation'),
            row=2, col=1
        )
        
        # Risk level distribution
        risk_dist = df['risk_level'].value_counts()
        fig.add_trace(
            go.Pie(labels=risk_dist.index,
                   values=risk_dist.values,
                   name='Risk Distribution'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Weather Risk Dashboard")
        return fig

    def plot_model_performance(self, history):
        """
        Plot model training history
        
        Args:
            history: Keras history object
            
        Returns:
            Plotly figure object
        """
        fig = make_subplots(rows=1, cols=2,
                           subplot_titles=('Model Loss', 'Model Accuracy'))
        
        # Loss plot
        fig.add_trace(
            go.Scatter(y=history.history['loss'],
                      name='Training Loss'),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(y=history.history['val_loss'],
                      name='Validation Loss'),
            row=1, col=1
        )
        
        # Accuracy plot
        fig.add_trace(
            go.Scatter(y=history.history['accuracy'],
                      name='Training Accuracy'),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(y=history.history['val_accuracy'],
                      name='Validation Accuracy'),
            row=1, col=2
        )
        
        fig.update_layout(height=400, title_text="Model Training Performance")
        return fig
