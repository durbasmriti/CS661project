import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__, path="/delivery-analysis", name="Delivery Analysis")

# Path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'Final_olist_dataset.csv')


# Columns for pie chart: 8th and 9th (0-indexed: 7 and 8)
pie_col_names = [7, 8]
pie_col_labels = ['order_delivered_customer_date', 'order_estimated_delivery_date']

# Columns for bar chart: use column names for clarity
bar_col_names = ['order_purchase_timestamp', 'order_delivered_customer_date', 'product_category_name_english']
bar_col_labels = ['order_purchase_timestamp', 'order_delivered_customer_date', 'product_category_name_english']


# Sample 3000 rows for performance
sample_size = 3000

# PIE CHART DATA
try:
    df_pie = pd.read_csv(DATA_PATH, usecols=pie_col_names)
    df_pie.columns = pie_col_labels
    df_pie_sample = df_pie.sample(n=sample_size, random_state=42)
except Exception as e:
    df_pie_sample = pd.DataFrame(columns=pie_col_labels)

for col in pie_col_labels:
    df_pie_sample[col] = pd.to_datetime(df_pie_sample[col], errors='coerce').dt.date

def get_status(row):
    if pd.isnull(row['order_delivered_customer_date']) or pd.isnull(row['order_estimated_delivery_date']):
        return 'Unknown'
    if row['order_delivered_customer_date'] >= row['order_estimated_delivery_date']:
        return 'On Schedule'
    else:
        return 'Late'

df_pie_sample['Delivery Status'] = df_pie_sample.apply(get_status, axis=1)
status_counts = df_pie_sample['Delivery Status'].value_counts().reindex(['On Schedule', 'Late']).fillna(0)

fig_pie = px.pie(
    names=status_counts.index,
    values=status_counts.values,
    title='Delivery Analysis: On Schedule vs Late Deliveries',
    color=status_counts.index,
    color_discrete_map={
        'On Schedule': '#2ecc71',  # green
        'Late': '#e74c3c'          # red
    },
    hole=0.3
)
fig_pie.update_traces(textinfo='percent+label', pull=[0.05, 0.05])

# BAR CHART DATA
try:
    # Increase sample size for more valid categories
    # Use the sample file for performance
    DATA_PATH_SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'Samples_ECom_Random.csv')
    df_bar = pd.read_csv(DATA_PATH_SAMPLE, usecols=bar_col_names)
except Exception as e:
    df_bar = pd.DataFrame(columns=bar_col_labels)

# Convert to pandas datetime and normalize (ignore time, keep as pandas datetime)
for col in ['order_purchase_timestamp', 'order_delivered_customer_date']:
    df_bar[col] = pd.to_datetime(df_bar[col], errors='coerce').dt.normalize()

# Calculate delivery days
df_bar['delivery_days'] = (df_bar['order_delivered_customer_date'] - df_bar['order_purchase_timestamp']).dt.days

# Filter to keep only string category names (avoid numbers, NaN, empty)
category_delivery = df_bar.dropna(subset=['product_category_name_english', 'delivery_days'])
category_delivery = category_delivery[category_delivery['product_category_name_english'].apply(lambda x: isinstance(x, str) and x.strip() != "")]

# Sample after filtering to ensure valid categories
if len(category_delivery) > sample_size:
    category_delivery = category_delivery.sample(n=sample_size, random_state=42)

# Group by product category name and calculate average delivery days
category_avg = category_delivery.groupby('product_category_name_english', as_index=False)['delivery_days'].mean()
category_avg = category_avg.sort_values('delivery_days', ascending=False)

# Show only top 20 categories for readability
category_avg = category_avg.head(20)

# Bar chart
fig_bar = px.bar(
    category_avg,
    x='delivery_days',
    y='product_category_name_english',
    orientation='h',
    color='delivery_days',
    color_continuous_scale=px.colors.sequential.Blues,
    labels={
        'delivery_days': 'Average Delivery Days',
        'product_category_name_english': 'Product Category'
    },
    title='Average Delivery Days by Product Category'
)
fig_bar.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    margin=dict(l=250),  # Increase left margin for long labels
    font=dict(size=12)   # Optionally, reduce font size for readability
)

def layout():
    return html.Div([
        html.H2("Delivery Analysis", className="mb-4"),
        dcc.Graph(figure=fig_pie),
        html.Hr(),
        html.H3("Average Delivery Days by Product Category", className="mb-3 mt-4"),
        dcc.Graph(figure=fig_bar)
    ])
