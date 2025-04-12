import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="5000 Records Dashboard", layout="wide")

# Title
st.title("📊 Dashboard for 5000 Records")

# Load the CSV data
@st.cache_data
def load_data():
    path = "D:/indiannn/lovely/5000 Records.csv"
    return pd.read_csv(path)

df = load_data()

# Show the raw data toggle
with st.expander("📄 Show Raw Data"):
    st.dataframe(df, use_container_width=True)

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Automatically detect categorical columns
filter_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Create multiselect filters
for col in filter_cols:
    options = df[col].dropna().unique().tolist()
    selected = st.sidebar.multiselect(f"{col}:", options, default=options)
    df = df[df[col].isin(selected)]

# Main metrics
st.subheader("📈 Summary Metrics")
st.write(f"✅ Filtered Rows: {len(df)}")

# Chart Options
if len(numeric_cols) >= 2:
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox("X-Axis", numeric_cols)
    with col2:
        y_axis = st.selectbox("Y-Axis", numeric_cols, index=1)

    chart_type = st.radio("Select Chart Type", ["Scatter", "Line", "Bar"])

    st.subheader(f"{chart_type} Chart: {x_axis} vs {y_axis}")
    fig, ax = plt.subplots()

    if chart_type == "Scatter":
        ax.scatter(df[x_axis], df[y_axis], alpha=0.7)
    elif chart_type == "Line":
        ax.plot(df[x_axis], df[y_axis])
    elif chart_type == "Bar":
        ax.bar(df[x_axis], df[y_axis])

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    st.pyplot(fig)
else:
    st.warning("Not enough numeric columns found for charting.")
