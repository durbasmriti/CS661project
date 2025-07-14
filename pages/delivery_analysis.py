import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

# Register page
dash.register_page(__name__, path="/delivery-analysis", name="Delivery Analysis")

# Load data
df = pd.read_csv("data/E-commerse.csv")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'], errors='coerce')
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'], errors='coerce')

# Derived columns
df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
df['is_late'] = df['order_delivered_customer_date'] > df['order_estimated_delivery_date']

# Dropdown values
categories = df['product_category_name_english'].dropna().unique()

# Load Indian GeoJSON for choropleth
with open("data/states_india.geojson", "r") as f:
    india_geojson = json.load(f)
for feature in india_geojson["features"]:
    feature["id"] = feature["properties"]["st_nm"].title()

# Layout
layout = html.Div([
    html.H2("Delivery Analysis", className="text-center text-primary mb-4"),

    dbc.Row([
        dbc.Col([
            html.Label("Filter by Product Category"),
            dcc.Dropdown(
                id='category-filter',
                options=[{"label": cat, "value": cat} for cat in sorted(categories)],
                value=None,
                placeholder="Select a category (optional)",
                style={"marginBottom": "20px"}
            ),
        ], width=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="delivery-tabs", value='avg-time', children=[
                dcc.Tab(label="Avg Delivery Time by Category", value='avg-time'),
                dcc.Tab(label="Delivery Time Distribution", value='histogram'),
                dcc.Tab(label="Late Deliveries by State", value='late-state'),
                dcc.Tab(label="Delivery Time vs Shipping Cost", value='box'),
                dcc.Tab(label="Freight Cost vs Delivery Time", value='scatter'),
                dcc.Tab(label="Delivery Time by State (Map)", value='map'),
            ])
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Analysis Result"),
            dbc.CardBody(id='tab-content')
        ]), width=12)
    ])
])

# Callback
@dash.callback(
    Output('tab-content', 'children'),
    Input('delivery-tabs', 'value'),
    Input('category-filter', 'value')
)
def update_tab(tab, selected_category):
    filtered = df.copy()
    if selected_category:
        filtered = filtered[filtered['product_category_name_english'] == selected_category]

    if tab == 'avg-time':
        data = filtered.groupby('product_category_name_english')['delivery_days'] \
            .mean().dropna().sort_values(ascending=False).reset_index()
        fig = px.bar(data, x='product_category_name_english', y='delivery_days',
                     labels={'delivery_days': 'Avg Delivery Days'},
                     title="Average Delivery Time by Product Category",
                     template="plotly_white")
        fig.update_layout(xaxis_tickangle=-45, height=600)

    elif tab == 'histogram':
        fig = px.histogram(filtered, x='delivery_days', nbins=20,
                           title="Delivery Time Distribution",
                           labels={'delivery_days': 'Delivery Days'},
                           template="plotly_white")
        fig.update_layout(height=500)

    elif tab == 'late-state':
        late_state = filtered.groupby('customer_state')['is_late'] \
            .mean().reset_index().sort_values(by='is_late', ascending=False)
        fig = px.bar(late_state, x='customer_state', y='is_late',
                     labels={'is_late': '% Late Deliveries'},
                     title="Percentage of Late Deliveries by State",
                     template="plotly_white")
        fig.update_layout(height=500)

    elif tab == 'box':
        filtered['freight_bin'] = pd.qcut(filtered['freight_value'], 4,
                                          labels=["Low", "Medium", "High", "Very High"])
        fig = px.box(filtered, x='freight_bin', y='delivery_days',
                     title="Delivery Days by Shipping Cost Quartile",
                     labels={'freight_bin': 'Freight Cost Bucket'},
                     template="plotly_white")
        fig.update_layout(height=500)

    elif tab == 'scatter':
        fig = px.scatter(filtered, x='freight_value', y='delivery_days',
                         title="Freight Cost vs Delivery Days",
                         labels={'freight_value': 'Freight ($)', 'delivery_days': 'Delivery Time'},
                         template="plotly_white")
        fig.update_layout(height=500)

    elif tab == 'map':
        avg_state = filtered.groupby('customer_state')['delivery_days'].mean().reset_index()
        avg_state["customer_state"] = avg_state["customer_state"].str.title()
        fig = px.choropleth(
            avg_state,
            geojson=india_geojson,
            locations="customer_state",
            featureidkey="properties.st_nm",
            color="delivery_days",
            color_continuous_scale="YlOrRd",
            title="Average Delivery Time by State",
            labels={"delivery_days": "Avg Delivery Days"},
            template="plotly_white"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=600)

    else:
        return html.Div("No plot selected")

    return dcc.Graph(figure=fig)
