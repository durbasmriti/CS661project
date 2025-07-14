import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "E-Commerce Dashboard"

# Sidebar (collapsible)
sidebar = html.Div(
    [
        html.H2("Plots", className="text-white p-3"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Order Status", href="/order-status", active="exact"),
                dbc.NavLink("Sales", href="/sales", active="exact"),
                dbc.NavLink("Delivery Analysis", href="/delivery-analysis", active="exact"),
                dbc.NavLink("Monthly Order", href="/monthly-order", active="exact"),
                dbc.NavLink("Payment Method", href="/payment-method", active="exact"),
                dbc.NavLink("Revenue by City", href="/revenue-city", active="exact"),
                dbc.NavLink("Review Score", href="/review-score", active="exact"),
                dbc.NavLink("Top Sellers", href="/top-sellers", active="exact"),
                dbc.NavLink("Price and Freight", href="/price-frieght", active="exact"),
                dbc.NavLink("Product Metrix Correlation", href="/product-metrix", active="exact"),
                dbc.NavLink("Top Products", href="/top-products", active="exact"),
                dbc.NavLink("New vs Repeat Customers", href="/new-vs-repeat", id="nav-new-vs-repeat", active="exact"),
            ],
            vertical=True,
            pills=True,
            className="ms-3",
        ),
    ],
    id="sidebar",
    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "bottom": "0",
        "width": "250px",
        "padding": "20px",
        "backgroundColor": "#e5e9ee",
        "color": "white",
        "zIndex": "1000"
    },
)

# Top Navbar with Toggle Button
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Button("☰", outline=True, color="light", id="sidebar-toggle", className="me-2"),
            dbc.NavbarBrand("E-Commerce Sales Dashboard", className="text-white mx-auto fs-3"),
        ]
    ),
    color="primary",
    dark=True,
    fixed="top",
    className="mb-5"
)

page_wrapper = html.Div(
    dash.page_container,
    id="page-wrapper",
    style={"marginLeft": "250px", "marginTop": "80px", "padding": "2rem"}
)

app.layout = html.Div([
    navbar,
    html.Div(id="sidebar-container", children=[sidebar]),
    page_wrapper
])

# Toggle sidebar visibility
@app.callback(
    Output("sidebar-container", "style"),
    Output("page-wrapper", "style"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-container", "style"),
    prevent_initial_call=True
)
def toggle_sidebar(n, style):
    if style and style.get("display") == "none":
        return (
            {"display": "block"},
            {"marginLeft": "250px", "marginTop": "80px", "padding": "2rem"}
        )
    else:
        return (
            {"display": "none"},
            {"marginLeft": "0", "marginTop": "80px", "padding": "2rem"}
        )

if __name__ == "__main__":
    app.run(debug=True)
