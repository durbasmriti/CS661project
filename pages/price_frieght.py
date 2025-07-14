import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/price-frieght", name="Price vs Freight")

# Load data
df = pd.read_csv("data/E-commerse.csv")

# Filter outliers early for dropdown options
df_filtered = df[(df['price'] <= 10000) & (df['freight_value'] <= 1000)]

# Dropdown
category_options = [{'label': cat, 'value': cat} for cat in sorted(df_filtered['product_category_name_english'].dropna().unique())]


layout = html.Div([
    html.H3("Product Price vs Freight Value", className="mb-4 text-center text-primary"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Select Product Category"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=category_options,
                        placeholder="Filter by category (optional)",
                        value=None,
                        clearable=True
                    )
                ])
            ])
        ], width=4)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Price vs Freight Scatter Plot"),
                dbc.CardBody([
                    dcc.Graph(id="price-freight-scatter")
                ])
            ])
        ])
    ])
])


@callback(
    Output("price-freight-scatter", "figure"),
    Input("category-dropdown", "value")
)
def update_scatter(selected_category):
    filtered_df = df_filtered.copy()
    if selected_category:
        filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]

    fig = px.scatter(
        filtered_df,
        x='price',
        y='freight_value',
        title='Relationship Between Product Price and Freight Value',
        labels={'price': 'Product Price (₹)', 'freight_value': 'Freight Cost (₹)'},
        opacity=0.6,
        color_discrete_sequence=['#0074D9']
    )
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(template='plotly_white')

    return fig
