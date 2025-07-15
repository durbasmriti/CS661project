import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div(
    style={
        "textAlign": "center",
        "padding": "30px",
        "backgroundColor": "#F5F5F5",
    },
    children=[
        html.Div([
            html.H2(
                "Welcome to the E-Commerce Sales Dashboard",
                style={
                    "color": "#1a1a1a",
                    "fontWeight": "bold",
                    "fontSize": "2rem",
                    "marginBottom": "10px"
                }
            ),
            html.P(
                "Explore interactive insights into sales performance, delivery timelines, "
                "customer feedback, and much more. This dashboard, built using Plotly Dash, "
                "enables intuitive exploration of Indian e-commerce metrics",
                style={
                    "fontSize": "24px",
                    "color": "#444",
                    "maxWidth": "80%",
                    "margin": "0 auto"
                }
            )
        ])
    ]
)
