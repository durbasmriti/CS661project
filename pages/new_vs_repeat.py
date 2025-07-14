import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/new-vs-repeat", name="New vs Repeat Customers")

# Load data
df = pd.read_csv("data/E-commerse.csv")

# Convert to datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Extract month
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# Identify customer's first purchase timestamp
df['first_purchase_date'] = df.groupby('customer_unique_id')['order_purchase_timestamp'].transform('min')

# Label each order as new or repeat
df['customer_type'] = df.apply(
    lambda row: 'New' if row['order_purchase_timestamp'] == row['first_purchase_date'] else 'Repeat',
    axis=1
)

# Group for monthly stacked bar
monthly_counts = df.groupby(['order_month', 'customer_type']).size().reset_index(name='count')

# Group for donut chart
donut_data = df['customer_type'].value_counts().reset_index()
donut_data.columns = ['customer_type', 'count']

# Dash layout
layout = html.Div([
    html.H3("New vs Repeat Customers", className="mb-4 text-center text-primary"),

    html.Div([
        dcc.Graph(
            figure=px.bar(
                monthly_counts,
                x='order_month',
                y='count',
                color='customer_type',
                barmode='stack',
                title='Monthly New vs Repeat Customers',
                labels={'order_month': 'Month', 'count': 'Number of Customers'}
            )
        )
    ], className="mb-4"),

    html.Div([
        dcc.Graph(
            figure=px.pie(
                donut_data,
                names='customer_type',
                values='count',
                hole=0.5,
                title='Overall Customer Composition (New vs Repeat)'
            )
        )
    ])
])