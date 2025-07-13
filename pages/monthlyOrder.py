
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__, path="/monthly-order", name="Monthly Orders")

# Use the sample file for performance
DATA_PATH_SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'Final_olist_dataset.csv')
sample_size = 5000

# Columns needed
cols = [
    'order_purchase_timestamp',
    'customer_city',
    'product_category_name_english',
    'customer_state'
]

# Read sample
df = pd.read_csv(DATA_PATH_SAMPLE, usecols=cols)
if len(df) > sample_size:
    df = df.sample(n=sample_size, random_state=42)

# Convert to datetime and extract year-month in 'YYYY-Mon' format
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df = df.dropna(subset=['order_purchase_timestamp'])
df['year_month'] = df['order_purchase_timestamp'].dt.strftime('%Y-%b')




# 1. City-wise monthly order histogram with dropdown
city_month = df.groupby(['year_month', 'customer_city']).size().reset_index(name='orders')
# Sort months chronologically
month_strs = city_month['year_month'].unique()
month_dt_map = {m: pd.to_datetime(m, format='%Y-%b') for m in month_strs}
months = [m for m, _ in sorted(month_dt_map.items(), key=lambda x: x[1])]

def create_city_histogram(selected_month):
    filtered = city_month[city_month['year_month'] == selected_month].sort_values('orders', ascending=False)
    fig = px.bar(
        filtered,
        x='customer_city',
        y='orders',
        title=f'City-wise Orders for {selected_month}',
        labels={'customer_city': 'City', 'orders': 'Number of Orders'},
        height=400
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

# Initial month selection
initial_month = months[0] if months else None

# 2. Product category wise monthly order histogram (interactive)
prod_month = df.groupby(['year_month', 'product_category_name_english']).size().reset_index(name='orders')
def create_prod_histogram(selected_month):
    filtered = prod_month[prod_month['year_month'] == selected_month].sort_values('orders', ascending=False)
    fig = px.bar(
        filtered,
        x='product_category_name_english',
        y='orders',
        color='product_category_name_english',
        title=f'Product Category-wise Orders for {selected_month}',
        labels={'product_category_name_english': 'Product Category', 'orders': 'Number of Orders'},
        height=400,
        width=1100
    )
    fig.update_layout(
        plot_bgcolor='#f7f7fa',
        paper_bgcolor='#f7f7fa',
        yaxis=dict(gridcolor='#444', gridwidth=1),
        xaxis=dict(gridcolor='#f7f7fa', gridwidth=1),
        xaxis_tickangle=45
    )
    return fig

# 3. State wise monthly order histogram (interactive)
state_month = df.groupby(['year_month', 'customer_state']).size().reset_index(name='orders')
def create_state_histogram(selected_month):
    filtered = state_month[state_month['year_month'] == selected_month].sort_values('orders', ascending=False)
    fig = px.bar(
        filtered,
        x='customer_state',
        y='orders',
        color='customer_state',
        title=f'State-wise Orders for {selected_month}',
        labels={'customer_state': 'State', 'orders': 'Number of Orders'},
        height=400,
        width=1100
    )
    fig.update_layout(
        plot_bgcolor='#f7f7fa',
        paper_bgcolor='#f7f7fa',
        yaxis=dict(gridcolor='#444', gridwidth=1),
        xaxis=dict(gridcolor='#f7f7fa', gridwidth=1)
    )
    return fig

from dash.dependencies import Input, Output

def layout():
    card_style = {
        'background': '#fff',
        'borderRadius': '16px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'padding': '24px',
        'marginBottom': '32px',
        'border': '1px solid #e3e3e3',
    }
    heading_style = {
        'background': '#f7f7fa',
        'borderRadius': '10px',
        'padding': '10px 18px',
        'marginBottom': '18px',
        'fontWeight': 'bold',
        'color': '#2a3f5f',
        'fontSize': '1.2rem',
        'borderLeft': '5px solid #4e79a7',
        'boxShadow': '0 1px 4px rgba(0,0,0,0.03)'
    }
    return html.Div([
        html.H2("Monthly Orders Analysis", className="mb-4"),
        html.Div([
            html.H4("City-wise Orders by Month", style={'marginBottom': '0.5rem'}),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': m, 'value': m} for m in months],
                value=initial_month,
                clearable=False,
                style={'width': '300px'}
            )
        ], style={
            'position': 'sticky',
            'top': '60px',
            'zIndex': 100,
            'background': '#fff',
            'paddingTop': '10px',
            'paddingBottom': '10px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
        }),
        html.Div([
            html.Div("City-wise Orders", style=heading_style),
            dcc.Graph(id='city-month-graph', figure=create_city_histogram(initial_month)),
        ], style=card_style),
        html.Div([
            html.Div("Product Category-wise Monthly Orders", style=heading_style),
            dcc.Graph(id='prod-month-graph', figure=create_prod_histogram(initial_month)),
        ], style=card_style),
        html.Div([
            html.Div("State-wise Monthly Orders", style=heading_style),
            dcc.Graph(id='state-month-graph', figure=create_state_histogram(initial_month)),
        ], style=card_style),
    ])

# Callbacks for interactive histograms
from dash import callback, ctx
@callback(
    Output('city-month-graph', 'figure'),
    Output('prod-month-graph', 'figure'),
    Output('state-month-graph', 'figure'),
    Input('month-dropdown', 'value')
)
def update_all_histograms(selected_month):
    if selected_month:
        return (
            create_city_histogram(selected_month),
            create_prod_histogram(selected_month),
            create_state_histogram(selected_month)
        )
    return (
        create_city_histogram(initial_month),
        create_prod_histogram(initial_month),
        create_state_histogram(initial_month)
    )