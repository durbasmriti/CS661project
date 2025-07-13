
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__, path="/price-frieght", name="Price & Freight Analysis")

# Use the full dataset for analysis
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'Final_olist_dataset.csv')

# Columns needed
cols = [
    'price',
    'freight_value',
    'product_category_name_english',
    'customer_state'
]

# Read a sample for performance (adjust nrows as needed)
df = pd.read_csv(DATA_PATH, usecols=cols, nrows=10000)

# 1. Scatter Plot: Mean Product Price vs. Mean Freight Value by Product Category
import plotly.colors as pc

mean_df = df.groupby('product_category_name_english', as_index=False).agg({
    'price': 'mean',
    'freight_value': 'mean'
})

# Assign a color to each product category (optional: group similar as before)
base_colors = pc.qualitative.Plotly
categories = mean_df['product_category_name_english'].unique()
category_color_map = {cat: base_colors[i % len(base_colors)] for i, cat in enumerate(sorted(categories))}

fig_scatter = px.scatter(
    mean_df, x='price', y='freight_value',
    title='Mean Product Price vs. Mean Freight Value by Product Category',
    labels={'price': 'Mean Product Price', 'freight_value': 'Mean Freight Value'},
    color='product_category_name_english',
    color_discrete_map=category_color_map,
    hover_name='product_category_name_english',
    size_max=15
)
fig_scatter.update_traces(marker=dict(size=14, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(plot_bgcolor='#f7f7fa', paper_bgcolor='#f7f7fa')

# 2. Box Plot: Freight Value by Product Category
fig_box = px.box(
    df, x='product_category_name_english', y='freight_value',
    title='Freight Value Distribution by Product Category',
    labels={'product_category_name_english': 'Product Category', 'freight_value': 'Freight Value'},
    points='outliers'
)
fig_box.update_layout(plot_bgcolor='#f7f7fa', paper_bgcolor='#f7f7fa', xaxis_tickangle=45)

# 3. Bar Chart: Average Freight Value by State
state_avg = df.groupby('customer_state', as_index=False)['freight_value'].mean()
fig_bar = px.bar(
    state_avg, x='customer_state', y='freight_value',
    title='Average Freight Value by State',
    labels={'customer_state': 'Customer State', 'freight_value': 'Average Freight Value'},
    color='freight_value',
    color_continuous_scale=px.colors.sequential.Blues
)
fig_bar.update_layout(plot_bgcolor='#f7f7fa', paper_bgcolor='#f7f7fa')

def layout():
    return html.Div([
        html.H2("Price & Freight Analysis", className="mb-4"),
        html.H4("Price vs. Freight Value"),
        dcc.Graph(figure=fig_scatter),
        html.Hr(),
        html.H4("Freight Value Distribution by Product Category"),
        dcc.Graph(figure=fig_box),
        html.Hr(),
        html.H4("Average Freight Value by State"),
        dcc.Graph(figure=fig_bar)
    ])
