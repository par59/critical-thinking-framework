import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the data
df = pd.read_csv('5000 Records.csv')

# Data preprocessing
df['Last % Hike'] = df['Last % Hike'].str.rstrip('%').astype('float')
df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
df['Year of Joining'] = df['Date of Joining'].dt.year

# Create the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Employee Analytics Dashboard", className="text-center my-4"), width=12)
    ]),
    
    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': region, 'value': region} for region in df['Region'].unique()],
                value=None,
                multi=True
            )
        ], width=3),
        dbc.Col([
            html.Label("Select Gender:"),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': gender, 'value': gender} for gender in df['Gender'].unique()],
                value=None,
                multi=True
            )
        ], width=3),
        dbc.Col([
            html.Label("Select Age Range:"),
            dcc.RangeSlider(
                id='age-slider',
                min=df['Age in Yrs.'].min(),
                max=df['Age in Yrs.'].max(),
                step=1,
                value=[df['Age in Yrs.'].min(), df['Age in Yrs.'].max()],
                marks={i: str(i) for i in range(int(df['Age in Yrs.'].min()), int(df['Age in Yrs.'].max()) + 1, 5)}
            )
        ], width=6)
    ], className="mb-4"),
    
    # Tabs for different sections
    dbc.Tabs([
        # Demographics Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='gender-distribution'),
                    html.Button("Download Gender Data", id="btn-gender", className="btn btn-primary mt-2")
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='age-distribution'),
                    html.Button("Download Age Data", id="btn-age", className="btn btn-primary mt-2")
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='regional-distribution'),
                    html.Button("Download Regional Data", id="btn-region", className="btn btn-primary mt-2")
                ], width=4)
            ])
        ], label="Demographics"),
        
        # Compensation Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='salary-by-region'),
                    html.Button("Download Salary Data", id="btn-salary", className="btn btn-primary mt-2")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='salary-distribution'),
                    html.Button("Download Distribution Data", id="btn-dist", className="btn btn-primary mt-2")
                ], width=6)
            ])
        ], label="Compensation"),
        
        # Tenure Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='tenure-distribution'),
                    html.Button("Download Tenure Data", id="btn-tenure", className="btn btn-primary mt-2")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='hiring-trends'),
                    html.Button("Download Hiring Data", id="btn-hiring", className="btn btn-primary mt-2")
                ], width=6)
            ])
        ], label="Tenure"),
        
        # Geographic Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='state-distribution'),
                    html.Button("Download State Data", id="btn-state", className="btn btn-primary mt-2")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='city-distribution'),
                    html.Button("Download City Data", id="btn-city", className="btn btn-primary mt-2")
                ], width=6)
            ])
        ], label="Geographic"),
        
        # Performance Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='salary-vs-tenure'),
                    html.Button("Download Correlation Data", id="btn-correlation", className="btn btn-primary mt-2")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='age-vs-salary'),
                    html.Button("Download Age-Salary Data", id="btn-age-salary", className="btn btn-primary mt-2")
                ], width=6)
            ])
        ], label="Performance")
    ]),
    
    # Download all data button
    dbc.Row([
        dbc.Col(
            html.Button("Download All Data", id="btn-all", className="btn btn-success mt-4"),
            width=12, className="text-center"
        )
    ])
])

# Callbacks for filters
@app.callback(
    Output('gender-distribution', 'figure'),
    Output('age-distribution', 'figure'),
    Output('regional-distribution', 'figure'),
    Output('salary-by-region', 'figure'),
    Output('salary-distribution', 'figure'),
    Output('tenure-distribution', 'figure'),
    Output('hiring-trends', 'figure'),
    Output('state-distribution', 'figure'),
    Output('city-distribution', 'figure'),
    Output('salary-vs-tenure', 'figure'),
    Output('age-vs-salary', 'figure'),
    Input('region-filter', 'value'),
    Input('gender-filter', 'value'),
    Input('age-slider', 'value')
)
def update_graphs(selected_regions, selected_genders, age_range):
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]
    filtered_df = filtered_df[
        (filtered_df['Age in Yrs.'] >= age_range[0]) & 
        (filtered_df['Age in Yrs.'] <= age_range[1])
    ]
    
    # Create all visualizations
    gender_fig = px.pie(filtered_df, names='Gender', title='Gender Distribution')
    age_fig = px.histogram(filtered_df, x='Age in Yrs.', title='Age Distribution')
    region_fig = px.pie(filtered_df, names='Region', title='Regional Distribution')
    
    salary_region_fig = px.bar(
        filtered_df.groupby('Region')['Salary'].mean().reset_index(),
        x='Region', y='Salary', title='Average Salary by Region'
    )
    
    salary_dist_fig = px.box(filtered_df, y='Salary', title='Salary Distribution')
    
    tenure_fig = px.histogram(
        filtered_df, x='Age in Company (Years)',
        title='Years of Service Distribution'
    )
    
    hiring_fig = px.line(
        filtered_df.groupby('Year of Joining').size().reset_index(),
        x='Year of Joining', y=0, title='Hiring Trends'
    )
    
    state_fig = px.choropleth(
        filtered_df.groupby('State').size().reset_index(),
        locations='State', locationmode='USA-states',
        color=0, scope='usa', title='Employee Count by State'
    )
    
    city_fig = px.treemap(
        filtered_df.groupby(['State', 'City']).size().reset_index(),
        path=['State', 'City'], values=0,
        title='City-wise Employee Distribution'
    )
    
    salary_tenure_fig = px.scatter(
        filtered_df, x='Age in Company (Years)',
        y='Salary', title='Salary vs Years of Service'
    )
    
    age_salary_fig = px.scatter(
        filtered_df, x='Age in Yrs.',
        y='Salary', size='Salary',
        title='Age vs Salary Distribution'
    )
    
    return (
        gender_fig, age_fig, region_fig,
        salary_region_fig, salary_dist_fig,
        tenure_fig, hiring_fig, state_fig,
        city_fig, salary_tenure_fig, age_salary_fig
    )

# Download callbacks
@app.callback(
    Output("download-gender", "data"),
    Input("btn-gender", "n_clicks"),
    prevent_initial_call=True
)
def download_gender(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return dcc.send_data_frame(df[['Gender']].to_csv, "gender_data.csv")

# Add similar download callbacks for other buttons...

if __name__ == '__main__':
    app.run_server(debug=True) 