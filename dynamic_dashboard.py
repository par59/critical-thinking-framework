import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Generate more realistic sample data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
regions = ['North', 'South', 'East', 'West']
products = ['Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Headphones']
categories = ['Electronics', 'Accessories', 'Gadgets']

# Generate base data with trends and seasonality
def generate_trended_data(base_value, trend_factor, seasonality_factor, noise_factor, size):
    trend = np.linspace(0, trend_factor, size)
    seasonality = np.sin(np.linspace(0, 8*np.pi, size)) * seasonality_factor
    noise = np.random.normal(0, noise_factor, size)
    return base_value * (1 + trend + seasonality + noise)

# Generate the dataset
data = {
    'Date': dates,
    'Region': np.random.choice(regions, len(dates)),
    'Product': np.random.choice(products, len(dates)),
    'Category': np.random.choice(categories, len(dates)),
    'Sales': generate_trended_data(1000, 0.5, 0.2, 0.1, len(dates)),
    'Revenue': generate_trended_data(50000, 0.3, 0.15, 0.08, len(dates)),
    'Customers': generate_trended_data(100, 0.4, 0.1, 0.05, len(dates)),
    'Profit': generate_trended_data(20000, 0.2, 0.1, 0.06, len(dates)),
    'Marketing_Spend': generate_trended_data(10000, 0.1, 0.05, 0.03, len(dates)),
    'Customer_Satisfaction': np.random.uniform(3.5, 5.0, len(dates)),
    'Return_Rate': np.random.uniform(0.01, 0.05, len(dates)),
    'Inventory_Level': generate_trended_data(500, -0.1, 0.2, 0.1, len(dates))
}

# Create DataFrame and ensure positive values
df = pd.DataFrame(data)
df['Sales'] = df['Sales'].abs()
df['Revenue'] = df['Revenue'].abs()
df['Profit'] = df['Profit'].abs()
df['Marketing_Spend'] = df['Marketing_Spend'].abs()
df['Inventory_Level'] = df['Inventory_Level'].abs()

# Add derived metrics
df['ROI'] = (df['Profit'] / df['Marketing_Spend']) * 100
df['Average_Order_Value'] = df['Revenue'] / df['Customers']
df['Conversion_Rate'] = df['Customers'] / (df['Customers'] * 2)  # Simulated visitors
df['Profit_Margin'] = (df['Profit'] / df['Revenue']) * 100

# Round numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns
df[numeric_columns] = df[numeric_columns].round(2)

def create_download_button(data, filename):
    csv_string = data.to_csv(index=False)
    csv_string = "data:text/csv;charset=utf-8," + csv_string
    return html.A(
        html.Button("Download Data", className="btn btn-primary"),
        href=csv_string,
        download=filename,
        style={"margin-top": "10px"}
    )

# Create the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Advanced Business Analytics Dashboard", className="text-center my-4"), width=12)
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['Date'].min(),
                end_date=df['Date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], width=4),
        dbc.Col([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['Region'].unique()],
                value=df['Region'].unique().tolist(),
                multi=True
            )
        ], width=4),
        dbc.Col([
            html.Label("Select Product:"),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': product, 'value': product} for product in df['Product'].unique()],
                value=df['Product'].unique().tolist(),
                multi=True
            )
        ], width=4)
    ], className="mb-4"),
    
    # Matrices
    dbc.Row([
        dbc.Col([
            html.H4("Sales Performance Matrix"),
            dcc.Graph(id='sales-matrix'),
            html.Div(id='sales-matrix-download')
        ], width=4),
        dbc.Col([
            html.H4("Revenue Analysis Matrix"),
            dcc.Graph(id='revenue-matrix'),
            html.Div(id='revenue-matrix-download')
        ], width=4),
        dbc.Col([
            html.H4("Customer Metrics Matrix"),
            dcc.Graph(id='customer-matrix'),
            html.Div(id='customer-matrix-download')
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Profit & ROI Matrix"),
            dcc.Graph(id='profit-matrix'),
            html.Div(id='profit-matrix-download')
        ], width=6),
        dbc.Col([
            html.H4("Product Performance Matrix"),
            dcc.Graph(id='product-matrix'),
            html.Div(id='product-matrix-download')
        ], width=6)
    ]),
    
    # Graphs
    dbc.Row([
        dbc.Col([
            html.H4("Sales & Revenue Trend"),
            dcc.Graph(id='sales-trend'),
            html.Div(id='sales-trend-download')
        ], width=6),
        dbc.Col([
            html.H4("Customer Satisfaction & Return Rate"),
            dcc.Graph(id='customer-metrics'),
            html.Div(id='customer-metrics-download')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Marketing ROI Analysis"),
            dcc.Graph(id='marketing-analysis'),
            html.Div(id='marketing-analysis-download')
        ], width=6),
        dbc.Col([
            html.H4("Inventory & Conversion Analysis"),
            dcc.Graph(id='inventory-analysis'),
            html.Div(id='inventory-analysis-download')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Product Performance Comparison"),
            dcc.Graph(id='product-performance'),
            html.Div(id='product-performance-download')
        ], width=12)
    ])
], fluid=True)

# Callbacks for updating the dashboard and download buttons
@app.callback(
    [Output('sales-matrix', 'figure'),
     Output('revenue-matrix', 'figure'),
     Output('customer-matrix', 'figure'),
     Output('profit-matrix', 'figure'),
     Output('product-matrix', 'figure'),
     Output('sales-trend', 'figure'),
     Output('customer-metrics', 'figure'),
     Output('marketing-analysis', 'figure'),
     Output('inventory-analysis', 'figure'),
     Output('product-performance', 'figure'),
     Output('sales-matrix-download', 'children'),
     Output('revenue-matrix-download', 'children'),
     Output('customer-matrix-download', 'children'),
     Output('profit-matrix-download', 'children'),
     Output('product-matrix-download', 'children'),
     Output('sales-trend-download', 'children'),
     Output('customer-metrics-download', 'children'),
     Output('marketing-analysis-download', 'children'),
     Output('inventory-analysis-download', 'children'),
     Output('product-performance-download', 'children')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('region-dropdown', 'value'),
     Input('product-dropdown', 'value')]
)
def update_dashboard(start_date, end_date, regions, products):
    # Filter data based on selections
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date) & \
           (df['Region'].isin(regions)) & (df['Product'].isin(products))
    filtered_df = df[mask]
    
    # Create matrices and their data
    sales_matrix_data = filtered_df.pivot_table(values=['Sales', 'Average_Order_Value'], 
                                              index='Region', columns='Product', aggfunc='mean')
    sales_matrix = px.imshow(
        sales_matrix_data,
        title='Sales & Average Order Value by Region and Product',
        color_continuous_scale='Viridis'
    )
    
    revenue_matrix_data = filtered_df.pivot_table(values=['Revenue', 'Profit_Margin'], 
                                                index='Region', columns='Product', aggfunc='mean')
    revenue_matrix = px.imshow(
        revenue_matrix_data,
        title='Revenue & Profit Margin by Region and Product',
        color_continuous_scale='Plasma'
    )
    
    customer_matrix_data = filtered_df.pivot_table(values=['Customers', 'Customer_Satisfaction', 'Conversion_Rate'], 
                                                 index='Region', columns='Product', aggfunc='mean')
    customer_matrix = px.imshow(
        customer_matrix_data,
        title='Customer Metrics by Region and Product',
        color_continuous_scale='Inferno'
    )
    
    profit_matrix_data = filtered_df.pivot_table(values=['Profit', 'ROI'], 
                                               index='Region', columns='Product', aggfunc='mean')
    profit_matrix = px.imshow(
        profit_matrix_data,
        title='Profit & ROI by Region and Product',
        color_continuous_scale='Magma'
    )
    
    product_matrix_data = filtered_df.pivot_table(values=['Sales', 'Revenue', 'Profit', 'ROI'], 
                                                index='Product', aggfunc='mean')
    product_matrix = px.imshow(
        product_matrix_data,
        title='Product Performance Metrics',
        color_continuous_scale='Cividis'
    )
    
    # Create graphs and their data
    sales_trend_data = filtered_df.groupby('Date').agg({
        'Sales': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    sales_trend = px.line(
        sales_trend_data,
        x='Date', y=['Sales', 'Revenue'],
        title='Daily Sales & Revenue Trend'
    )
    
    customer_metrics_data = filtered_df.groupby('Date').agg({
        'Customer_Satisfaction': 'mean',
        'Return_Rate': 'mean'
    }).reset_index()
    customer_metrics = px.line(
        customer_metrics_data,
        x='Date', y=['Customer_Satisfaction', 'Return_Rate'],
        title='Customer Satisfaction & Return Rate Trend'
    )
    
    marketing_analysis = px.scatter(
        filtered_df,
        x='Marketing_Spend', y='ROI',
        color='Region', size='Revenue',
        title='Marketing ROI Analysis'
    )
    
    inventory_analysis = px.scatter(
        filtered_df,
        x='Inventory_Level', y='Conversion_Rate',
        color='Product', size='Sales',
        title='Inventory vs Conversion Rate Analysis'
    )
    
    product_performance_data = filtered_df.groupby('Product').agg({
        'Sales': 'sum',
        'Revenue': 'sum',
        'Profit': 'sum',
        'ROI': 'mean'
    }).reset_index()
    product_performance = px.bar(
        product_performance_data,
        x='Product', y=['Sales', 'Revenue', 'Profit', 'ROI'],
        title='Product Performance Comparison',
        barmode='group'
    )
    
    # Create download buttons
    sales_matrix_download = create_download_button(sales_matrix_data.reset_index(), 'sales_matrix.csv')
    revenue_matrix_download = create_download_button(revenue_matrix_data.reset_index(), 'revenue_matrix.csv')
    customer_matrix_download = create_download_button(customer_matrix_data.reset_index(), 'customer_matrix.csv')
    profit_matrix_download = create_download_button(profit_matrix_data.reset_index(), 'profit_matrix.csv')
    product_matrix_download = create_download_button(product_matrix_data.reset_index(), 'product_matrix.csv')
    sales_trend_download = create_download_button(sales_trend_data, 'sales_trend.csv')
    customer_metrics_download = create_download_button(customer_metrics_data, 'customer_metrics.csv')
    marketing_analysis_download = create_download_button(filtered_df[['Marketing_Spend', 'ROI', 'Region', 'Revenue']], 'marketing_analysis.csv')
    inventory_analysis_download = create_download_button(filtered_df[['Inventory_Level', 'Conversion_Rate', 'Product', 'Sales']], 'inventory_analysis.csv')
    product_performance_download = create_download_button(product_performance_data, 'product_performance.csv')
    
    return (sales_matrix, revenue_matrix, customer_matrix, profit_matrix, product_matrix,
            sales_trend, customer_metrics, marketing_analysis, inventory_analysis, product_performance,
            sales_matrix_download, revenue_matrix_download, customer_matrix_download, profit_matrix_download,
            product_matrix_download, sales_trend_download, customer_metrics_download, marketing_analysis_download,
            inventory_analysis_download, product_performance_download)

if __name__ == '__main__':
    app.run_server(debug=True) 