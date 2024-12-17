# Weather Analytics Visualizations

This directory contains various visualization tools and dashboards for the Extreme Weather Management project.

## Available Visualizations

### 1. Streamlit Dashboard
Interactive web-based dashboard with real-time data visualization.

- **Location**: `/streamlit`
- **Features**:
  - Temperature heatmaps
  - Weather distributions
  - Correlation analysis
  - Geographic mapping
  - Time series analysis

### 2. Tableau Public Dashboard
Static dashboard with rich interactive features.

- **Location**: `/tableau`
- **Features**:
  - Geographic heat maps
  - Temperature trends
  - Weather patterns
  - Custom calculations
  - Story points

## Directory Structure

```
visualizations/
├── streamlit/
│   ├── streamlit_app.py
│   └── requirements.txt
├── tableau/
│   ├── data_export.py
│   └── weather_data.csv
└── README.md
```

## Setup Instructions

### Streamlit Dashboard
1. Navigate to the streamlit directory:
   ```bash
   cd streamlit
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```

### Tableau Dashboard
1. Navigate to the tableau directory:
   ```bash
   cd tableau
   ```
2. Generate data for Tableau:
   ```bash
   python data_export.py
   ```
3. Open `weather_data.csv` in Tableau Public

## Usage Guide

### Streamlit Dashboard
- Access at: http://localhost:8501
- Use sidebar filters for data selection
- Interactive charts with hover details
- Download options for visualizations

### Tableau Public Dashboard
- Access at: [Tableau Public Link]
- Use built-in filters
- Download views as images
- Share specific views via links

## Development

To add new visualizations:
1. Create a new directory for your visualization tool
2. Add a README.md with setup instructions
3. Include requirements.txt if needed
4. Add source code and documentation
5. Update this main README

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your visualization
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
