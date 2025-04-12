import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Interactive Dashboard")

# Create sample data
@st.cache_data
def generate_data():
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    data = {
        'Date': dates,
        'Revenue': np.random.normal(1000, 200, len(dates)).cumsum(),
        'Users': np.random.normal(100, 20, len(dates)).cumsum(),
        'Conversion Rate': np.random.normal(0.3, 0.05, len(dates)),
        'Average Order Value': np.random.normal(50, 10, len(dates)),
        'Customer Satisfaction': np.random.normal(4.5, 0.3, len(dates))
    }
    return pd.DataFrame(data)

df = generate_data()

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Filter data based on date range
mask = (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))
filtered_df = df[mask]

# Create columns for metrics
col1, col2, col3, col4, col5 = st.columns(5)

# Metric 1: Revenue
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Total Revenue",
        value=f"${filtered_df['Revenue'].iloc[-1]:,.0f}",
        delta=f"${filtered_df['Revenue'].iloc[-1] - filtered_df['Revenue'].iloc[0]:,.0f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Metric 2: Users
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Total Users",
        value=f"{filtered_df['Users'].iloc[-1]:,.0f}",
        delta=f"{filtered_df['Users'].iloc[-1] - filtered_df['Users'].iloc[0]:,.0f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Metric 3: Conversion Rate
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Conversion Rate",
        value=f"{filtered_df['Conversion Rate'].mean():.1%}",
        delta=f"{(filtered_df['Conversion Rate'].mean() - df['Conversion Rate'].mean()):.1%}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Metric 4: Average Order Value
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Avg Order Value",
        value=f"${filtered_df['Average Order Value'].mean():.2f}",
        delta=f"${filtered_df['Average Order Value'].mean() - df['Average Order Value'].mean():.2f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Metric 5: Customer Satisfaction
with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Customer Satisfaction",
        value=f"{filtered_df['Customer Satisfaction'].mean():.1f}/5",
        delta=f"{filtered_df['Customer Satisfaction'].mean() - df['Customer Satisfaction'].mean():.1f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Create charts
st.subheader("Trend Analysis")

# Line chart for Revenue and Users
fig1 = px.line(
    filtered_df,
    x='Date',
    y=['Revenue', 'Users'],
    title='Revenue and Users Over Time',
    labels={'value': 'Value', 'variable': 'Metric'},
    template='plotly_white'
)
st.plotly_chart(fig1, use_container_width=True)

# Bar chart for Conversion Rate and Average Order Value
fig2 = px.bar(
    filtered_df,
    x='Date',
    y=['Conversion Rate', 'Average Order Value'],
    title='Conversion Rate and Average Order Value',
    labels={'value': 'Value', 'variable': 'Metric'},
    template='plotly_white'
)
st.plotly_chart(fig2, use_container_width=True)

# Add a download button for the data
st.sidebar.download_button(
    label="Download Data",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='dashboard_data.csv',
    mime='text/csv'
)
