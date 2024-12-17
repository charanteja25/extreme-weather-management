# Extreme Weather Management System

## 🌪️ Project Overview
A deep learning-based system for real-time weather risk assessment and prediction. This project uses Azure AI services and Power BI for visualizing weather patterns and predicting potential risks.

## 🎯 Key Features
- Real-time weather data processing
- Risk assessment using deep learning models
- Interactive Power BI dashboards
- Automated alert system
- Historical weather pattern analysis

## 🏗️ Project Structure
```
extreme-weather-management/
├── data/                      # Data files and preprocessing scripts
├── models/                    # Trained models and model architectures
├── notebooks/                 # Jupyter notebooks for analysis
├── src/                      # Source code
│   ├── data_processing/      # Data processing utilities
│   ├── model/                # Model implementation
│   ├── visualization/        # Visualization tools
│   └── api/                  # API endpoints
├── tests/                    # Unit tests
└── docs/                     # Documentation
```

## 🛠️ Technology Stack
- Python 3.8+
- TensorFlow 2.x
- Azure AI Services
- Power BI
- FastAPI
- Pandas
- NumPy
- Scikit-learn

## 📊 Features
1. **Weather Data Processing**
   - Real-time data collection from multiple sources
   - Data cleaning and preprocessing
   - Feature engineering

2. **Risk Assessment**
   - Deep learning model for risk prediction
   - Confidence scoring
   - Historical pattern matching

3. **Visualization**
   - Interactive dashboards
   - Real-time monitoring
   - Risk heat maps

4. **Alert System**
   - Automated risk notifications
   - Severity classification
   - Action recommendations

## 🚀 Getting Started

### Prerequisites
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application
```bash
python src/main.py
```

### Running Tests
```bash
pytest tests/
```

## 📈 Model Performance
- Accuracy: 92% on test set
- F1 Score: 0.89
- Precision: 0.91
- Recall: 0.87

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact
- **Author**: Venkata Charan Teja Gunisetty
- **Email**: charanteja.teja25@gmail.com
- **LinkedIn**: [Charan Teja Gunisetty](https://www.linkedin.com/in/charantejagunisetty/)

## Streamlit Dashboard 🎯

### About Streamlit
Streamlit is an open-source Python library that makes it easy to create beautiful, interactive web applications for data science and machine learning. Our dashboard leverages Streamlit's capabilities to provide:

- **Real-time Interactivity**: Dynamic filtering and updates without page reloads
- **Rich Data Visualizations**: Integration with Plotly for advanced charts
- **Responsive Layout**: Automatic mobile-friendly design
- **Easy Deployment**: Simple deployment to cloud platforms

### Dashboard Architecture

The dashboard is built using:
- **Streamlit**: For the web interface and interactivity
- **Plotly**: For interactive data visualizations
- **Folium**: For geographic mapping
- **Pandas**: For data manipulation and analysis

### Key Features

1. **Interactive Data Filters**
   - Date range selection
   - City-based filtering
   - Real-time updates

2. **Visualization Types**
   - Temperature Heatmaps
   - Weather Distribution Plots
   - Correlation Analysis
   - Time Series Trends
   - Geographic Distribution
   - Scatter Matrix Analysis

3. **Analysis Tabs**
   - Overview: Quick insights and summaries
   - Detailed Analysis: In-depth metrics and correlations
   - Geographic View: Location-based weather patterns

### Installation and Setup

1. **Prerequisites**
   ```bash
   # Ensure you have Python 3.8+ installed
   python --version
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard**
   ```bash
   cd extreme-weather-management
   streamlit run src/streamlit_app.py
   ```

### Usage Guide

1. **Starting the Dashboard**
   - Execute the run command above
   - Dashboard will open in your default browser
   - Default address: http://localhost:8501

2. **Navigation**
   - Use the sidebar for filtering options
   - Switch between tabs for different analyses
   - Interact with charts:
     * Hover for detailed information
     * Click and drag to zoom
     * Double-click to reset view
     * Download data or images

3. **Data Filtering**
   - Select date range from the calendar
   - Choose specific cities
   - All visualizations update automatically

4. **Customization**
   - Dark/Light mode toggle
   - Full-screen view for charts
   - Download options for visualizations

### Performance Tips

- **Data Loading**: Initial load may take a few seconds
- **Filtering**: Apply city filters first for faster performance
- **Memory Usage**: Clear browser cache if performance degrades
- **Best Practice**: Limit date range for smoother experience

### Troubleshooting

Common issues and solutions:
1. **Dashboard Not Loading**
   - Check if all dependencies are installed
   - Verify Python version compatibility
   - Clear browser cache

2. **Slow Performance**
   - Reduce date range selection
   - Filter specific cities
   - Close unused browser tabs

3. **Visualization Issues**
   - Refresh the page
   - Update your browser
   - Check console for errors

### Future Enhancements

Planned features:
- Advanced analytics capabilities
- Custom metric calculations
- Export functionality
- API integration
- User authentication
- Custom themes

## Interactive Weather Dashboard

The project now includes an interactive weather analytics dashboard built with Streamlit and Plotly. The dashboard provides:

- Real-time weather data visualization
- Interactive filtering by date and city
- Multiple visualization types:
  - Temperature heatmaps
  - Weather metric distributions
  - Correlation analysis
  - Time series analysis
  - Geographic distribution

### Running the Dashboard

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Streamlit server:
   ```bash
   cd extreme-weather-management
   streamlit run src/streamlit_app.py
   ```

3. Open your browser and navigate to http://localhost:8501

### Dashboard Features

- **Overview Tab**: View temperature variations and weather metric distributions
- **Detailed Analysis Tab**: Explore correlations and time series patterns
- **Geographic View Tab**: Interactive map showing weather conditions by location

### Filtering and Interaction

- Use the sidebar to select date ranges and cities
- Interact with visualizations:
  - Hover over data points for detailed information
  - Click and drag to zoom
  - Double-click to reset view
  - Download options for each chart
