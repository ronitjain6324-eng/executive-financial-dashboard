import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG (MUST BE FIRST) =================
st.set_page_config(
    page_title="Executive Financial Performance Dashboard",
    layout="wide"
)

# ================= TITLE =================
st.title("📊 Executive Financial Performance Dashboard")
st.caption("Power BI–style financial insights with dynamic business logic")

# ================= BASE DATA =================
df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [210000, 225000, 240000, 260000, 280000, 300000],
    "COGS": [130000, 138000, 145000, 155000, 165000, 175000],
    "Operating Expenses": [45000, 47000, 48000, 50000, 52000, 54000]
})

# ================= DERIVED METRICS =================
df["Gross Profit"] = df["Revenue"] - df["COGS"]
df["Gross Margin %"] = (df["Gross Profit"] / df["Revenue"]) * 100
df["Net Profit"] = df["Gross Profit"] - df["Operating Expenses"]
df["Net Margin %"] = (df["Net Profit"] / df["Revenue"]) * 100

# ================= SIDEBAR FILTERS (POWER BI SLICERS) =================
st.sidebar.header("🔎 Filters")

selected_months = st.sidebar.multiselect(
    "Select Month(s)",
    options=df["Month"].unique(),
    default=df["Month"].unique()
)

filtered_df = df[df["Month"].isin(selected_months)]

# ================= DYNAMIC KPI CALCULATIONS =================
total_revenue = filtered_df["Revenue"].sum()
total_cogs = filtered_df["COGS"].sum()
gross_profit = filtered_df["Gross Profit"].sum()
net_profit = filtered_df["Net Profit"].sum()

gross_margin = (gross_profit / total_revenue) * 100 if total_revenue else 0
net_margin = (net_profit / total_revenue) * 100 if total_revenue else 0

# ================= KPI ROW (EXECUTIVE STRIP) =================
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Revenue", f"₹{total_revenue:,.0f}")
col2.metric("COGS", f"₹{total_cogs:,.0f}")
col3.metric("Gross Profit", f"₹{gross_profit:,.0f}")
col4.metric("Gross Margin %", f"{gross_margin:.2f}%")
col5.metric("Net Profit", f"₹{net_profit:,.0f}")
col6.metric("Net Margin %", f"{net_margin:.2f}%")

st.caption(
    f"📊 Metrics calculated for {len(filtered_df)} month(s): "
    f"{', '.join(selected_months) if selected_months else 'None'}"
)

st.divider()

# ================= ROW 1: PROFIT TRENDS =================
c1, c2 = st.columns(2)

with c1:
    st.subheader("Operating Profit Over Time")
    fig1 = px.bar(
        filtered_df,
        x="Month",
        y="Net Profit",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Net Profit Trend")
    fig2 = px.line(
        filtered_df,
        x="Month",
        y="Net Profit",
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ================= ROW 2: MARGIN & EXPENSES =================
c3, c4 = st.columns(2)

with c3:
    st.subheader("Gross Margin % Trend")
    fig3 = px.line(
        filtered_df,
        x="Month",
        y="Gross Margin %",
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Operating Expense Breakdown (G&A)")
    expense_df = pd.DataFrame({
        "Category": ["Salaries", "Marketing", "Technology", "Rent", "Utilities"],
        "Amount": [120000, 60000, 45000, 30000, 20000]
    })
    fig4 = px.bar(
        expense_df,
        x="Amount",
        y="Category",
        orientation="h"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ================= EXECUTIVE SUMMARY =================
st.subheader("📌 Executive Summary")

st.write(
    f"""
    The dashboard reflects financial performance for the selected period.
    Revenue growth remains consistent across months while gross margins stay stable,
    indicating effective cost control at the production level.
    Net profitability improves as operating expenses scale proportionally with revenue,
    suggesting healthy and sustainable business growth.
    """
)
