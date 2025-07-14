# E-commerce Sales Dashboard

## Overview
The E-commerce Sales Dashboard is an interactive web application built using Dash and Plotly. It allows users to analyze e-commerce sales data through various visualizations, providing insights into sales performance, profit margins, and trends over time.

## Project Structure

```
ecommerce-sales-dashboard/
├── assets/
│   └── styles.css            # CSS styles for the dashboard
├── data/
│   └── Sample - Superstore.csv  # Dataset used for analysis
├── app.py                    # Main Dash application file
├── README.md                 # Project documentation
└── requirements.txt          # List of required Python packages
|__ preprocessing_olist.ipynb
```

## Setup Instructions

1. **Clone the Repository**:  
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:
   ```
   cd ecommerce-sales-dashboard
   ```

3. **Install Dependencies**:  
   Ensure you have Python installed, then install the required packages using:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**:  
   Start the Dash application by running:
   ```
   python app.py
   ```
   Open your web browser and go to [http://127.0.0.1:8050](http://127.0.0.1:8050) to view the dashboard.

## Usage Guidelines

- Use the navigation sidebar to explore different sales and profit visualizations.
- Each page provides contextual filters (such as region, category, year, or segment) to help you analyze the data.
- The dashboard updates the visualizations based on your selections.

## Customization

- Modify `assets/styles.css` to change the appearance of the dashboard, including colors, fonts, and layout.
- You can add more data to the `data/` folder and update `app.py` to use a different dataset if needed.
