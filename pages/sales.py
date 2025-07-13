# sales with state, product category, city (with dropdown)
# monthly trends
# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback

# dash.register_page(__name__, path="/sales")

# # Load the dataset
# df = pd.read_csv("data/final_olist_dataset.csv", parse_dates=['order_purchase_timestamp'])

# # Clean and prepare
# df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# # Dropdown options
# dimension_options = {
#     'customer_state': 'State',
#     'customer_city': 'City',
#     'product_category_name_english': 'Product Category'
# }

# layout = html.Div([
#     html.H3("Sales Analysis", className="mb-4", style={"textAlign": "center", "color": "#2c3e50"}),

#     html.Div([
#         html.Label("Select Dimension:", className="mb-2"),
#         dcc.Dropdown(
#             id='sales-dimension-dropdown',
#             options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#             value='customer_state',
#             clearable=False,
#             style={"width": "300px"}
#         )
#     ], style={"marginBottom": "30px"}),

#     dcc.Graph(id='sales-bar-graph'),
#     html.Hr(),
#     dcc.Graph(id='monthly-sales-trend')
# ])

# @callback(
#     Output('sales-bar-graph', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_sales_bar(dimension):
#     sales_summary = df.groupby(dimension)['price'].sum().sort_values(ascending=False).head(15).reset_index()
#     fig = px.bar(
#         sales_summary,
#         x=dimension,
#         y='price',
#         title=f"Top 15 {dimension_options[dimension]}s by Total Sales",
#         labels={'price': 'Total Sales (₹)', dimension: dimension_options[dimension]},
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# @callback(
#     Output('monthly-sales-trend', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_monthly_sales(_):
#     monthly = df.groupby('month')['price'].sum().reset_index()
#     fig = px.line(
#         monthly,
#         x='month',
#         y='price',
#         title="Monthly Sales Trend",
#         labels={'price': 'Total Sales (₹)', 'month': 'Month'},
#         markers=True,
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig

# ---------------------------------------
# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/sales")

# # Load the dataset
# df = pd.read_csv("data/final_olist_dataset.csv", parse_dates=['order_purchase_timestamp'])
# df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

# # Dropdown options
# dimension_options = {
#     'customer_state': 'State',
#     # 'customer_city': 'City',
#     'product_category_name_english': 'Product Category'
# }

# layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.H3("Sales Analysis", className="text-center mb-4", style={"color": "#2c3e50"})
#         ])
#     ]),

#     dbc.Row([
#         dbc.Col([
#             html.Label("Select Dimension:", className="mb-2 fw-bold"),
#             dcc.Dropdown(
#                 id='sales-dimension-dropdown',
#                 options=[{"label": v, "value": k} for k, v in dimension_options.items()],
#                 value='customer_state',
#                 clearable=False,
#                 style={"width": "100%"}
#             )
#         ], width=4)
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader("Top 15 by Total Sales", className="fw-bold"),
#                 dbc.CardBody([
#                     dcc.Graph(id='sales-bar-graph', config={'displayModeBar': True}, style={"height": "400px"})
#                 ])
#             ])
#         ], width=12)
#     ], className="mb-4"),

#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader("Monthly Sales Trend", className="fw-bold"),
#                 dbc.CardBody([
#                     dcc.Graph(id='monthly-sales-trend', config={'displayModeBar': True}, style={"height": "400px"})
#                 ])
#             ])
#         ], width=12)
#     ])
# ], fluid=True)


# @callback(
#     Output('sales-bar-graph', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_sales_bar(dimension):
#     sales_summary = df.groupby(dimension)['price'].sum().sort_values(ascending=False).head(15).reset_index()
#     fig = px.bar(
#         sales_summary,
#         x=dimension,
#         y='price',
#         title=f"Top 15 {dimension_options[dimension]}s by Total Sales",
#         labels={'price': 'Total Sales (₹)', dimension: dimension_options[dimension]},
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig


# @callback(
#     Output('monthly-sales-trend', 'figure'),
#     Input('sales-dimension-dropdown', 'value')
# )
# def update_monthly_sales(_):
#     monthly = df.groupby('month')['price'].sum().reset_index()
#     fig = px.line(
#         monthly,
#         x='month',
#         y='price',
#         title="Monthly Sales Trend",
#         labels={'price': 'Total Sales (₹)', 'month': 'Month'},
#         markers=True,
#         template='plotly_white'
#     )
#     fig.update_layout(xaxis_tickangle=45)
#     return fig
# ------------------------------
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import json

# Register the page
dash.register_page(__name__, path="/sales")

# Load dataset
df = pd.read_csv("data/E-commerse.csv")

# Clean state names if needed
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

# Grouped Data
state_grouped = df.groupby("customer_state")["order_item_id"].count().reset_index(name="total_products")
category_grouped = df.groupby("product_category_name_english")["order_item_id"].count().reset_index(name="total_products")

# Dropdown options
dropdown_options = sorted(df["customer_state"].dropna().unique())

# Load local GeoJSON
with open("data/states_india.geojson", "r") as f:
    india_states_geojson = json.load(f)

for feature in india_states_geojson["features"]:
    feature["id"] = feature["properties"]["st_nm"].title()

# ============ Layout ============

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

# ============ Callbacks ============

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
