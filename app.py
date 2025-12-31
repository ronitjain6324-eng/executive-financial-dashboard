import streamlit as st
import pandas as pd
import plotly.express as px

# MUST be first Streamlit command
st.set_page_config(page_title="Executive Financial Dashboard", layout="wide")

st.title("📊 Executive Financial Performance Dashboard")
st.write("✅ App loaded successfully")

# Data
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [210000, 225000, 240000, 260000, 280000, 300000],
    "COGS": [130000, 138000, 145000, 155000, 165000, 175000],
    "Operating_Expenses": [45000, 47000, 48000, 50000, 52000, 54000]
})

# Calculations
df["Gross_Profit"] = df["Revenue"] - df["COGS"]
df["Net_Profit"] = df["Gross_Profit"] - df["Operating_Expenses"]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"₹{df['Revenue'].sum():,.0f}")
col2.metric("Gross Profit", f"₹{df['Gross_Profit'].sum():,.0f}")
col3.metric("Net Profit", f"₹{df['Net_Profit'].sum():,.0f}")

st.divider()

# Chart
st.plotly_chart(
    px.line(df, x="Month", y="Revenue", markers=True),
    use_container_width=True
)
 