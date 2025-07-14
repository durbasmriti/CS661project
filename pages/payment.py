
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/payment-method")

df = pd.read_csv("data/E-commerse.csv")


df["product_category_name_english"] = df["product_category_name_english"].fillna("Unknown")


category_payment = df.groupby(["product_category_name_english", "payment_type"]).size().reset_index(name="count")
payment_type_counts = df["payment_type"].value_counts().reset_index()
payment_type_counts.columns = ["payment_type", "count"]


layout = html.Div([
    html.H4("Payment Type Distribution per Product Category", className="mb-4 text-primary"),

    dcc.Graph(id="stacked-payment-bar"),

    html.Hr(),

    html.H5("Overall Payment Type Usage", className="mb-3 text-success"),
    dcc.Graph(id="payment-type-pie")
])


@callback(
    Output("stacked-payment-bar", "figure"),
    Output("payment-type-pie", "figure"),
    Input("stacked-payment-bar", "id")  # dummy input to trigger once on load
)
def update_charts(_):
    # bar chart
    bar_fig = px.bar(
        category_payment,
        x="product_category_name_english",
        y="count",
        color="payment_type",
        title="Stacked Bar Chart: Payment Types by Product Category",
        labels={"count": "Number of Orders", "product_category_name_english": "Product Category"},
        barmode="stack"
    )
    bar_fig.update_layout(
        xaxis_tickangle=45,
        template="plotly_white",
        legend_title_text="Payment Type",
        margin=dict(l=20, r=20, t=60, b=120)
    )

    # Pie chart
    pie_fig = px.pie(
        payment_type_counts,
        values="count",
        names="payment_type",
        title="Overall Payment Type Usage (Percentage)",
        hole=0.3
    )
    pie_fig.update_traces(textinfo='percent+label')
    pie_fig.update_layout(template="plotly_white")

    return bar_fig, pie_fig
