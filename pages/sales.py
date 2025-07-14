import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import json


dash.register_page(__name__, path="/sales")


df = pd.read_csv("data/E-commerse.csv")

state_name_map = {
    "Andaman and Nicobar Islands": "Andaman & Nicobar Island",
    "Arunachal Pradesh": "Arunanchal Pradesh",
    "Chhattisgarh": "Chhattisgarh",
    "Delhi": "NCT of Delhi",
    "Jammu and Kashmir": "Jammu & Kashmir",
    "Orissa": "Odisha",
    "Pondicherry": "Puducherry",
    "Uttaranchal": "Uttarakhand"
}
df["customer_state"] = df["customer_state"].replace(state_name_map)


state_grouped = df.groupby("customer_state")["order_item_id"].count().reset_index(name="total_products")
category_grouped = df.groupby("product_category_name_english")["order_item_id"].count().reset_index(name="total_products")

# Dropdown
dropdown_options = sorted(df["customer_state"].dropna().unique())

# GeoJSON
with open("data/states_india.geojson", "r") as f:
    india_states_geojson = json.load(f)

for feature in india_states_geojson["features"]:
    feature["id"] = feature["properties"]["st_nm"].title()



layout = html.Div([
    html.H3("Product Sales Volume Analysis", className="mb-4 text-center text-primary"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Choropleth Map: Products Ordered by State"),
                dbc.CardBody(dcc.Graph(id="product-sales-map"))
            ], className="shadow-sm"),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Top Product Categories by Sales Volume"),
                dbc.CardBody(dcc.Graph(id="product-sales-bar"))
            ], className="shadow-sm"),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Select a State to See City-Wise Sales"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='state-dropdown',
                        options=[{"label": s, "value": s} for s in dropdown_options],
                        value=dropdown_options[0],
                        clearable=False,
                        style={"width": "300px"}
                    )
                ])
            ], className="shadow-sm"),
            width=12
        )
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Treemap: City-wise Product Sales"),
                dbc.CardBody(dcc.Graph(id="city-sales-treemap"))
            ], className="shadow-sm"),
            width=12
        )
    ])
])

#Callbacks

@callback(
    Output("product-sales-map", "figure"),
    Input("state-dropdown", "value")
)
def update_choropleth(_):
    fig = px.choropleth(
        state_grouped,
        geojson=india_states_geojson,
        locations="customer_state",
        featureidkey="properties.st_nm",
        color="total_products",
        color_continuous_scale="Blues",
        title="Products Ordered by State"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template="plotly_white")
    return fig

@callback(
    Output("product-sales-bar", "figure"),
    Input("state-dropdown", "value")
)
def update_bar_chart(_):
    fig = px.bar(
        category_grouped.sort_values("total_products", ascending=False).head(20),
        x="product_category_name_english",
        y="total_products",
        title="Top 20 Product Categories by Sales Volume",
        labels={"product_category_name_english": "Product Category", "total_products": "Products Sold"},
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig

@callback(
    Output("city-sales-treemap", "figure"),
    Input("state-dropdown", "value")
)
def update_city_treemap(selected_state):
    filtered = df[df["customer_state"] == selected_state]
    city_grouped = filtered.groupby(["customer_city", "product_category_name_english"])["order_item_id"].count().reset_index(name="total_products")
    fig = px.treemap(
        city_grouped,
        path=["customer_city", "product_category_name_english"],
        values="total_products",
        title=f"City-wise Product Category Sales in {selected_state}",
        template="plotly_white"
    )
    return fig
