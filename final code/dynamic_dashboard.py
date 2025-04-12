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

# Generate sample data
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
data = {
    'Date': dates,
    'Sales': np.random.randint(1000, 5000, len(dates)),
    'Revenue': np.random.uniform(10000, 50000, len(dates)),
    'Customers': np.random.randint(50, 200, len(dates)),
    'Profit': np.random.uniform(5000, 25000, len(dates)),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
    'Product': np.random.choice(['A', 'B', 'C', 'D', 'E'], len(dates))
}
df = pd.DataFrame(data)

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
        dbc.Col(html.H1("Dynamic Business Analytics Dashboard", className="text-center my-4"), width=12)
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
            html.H4("Sales Matrix"),
            dcc.Graph(id='sales-matrix'),
            html.Div(id='sales-matrix-download')
        ], width=4),
        dbc.Col([
            html.H4("Revenue Matrix"),
            dcc.Graph(id='revenue-matrix'),
            html.Div(id='revenue-matrix-download')
        ], width=4),
        dbc.Col([
            html.H4("Customer Matrix"),
            dcc.Graph(id='customer-matrix'),
            html.Div(id='customer-matrix-download')
        ], width=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Profit Matrix"),
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
            html.H4("Sales Trend"),
            dcc.Graph(id='sales-trend'),
            html.Div(id='sales-trend-download')
        ], width=6),
        dbc.Col([
            html.H4("Revenue Distribution"),
            dcc.Graph(id='revenue-distribution'),
            html.Div(id='revenue-distribution-download')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Customer Growth"),
            dcc.Graph(id='customer-growth'),
            html.Div(id='customer-growth-download')
        ], width=6),
        dbc.Col([
            html.H4("Profit Analysis"),
            dcc.Graph(id='profit-analysis'),
            html.Div(id='profit-analysis-download')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Product Performance"),
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
     Output('revenue-distribution', 'figure'),
     Output('customer-growth', 'figure'),
     Output('profit-analysis', 'figure'),
     Output('product-performance', 'figure'),
     Output('sales-matrix-download', 'children'),
     Output('revenue-matrix-download', 'children'),
     Output('customer-matrix-download', 'children'),
     Output('profit-matrix-download', 'children'),
     Output('product-matrix-download', 'children'),
     Output('sales-trend-download', 'children'),
     Output('revenue-distribution-download', 'children'),
     Output('customer-growth-download', 'children'),
     Output('profit-analysis-download', 'children'),
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
    sales_matrix_data = filtered_df.pivot_table(values='Sales', index='Region', columns='Product', aggfunc='sum')
    sales_matrix = px.imshow(
        sales_matrix_data,
        title='Sales by Region and Product',
        color_continuous_scale='Viridis'
    )
    
    revenue_matrix_data = filtered_df.pivot_table(values='Revenue', index='Region', columns='Product', aggfunc='sum')
    revenue_matrix = px.imshow(
        revenue_matrix_data,
        title='Revenue by Region and Product',
        color_continuous_scale='Plasma'
    )
    
    customer_matrix_data = filtered_df.pivot_table(values='Customers', index='Region', columns='Product', aggfunc='sum')
    customer_matrix = px.imshow(
        customer_matrix_data,
        title='Customers by Region and Product',
        color_continuous_scale='Inferno'
    )
    
    profit_matrix_data = filtered_df.pivot_table(values='Profit', index='Region', columns='Product', aggfunc='sum')
    profit_matrix = px.imshow(
        profit_matrix_data,
        title='Profit by Region and Product',
        color_continuous_scale='Magma'
    )
    
    product_matrix_data = filtered_df.pivot_table(values=['Sales', 'Revenue', 'Profit'], index='Product', aggfunc='sum')
    product_matrix = px.imshow(
        product_matrix_data,
        title='Product Performance Metrics',
        color_continuous_scale='Cividis'
    )
    
    # Create graphs and their data
    sales_trend_data = filtered_df.groupby('Date')['Sales'].sum().reset_index()
    sales_trend = px.line(
        sales_trend_data,
        x='Date', y='Sales',
        title='Daily Sales Trend'
    )
    
    revenue_distribution = px.box(
        filtered_df,
        x='Region', y='Revenue',
        title='Revenue Distribution by Region'
    )
    
    customer_growth_data = filtered_df.groupby('Date')['Customers'].sum().reset_index()
    customer_growth = px.area(
        customer_growth_data,
        x='Date', y='Customers',
        title='Customer Growth Over Time'
    )
    
    profit_analysis = px.scatter(
        filtered_df,
        x='Sales', y='Profit',
        color='Region', size='Revenue',
        title='Profit vs Sales Analysis'
    )
    
    product_performance_data = filtered_df.groupby('Product').agg({
        'Sales': 'sum',
        'Revenue': 'sum',
        'Profit': 'sum'
    }).reset_index()
    product_performance = px.bar(
        product_performance_data,
        x='Product', y=['Sales', 'Revenue', 'Profit'],
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
    revenue_distribution_download = create_download_button(filtered_df[['Region', 'Revenue']], 'revenue_distribution.csv')
    customer_growth_download = create_download_button(customer_growth_data, 'customer_growth.csv')
    profit_analysis_download = create_download_button(filtered_df[['Sales', 'Profit', 'Region', 'Revenue']], 'profit_analysis.csv')
    product_performance_download = create_download_button(product_performance_data, 'product_performance.csv')
    
    return (sales_matrix, revenue_matrix, customer_matrix, profit_matrix, product_matrix,
            sales_trend, revenue_distribution, customer_growth, profit_analysis, product_performance,
            sales_matrix_download, revenue_matrix_download, customer_matrix_download, profit_matrix_download,
            product_matrix_download, sales_trend_download, revenue_distribution_download, customer_growth_download,
            profit_analysis_download, product_performance_download)

if __name__ == '__main__':
    app.run_server(debug=True) 