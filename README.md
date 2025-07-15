# E-commerce Sales Dashboard

## Overview
The E-commerce Sales Dashboard is an interactive web application built using Dash and Plotly. It allows users to analyze e-commerce sales data through various visualizations, providing insights into sales performance, profit margins, and trends over time.

## Project Structure

```
ecommerce-sales-dashboard/
├── assets/
│ ├── ecommerce_img.png
│ ├── image.png
│ └── styles.css
│
├── data/
│ ├── E-commerse.csv
│ ├── Rating.csv
│ └── states_india.geojson
│
├── pages/
│ ├── init.py
│ ├── delivery_analysis.py
│ ├── home.py
│ ├── monthlyOrder.py
│ ├── new_vs_repeat.py
│ ├── order_status.py
│ ├── payment.py
│ ├── price_freight.py
│ ├── revenue.py
│ ├── review_score.py
│ ├── sales.py
│ └── top_seller_customers.py
│
├── .gitignore
├── README.md
├── app.py
├── preprocessing_olist.ipynb
└── requirements.txt
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

- You can add more data to the `data/` folder and update `app.py` to use a different dataset if needed.

  Team Members:
A Shri Vaishnavi (230002)
Durbasmriti Saha (230393)
Marka Varshitha (220634)
Mohd Fahad (230656)
P. Sruthi (230751)
Pratiksha (210760)
Priyanka (230798)
Soham Hanmane (220418)
Anany Dev Choudhary (220135)

Prof Soumya Dutta, Dept. of Computer Science and Engineering
