# # delivered /canceled

# import dash
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.express as px
# import json


# dash.register_page(__name__, path="/order-status")

# df = pd.read_csv("data/E-commerse.csv")

# # Layout
# layout = html.Div([
#     html.H3("Order Status Analysis", className="text-center text-primary mb-4"),

#     dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Order Status Count"),
#             dbc.CardBody([
#                 dcc.Graph(id="order-status-bar")
#             ])
#         ]), width=6),

#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Cancelled vs Delivered Orders (Choropleth Map)"),
#             dbc.CardBody([
#                 dcc.Graph(id="india-map-cancel-deliver")
#             ])
#         ]), width=6),
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col(dbc.Card([
#             dbc.CardHeader("Monthly Order Status Trend"),
#             dbc.CardBody([
#                 dcc.Graph(id="order-status-monthly")
#             ])
#         ]), width=12),
#     ], className="mb-4"),
# ])

# # ----------- Callbacks -----------

# # 1. Order status count bar chart
# @callback(
#     Output("order-status-bar", "figure"),
#     Input("order-status-bar", "id")
# )
# def update_status_bar(_):
#     status_count = df["order_status"].value_counts().reset_index()
#     status_count.columns = ["status", "count"]
#     fig = px.bar(
#         status_count,
#         x="status",
#         y="count",
#         color="status",
#         title="Distribution of Order Statuses",
#         template="plotly_white",
#         color_discrete_sequence=px.colors.qualitative.Set3
#     )
#     return fig

# # 2. Choropleth map for Delivered vs Canceled
# @callback(
#     Output("india-map-cancel-deliver", "figure"),
#     Input("india-map-cancel-deliver", "id")
# )
# def update_india_map(_):
#     filtered = df[df["order_status"].isin(["delivered", "canceled"])]
#     grouped = filtered.groupby(["customer_state", "order_status"]).size().unstack(fill_value=0).reset_index()
#     grouped["net_score"] = grouped.get("delivered", 0) - grouped.get("canceled", 0)

#     # Load India GeoJSON
#     with open("data/states_india.geojson", "rU") as f:
#         india_geojson = json.load(f)

#     # Assign "id" to each state
#     for feature in india_geojson["features"]:
#         feature["id"] = feature["properties"]["st_nm"].title()

#     fig = px.choropleth(
#         grouped,
#         geojson=india_geojson,
#         locations="customer_state",
#         featureidkey="properties.st_nm",
#         color="net_score",
#         hover_data=["delivered", "canceled"],
#         color_continuous_scale="Tealgrn",
#         title="Net Delivered Orders (Delivered - Canceled)",
#         template="plotly_white"
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     return fig

# # 3. Monthly order trend by status
# @callback(
#     Output("order-status-monthly", "figure"),
#     Input("order-status-monthly", "id")
# )
# def update_status_monthly(_):
#     df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
#     df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
#     monthly = df.groupby(["month", "order_status"]).size().reset_index(name="count")

#     fig = px.line(
#         monthly,
#         x="month",
#         y="count",
#         color="order_status",
#         title="Monthly Order Status Trend",
#         markers=True,
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
#     return fig


import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

# Register page
dash.register_page(__name__, path="/order-status")

# Load the dataset
df = pd.read_csv("data/E-commerse.csv")

# Convert purchase date
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")

# Load India states GeoJSON
with open("data/states_india.geojson", "r") as f:
    india_geojson = json.load(f)

# Assign ID to match with state names in df
for feature in india_geojson["features"]:
    feature["id"] = feature["properties"]["st_nm"].title()

# ========== LAYOUT ==========
layout = html.Div([
    html.H3("Order Status Analysis", className="text-center text-primary mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Order Status Distribution"),
            dbc.CardBody([
                dcc.Graph(id="order-status-bar")
            ])
        ], className="shadow"), width=6),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Net Orders by State (Delivered - Canceled)"),
            dbc.CardBody([
                dcc.Graph(id="india-map-cancel-deliver")
            ])
        ], className="shadow"), width=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Monthly Order Status Trend"),
            dbc.CardBody([
                dcc.Graph(id="order-status-monthly")
            ])
        ], className="shadow"), width=12),
    ], className="mb-4"),
])

# ========== CALLBACKS ==========

# Order Status Bar Chart
@callback(
    Output("order-status-bar", "figure"),
    Input("order-status-bar", "id")
)
def update_status_bar(_):
    status_count = df["order_status"].value_counts().reset_index()
    status_count.columns = ["status", "count"]
    fig = px.bar(
        status_count,
        x="status",
        y="count",
        color="status",
        title="Distribution of Order Statuses",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(xaxis_title="Order Status", yaxis_title="Number of Orders")
    return fig

#  India Choropleth Map (Delivered vs Canceled)
@callback(
    Output("india-map-cancel-deliver", "figure"),
    Input("india-map-cancel-deliver", "id")
)
def update_india_map(_):
    filtered = df[df["order_status"].isin(["delivered", "canceled"])]
    grouped = filtered.groupby(["customer_state", "order_status"]).size().unstack(fill_value=0).reset_index()
    grouped.columns.name = None
    grouped["net_score"] = grouped.get("delivered", 0) - grouped.get("canceled", 0)

    fig = px.choropleth(
        grouped,
        geojson=india_geojson,
        locations="customer_state",
        featureidkey="properties.st_nm",
        color="net_score",
        hover_data=["delivered", "canceled"],
        color_continuous_scale="Viridis",
        title="Net Delivered Orders (Delivered - Canceled)",
        template="plotly_white"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

# 3. Monthly Order Trend Line Plot
@callback(
    Output("order-status-monthly", "figure"),
    Input("order-status-monthly", "id")
)
def update_status_monthly(_):
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly = df.groupby(["month", "order_status"]).size().reset_index(name="count")

    fig = px.line(
        monthly,
        x="month",
        y="count",
        color="order_status",
        title="Monthly Order Status Trend",
        markers=True,
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Orders",
        xaxis_tickangle=45
    )
    return fig
