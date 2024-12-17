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
