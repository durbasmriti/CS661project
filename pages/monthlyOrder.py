# # monthly Orders by statesfor its cities
# # monthly orders product category wise
# # monthly Orders all states
# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc
# import requests

# dash.register_page(__name__, path="/monthly-order")
# df = pd.read_csv("data/E-commerse.csv")


# df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
# df["year_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

# # Dropdown
# states = sorted(df["customer_state"].dropna().unique())
# categories = df["product_category_name_english"].dropna().unique()

# layout = html.Div([
#     html.H3("Monthly Order Trends", className="mb-4 text-center text-primary"),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader("Monthly Orders for Top Product Categories"),
#                 dbc.CardBody(dcc.Graph(id="monthly-category-trend"))
#             ])
#         ])
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader("Monthly Orders per State"),
#                 dbc.CardBody(dcc.Graph(id="monthly-state-trend"))
#             ])
#         ])
#     ])
# ])

# @callback(
#     Output("monthly-category-trend", "figure"),
#     Input("monthly-category-trend", "id")
# )
# def plot_category_trends(_):
#     # Top 6 product categories
#     top_categories = df["product_category_name_english"].value_counts().nlargest(6).index
#     filtered = df[df["product_category_name_english"].isin(top_categories)]
#     grouped = (
#         filtered.groupby(["year_month", "product_category_name_english"])["order_id"]
#         .nunique()
#         .reset_index(name="order_count")
#     )
#     custom_palette = ['#e41a1c', "#277abe", '#4daf4a', "#cf0dec",
#                   '#ff7f00', '#ffff33', "#89451e", '#f781bf', "#7E7C7C"]

#     fig = px.line(
#         grouped,
#         x="year_month",
#         y="order_count",
#         color="product_category_name_english",
#         title="Monthly Order Trends of Top 6 Product Categories",
#         markers=True,
#         template="plotly_white",
#         color_discrete_sequence=custom_palette
#     )
#     fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
#     return fig

# @callback(
#     Output("monthly-state-trend", "figure"),
#     Input("monthly-state-trend", "id")
# )
# def plot_state_trends(_):
#     state_monthly = (
#         df.groupby(["year_month", "customer_state"])["order_id"]
#         .nunique()
#         .reset_index(name="order_count")
#     )
#     custom_palette2 = ["#e6194b", "#3cb44b","#ffe119","#0082c8", "#f58231", "#911eb4","#46f0f0","#f032e6",
#                        "#d2f53c","#fabebe","#008080",  "#e6beff", "#aa6e28","#fffac8","#800000", "#aaffc3","#808000",
#                         "#ffd8b1", "#000080", "#808080",  "#FFFFFF",  "#000000",  "#bcf60c" ]
#     fig = px.line(
#         state_monthly,
#         x="year_month",
#         y="order_count",
#         color="customer_state",
#         title="Monthly Orders Across All States",
#         markers=True,
#         template="plotly_white",
#         color_discrete_sequence=custom_palette2
#     )
#     fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
#     return fig

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path="/monthly-order")


df = pd.read_csv("data/E-commerse.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["year_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)


states = sorted(df["customer_state"].dropna().unique())
categories = df["product_category_name_english"].dropna().unique()

# Layout
layout = html.Div([
    html.H3("Monthly Order Trends", className="mb-4 text-center text-primary"),

    # Top 6 product categories monthly trend
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Orders for Top Product Categories"),
                dbc.CardBody(dcc.Graph(id="monthly-category-trend"))
            ])
        ])
    ], className="mb-4"),

    #monthly order trend for selected state
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Orders per State"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id="state-dropdown",
                        options=[{"label": state, "value": state} for state in states],
                        value=states[0],
                        clearable=False,
                        className="mb-3"
                    ),
                    dcc.Graph(id="monthly-state-trend")
                ])
            ])
        ])
    ])
])

# Callback for top 6 product categories
@callback(
    Output("monthly-category-trend", "figure"),
    Input("monthly-category-trend", "id")
)
def plot_category_trends(_):
    # Top 6 product categories
    top_categories = df["product_category_name_english"].value_counts().nlargest(6).index
    filtered = df[df["product_category_name_english"].isin(top_categories)]
    grouped = (
        filtered.groupby(["year_month", "product_category_name_english"])["order_id"]
        .nunique()
        .reset_index(name="order_count")
    )

    custom_palette = [
        '#e41a1c', "#277abe", '#4daf4a', "#cf0dec",
        '#ff7f00', '#ffff33', "#89451e", '#f781bf', "#7E7C7C"
    ]

    fig = px.line(
        grouped,
        x="year_month",
        y="order_count",
        color="product_category_name_english",
        title="Monthly Order Trends of Top 6 Product Categories",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=custom_palette
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
    return fig

# Callback for state-wise monthly trend
@callback(
    Output("monthly-state-trend", "figure"),
    Input("state-dropdown", "value")
)
def plot_state_trends(selected_state):
    filtered_df = df[df["customer_state"] == selected_state]
    state_monthly = (
        filtered_df.groupby("year_month")["order_id"]
        .nunique()
        .reset_index(name="order_count")
    )

    fig = px.line(
        state_monthly,
        x="year_month",
        y="order_count",
        title=f"Monthly Orders in {selected_state}",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#0082c8"]
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
    return fig
