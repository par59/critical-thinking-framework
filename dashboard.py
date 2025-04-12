import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from web_scraper import get_flipkart_products

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the data
df = get_flipkart_products('mobiles', 5)

# Create the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Flipkart Top Selling Products Dashboard", className="text-center my-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='price-bar-chart',
                figure=px.bar(df, x='name', y='price', 
                            title='Product Prices',
                            labels={'name': 'Product Name', 'price': 'Price (₹)'})
            )
        ], width=6),
        
        dbc.Col([
            dcc.Graph(
                id='rating-bar-chart',
                figure=px.bar(df, x='name', y='rating',
                            title='Product Ratings',
                            labels={'name': 'Product Name', 'rating': 'Rating'})
            )
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='reviews-bar-chart',
                figure=px.bar(df, x='name', y='reviews',
                            title='Number of Reviews',
                            labels={'name': 'Product Name', 'reviews': 'Number of Reviews'})
            )
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Product Details Table"),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            ], className="mt-4")
        ], width=12)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
