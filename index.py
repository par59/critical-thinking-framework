import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Employee Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("Employee Analytics Dashboard")

# Read the data
@st.cache_data
def load_data():
    df = pd.read_csv('5000 Records.csv')
    df['Last % Hike'] = df['Last % Hike'].str.rstrip('%').astype('float')
    df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
    df['Year of Joining'] = df['Date of Joining'].dt.year
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Region filter
selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Gender filter
selected_genders = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Age range filter
age_min = int(df['Age in Yrs.'].min())
age_max = int(df['Age in Yrs.'].max())
age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)

# Filter data based on selections
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Gender'].isin(selected_genders)) &
    (df['Age in Yrs.'] >= age_range[0]) &
    (df['Age in Yrs.'] <= age_range[1])
]

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Demographics", "Compensation", "Tenure", "Geographic", "Performance"
])

# Demographics Tab
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(
            px.pie(filtered_df, names='Gender', title='Gender Distribution'),
            use_container_width=True
        )
        st.download_button(
            "Download Gender Data",
            filtered_df[['Gender']].to_csv(index=False),
            "gender_data.csv",
            "text/csv"
        )
    
    with col2:
        st.plotly_chart(
            px.histogram(filtered_df, x='Age in Yrs.', title='Age Distribution'),
            use_container_width=True
        )
        st.download_button(
            "Download Age Data",
            filtered_df[['Age in Yrs.']].to_csv(index=False),
            "age_data.csv",
            "text/csv"
        )
    
    with col3:
        st.plotly_chart(
            px.pie(filtered_df, names='Region', title='Regional Distribution'),
            use_container_width=True
        )
        st.download_button(
            "Download Regional Data",
            filtered_df[['Region']].to_csv(index=False),
            "region_data.csv",
            "text/csv"
        )

# Compensation Tab
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            px.bar(
                filtered_df.groupby('Region')['Salary'].mean().reset_index(),
                x='Region', y='Salary', title='Average Salary by Region'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download Salary Data",
            filtered_df[['Region', 'Salary']].to_csv(index=False),
            "salary_data.csv",
            "text/csv"
        )
    
    with col2:
        st.plotly_chart(
            px.box(filtered_df, y='Salary', title='Salary Distribution'),
            use_container_width=True
        )
        st.download_button(
            "Download Distribution Data",
            filtered_df[['Salary']].to_csv(index=False),
            "distribution_data.csv",
            "text/csv"
        )

# Tenure Tab
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            px.histogram(
                filtered_df, x='Age in Company (Years)',
                title='Years of Service Distribution'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download Tenure Data",
            filtered_df[['Age in Company (Years)']].to_csv(index=False),
            "tenure_data.csv",
            "text/csv"
        )
    
    with col2:
        st.plotly_chart(
            px.line(
                filtered_df.groupby('Year of Joining').size().reset_index(),
                x='Year of Joining', y=0, title='Hiring Trends'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download Hiring Data",
            filtered_df[['Year of Joining']].to_csv(index=False),
            "hiring_data.csv",
            "text/csv"
        )

# Geographic Tab
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            px.choropleth(
                filtered_df.groupby('State').size().reset_index(),
                locations='State', locationmode='USA-states',
                color=0, scope='usa', title='Employee Count by State'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download State Data",
            filtered_df[['State']].to_csv(index=False),
            "state_data.csv",
            "text/csv"
        )
    
    with col2:
        st.plotly_chart(
            px.treemap(
                filtered_df.groupby(['State', 'City']).size().reset_index(),
                path=['State', 'City'], values=0,
                title='City-wise Employee Distribution'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download City Data",
            filtered_df[['State', 'City']].to_csv(index=False),
            "city_data.csv",
            "text/csv"
        )

# Performance Tab
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            px.scatter(
                filtered_df, x='Age in Company (Years)',
                y='Salary', title='Salary vs Years of Service'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download Correlation Data",
            filtered_df[['Age in Company (Years)', 'Salary']].to_csv(index=False),
            "correlation_data.csv",
            "text/csv"
        )
    
    with col2:
        st.plotly_chart(
            px.scatter(
                filtered_df, x='Age in Yrs.',
                y='Salary', size='Salary',
                title='Age vs Salary Distribution'
            ),
            use_container_width=True
        )
        st.download_button(
            "Download Age-Salary Data",
            filtered_df[['Age in Yrs.', 'Salary']].to_csv(index=False),
            "age_salary_data.csv",
            "text/csv"
        )

# Download all data button
st.sidebar.download_button(
    "Download All Data",
    filtered_df.to_csv(index=False),
    "all_data.csv",
    "text/csv"
) 