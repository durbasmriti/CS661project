# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc


# dash.register_page(__name__, path="/review-score")


# df = pd.read_csv("data/E-commerse.csv")
# df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], format='mixed', errors='coerce')
# df["review_score"] = df["review_score"].astype("int")

# # Card
# def create_card(title, graph_id):
#     return dbc.Card([
#         dbc.CardHeader(title, className="bg-primary text-white text-center fw-bold"),
#         dbc.CardBody(dcc.Graph(id=graph_id))
#     ], className="mb-4 shadow")


# layout = html.Div([
#     html.H3("Review Score Analysis", className="text-center text-primary mb-4"),

#     dbc.Row([
#         dbc.Col(create_card("Review Score Distribution", "review-pie"), width=6),
#         dbc.Col(create_card("Average Review Score Over Time", "review-timeline"), width=6),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Top Product Categories by Review Score", "review-bar-category"), width=12),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Review Score Distribution by Top Categories", "review-box-category"), width=12),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Review Score Frequency by Customer State", "review-heatmap"), width=12),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Radar View of Avg Review Scores (Top 10 Categories)", "review-radar"), width=12),
#     ])
# ])

# # Donut chart
# @callback(
#     Output("review-pie", "figure"),
#     Input("review-pie", "id")
# )
# def update_pie(_):
#     pie_df = df["review_score"].value_counts().sort_index().reset_index()
#     pie_df.columns = ["score", "count"]
#     fig = px.pie(
#         pie_df,
#         values="count",
#         names="score",
#         hole=0.4,
#         template="plotly_white",
#         color_discrete_sequence=px.colors.qualitative.Pastel
#     )
#     return fig

# # Timeline line plot
# @callback(
#     Output("review-timeline", "figure"),
#     Input("review-timeline", "id")
# )
# def update_timeline(_):
#     avg_score = df.groupby("review_creation_date")["review_score"].mean().reset_index()
#     fig = px.line(
#         avg_score,
#         x="review_creation_date",
#         y="review_score",
#         markers=True,
#         template="plotly_white"
#     )
#     fig.update_layout(title="Average Review Score Over Time", xaxis_title="Date", yaxis_title="Avg Score")
#     return fig

# # Stacked bar chart
# @callback(
#     Output("review-bar-category", "figure"),
#     Input("review-bar-category", "id")
# )
# def update_bar(_):
#     grouped = df.groupby(["product_category_name_english", "review_score"]).size().reset_index(name="count")
#     top_categories = grouped.groupby("product_category_name_english")["count"].sum().nlargest(10).index
#     grouped = grouped[grouped["product_category_name_english"].isin(top_categories)]
#     fig = px.bar(
#         grouped,
#         x="product_category_name_english",
#         y="count",
#         color="review_score",
#         template="plotly_white"
#     )
#     fig.update_layout(title="Top Product Categories by Review Score", xaxis_title="Product Category", yaxis_title="Review Count")
#     return fig

# # Boxplot
# @callback(
#     Output("review-box-category", "figure"),
#     Input("review-box-category", "id")
# )
# def update_box(_):
#     top = df["product_category_name_english"].value_counts().head(10).index
#     filtered = df[df["product_category_name_english"].isin(top)]
#     fig = px.box(
#         filtered,
#         x="product_category_name_english",
#         y="review_score",
#         points="all",
#         template="plotly_white",
#         color="product_category_name_english",
#         color_discrete_sequence=px.colors.qualitative.Safe
#     )
#     fig.update_layout(title="Review Score Distribution by Top Categories", xaxis_tickangle=45)
#     return fig

# # Heatmap
# @callback(
#     Output("review-heatmap", "figure"),
#     Input("review-heatmap", "id")
# )
# def update_heatmap(_):
#     heat_df = df.groupby(["customer_state", "review_score"]).size().reset_index(name="count")
#     fig = px.density_heatmap(
#         heat_df,
#         x="review_score",
#         y="customer_state",
#         z="count",
#         color_continuous_scale="Blues",
#         template="plotly_white"
#     )
#     fig.update_layout(title="Review Score Frequency by Customer State")
#     return fig

# # Radar plot with top 10 categories
# @callback(
#     Output("review-radar", "figure"),
#     Input("review-radar", "id")
# )
# def update_radar(_):
#     top = df["product_category_name_english"].value_counts().head(10).index
#     radar_df = df[df["product_category_name_english"].isin(top)].groupby("product_category_name_english")["review_score"].mean().reset_index()
#     fig = px.line_polar(
#         radar_df,
#         r="review_score",
#         theta="product_category_name_english",
#         line_close=True,
#         template="plotly",
#         color_discrete_sequence=["#3B82F6"]
#     )
#     fig.update_layout(title="Radar View of Avg Review Scores (Top 10 Categories)")
#     return fig


# import dash
# import pandas as pd
# import plotly.express as px
# from dash import dcc, html, Input, Output, callback
# import dash_bootstrap_components as dbc

# dash.register_page(__name__, path="/review-score")

# # Load and preprocess
# df = pd.read_csv("data/E-commerse.csv")
# df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], format="mixed", errors="coerce")
# df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")

# # Card template
# def create_card(title, graph_id):
#     return dbc.Card([
#         dbc.CardHeader(title, className="bg-primary text-white text-center fw-bold"),
#         dbc.CardBody(dcc.Graph(id=graph_id))
#     ], className="mb-4 shadow")

# layout = html.Div([
#     html.H3("Review Score Analysis", className="text-center text-primary mb-4"),

#     dbc.Row([
#         dbc.Col(create_card("Average Review Score by Category", "avg-review-category"), width=6),
#         dbc.Col(create_card("Avg Review Score Over Time", "avg-review-time"), width=6),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Boxplot: Review Score by Top 10 Products", "boxplot-product"), width=12),
#     ]),

#     dbc.Row([
#         dbc.Col(create_card("Scatter: Product Weight vs Review Score", "scatter-weight-review"), width=12),
#     ])
# ])

# # 1. Bar chart: Avg review by category
# @callback(Output("avg-review-category", "figure"), Input("avg-review-category", "id"))
# def update_avg_review_category(_):
#     avg_df = df.groupby("product_category_name_english")["review_score"].mean().reset_index()
#     top = df["product_category_name_english"].value_counts().head(15).index
#     avg_df = avg_df[avg_df["product_category_name_english"].isin(top)]
#     fig = px.bar(
#         avg_df.sort_values("review_score", ascending=False),
#         x="product_category_name_english", y="review_score",
#         title="Average Review Score by Top Categories",
#         color="review_score", color_continuous_scale="Tealgrn",
#         template="plotly_white"
#     )
#     fig.update_layout(xaxis_title="Category", yaxis_title="Avg Review Score", xaxis_tickangle=45)
#     return fig

# # 2. Timeline: Avg review over time
# @callback(Output("avg-review-time", "figure"), Input("avg-review-time", "id"))
# def update_review_timeline(_):
#     trend = df.groupby("review_creation_date")["review_score"].mean().reset_index()
#     fig = px.line(
#         trend, x="review_creation_date", y="review_score",
#         title="Average Review Score Over Time",
#         markers=True, template="plotly_white", color_discrete_sequence=["#636EFA"]
#     )
#     fig.update_layout(xaxis_title="Date", yaxis_title="Avg Score")
#     return fig

# # 3. Boxplot by top 10 product IDs (by number of reviews)
# @callback(Output("boxplot-product", "figure"), Input("boxplot-product", "id"))
# def update_box_product(_):
#     top_products = df["product_id"].value_counts().head(10).index
#     filtered = df[df["product_id"].isin(top_products)]
#     fig = px.box(
#         filtered, x="product_id", y="review_score",
#         color="product_id",
#         title="Review Score Distribution for Top 10 Products",
#         template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2
#     )
#     fig.update_layout(xaxis_title="Product ID", yaxis_title="Review Score")
#     return fig

# # 4. Scatter: Product weight vs review
# @callback(Output("scatter-weight-review", "figure"), Input("scatter-weight-review", "id"))
# def update_scatter_weight_review(_):
#     filtered = df[(df["product_weight_g"] > 0) & (df["product_weight_g"] < 10000)]
#     fig = px.scatter(
#         filtered, x="product_weight_g", y="review_score",
#         color="review_score", template="plotly_white",
#         title="Product Weight vs Review Score",
#         color_continuous_scale="Rainbow"
#     )
#     fig.update_layout(xaxis_title="Product Weight (g)", yaxis_title="Review Score")
#     return fig


import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/review-score")

# Load data
df = pd.read_csv("data/E-commerse.csv")
df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], format='mixed', errors='coerce')
df["review_score"] = df["review_score"].astype("int")

# Card creator
def create_card(title, graph_id):
    return dbc.Card([
        dbc.CardHeader(title, className="bg-primary text-white text-center fw-bold"),
        dbc.CardBody(dcc.Graph(id=graph_id))
    ], className="mb-4 shadow")

# Layout
layout = html.Div([
    html.H3("Review Score Analysis", className="text-center text-primary mb-4"),

    dbc.Row([
        dbc.Col(create_card("Avg Review Score by Product Category", "review-bar-category"), width=6),
        dbc.Col(create_card("Review Score Trend (Top Categories)", "review-trend"), width=6),
    ]),

    dbc.Row([
        dbc.Col(create_card("Top Product Categories by Review Score", "review-bar-score"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Review Score Distribution by Top Categories", "review-box-category"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Review Score Frequency by Customer State", "review-heatmap"), width=12),
    ]),

    dbc.Row([
        dbc.Col(create_card("Radar View of Avg Review Scores (Top 10 Categories)", "review-radar"), width=12),
    ])
])

# ---------------- CALLBACKS ---------------- #

# Bar Chart: Avg Review Score by Category
@callback(
    Output("review-bar-category", "figure"),
    Input("review-bar-category", "id")
)
def update_avg_score_bar(_):
    avg_df = df.groupby("product_category_name_english")["review_score"].mean().reset_index()
    count_df = df["product_category_name_english"].value_counts().head(10).index
    avg_df = avg_df[avg_df["product_category_name_english"].isin(count_df)]

    fig = px.bar(
        avg_df.sort_values("review_score", ascending=False),
        x="product_category_name_english",
        y="review_score",
        title="Avg Review Score by Product Category",
        labels={"product_category_name_english": "Category", "review_score": "Avg Score"},
        color="review_score",
        color_continuous_scale="Plasma",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=45)
    return fig

# Line Plot: Review Score Trend (Top Categories)
@callback(
    Output("review-trend", "figure"),
    Input("review-trend", "id")
)
def update_review_trend(_):
    top_categories = df["product_category_name_english"].value_counts().head(5).index
    filtered = df[df["product_category_name_english"].isin(top_categories)]
    trend_df = (
        filtered.groupby([pd.Grouper(key="review_creation_date", freq="M"), "product_category_name_english"])
        ["review_score"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        trend_df,
        x="review_creation_date",
        y="review_score",
        color="product_category_name_english",
        markers=True,
        template="plotly_white",
        title="Monthly Avg Review Score (Top 5 Categories)",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Avg Review Score")
    return fig

# Stacked Bar: Top Categories by Score
@callback(
    Output("review-bar-score", "figure"),
    Input("review-bar-score", "id")
)
def update_bar(_):
    grouped = df.groupby(["product_category_name_english", "review_score"]).size().reset_index(name="count")
    top_categories = grouped.groupby("product_category_name_english")["count"].sum().nlargest(10).index
    grouped = grouped[grouped["product_category_name_english"].isin(top_categories)]
    fig = px.bar(
        grouped,
        x="product_category_name_english",
        y="count",
        color="review_score",
        template="plotly_white"
    )
    fig.update_layout(title="Top Product Categories by Review Score", xaxis_title="Product Category", yaxis_title="Review Count")
    return fig

# Boxplot: Score Distribution by Category
@callback(
    Output("review-box-category", "figure"),
    Input("review-box-category", "id")
)
def update_box(_):
    top = df["product_category_name_english"].value_counts().head(10).index
    filtered = df[df["product_category_name_english"].isin(top)]
    fig = px.box(
        filtered,
        x="product_category_name_english",
        y="review_score",
        points="all",
        template="plotly_white",
        color="product_category_name_english",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(title="Review Score Distribution by Top Categories", xaxis_tickangle=45)
    return fig

# Heatmap: Score Frequency by State
@callback(
    Output("review-heatmap", "figure"),
    Input("review-heatmap", "id")
)
def update_heatmap(_):
    heat_df = df.groupby(["customer_state", "review_score"]).size().reset_index(name="count")
    fig = px.density_heatmap(
        heat_df,
        x="review_score",
        y="customer_state",
        z="count",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig.update_layout(title="Review Score Frequency by Customer State")
    return fig

# Radar: Avg Review by Top 10 Categories
@callback(
    Output("review-radar", "figure"),
    Input("review-radar", "id")
)
def update_radar(_):
    top = df["product_category_name_english"].value_counts().head(10).index
    radar_df = df[df["product_category_name_english"].isin(top)].groupby("product_category_name_english")["review_score"].mean().reset_index()
    fig = px.line_polar(
        radar_df,
        r="review_score",
        theta="product_category_name_english",
        line_close=True,
        template="plotly",
        color_discrete_sequence=["#3B82F6"]
    )
    fig.update_layout(title="Radar View of Avg Review Scores (Top 10 Categories)")
    return fig
