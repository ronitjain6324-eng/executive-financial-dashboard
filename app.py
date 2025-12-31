import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Business Financial Intelligence Simulator",
    layout="wide"
)

# ================= MODERN STYLING =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #ffffff;
}
p, label {
    color: #d1d5db;
}
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 18px;
    border-left: 6px solid #4cc9f0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b132b, #1c2541);
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("## 🚀 Business Financial Intelligence Simulator")
st.markdown(
    "A **founder-first**, scenario-driven financial model inspired by modern BI tools"
)

# ================= SIDEBAR INPUTS =================
st.sidebar.header("📥 Business Configuration")

selling_price = st.sidebar.number_input("Selling Price per Unit (₹)", 1, 100000, 50)
cost_per_unit = st.sidebar.number_input("Cost per Unit (₹)", 0, 100000, 20)
fixed_expenses = st.sidebar.number_input("Fixed Monthly Expenses (₹)", 0, 1000000, 20000)

months_count = st.sidebar.slider("Business Timeline (Months)", 3, 24, 12)
starting_units = st.sidebar.number_input("Units Sold in Month 1", 0, 100000, 70)
growth_rate = st.sidebar.slider("Monthly Sales Growth (%)", -50, 100, 10)

price_scenario = st.sidebar.slider("Price Change Scenario (%)", -30, 30, 0)

adjusted_price = selling_price * (1 + price_scenario / 100)

# ================= DATA GENERATION =================
months = [f"Month {i+1}" for i in range(months_count)]
units = []

current_units = starting_units
for _ in months:
    units.append(max(0, current_units))
    current_units *= (1 + growth_rate / 100)

data = []

for m, u in zip(months, units):
    revenue = u * adjusted_price
    cogs = u * cost_per_unit
    gross_profit = revenue - cogs
    net_profit = gross_profit - fixed_expenses

    gross_margin = (gross_profit / revenue) * 100 if revenue else 0
    net_margin = (net_profit / revenue) * 100 if revenue else 0

    data.append([m, u, revenue, cogs, gross_profit, net_profit, gross_margin, net_margin])

df = pd.DataFrame(data, columns=[
    "Month", "Units Sold", "Revenue", "COGS",
    "Gross Profit", "Net Profit", "Gross Margin %", "Net Margin %"
])

# ================= KPIs =================
total_revenue = df["Revenue"].sum()
total_cogs = df["COGS"].sum()
total_net_profit = df["Net Profit"].sum()
gross_margin_avg = df["Gross Margin %"].mean()
net_margin_avg = df["Net Margin %"].mean()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total COGS", f"₹{total_cogs:,.0f}")
k3.metric("Net Profit", f"₹{total_net_profit:,.0f}")
k4.metric("Avg Gross Margin", f"{gross_margin_avg:.2f}%")
k5.metric("Avg Net Margin", f"{net_margin_avg:.2f}%")

st.divider()

# ================= MOMENTUM INDICATOR =================
st.subheader("📈 Business Momentum")

trend = df["Net Profit"].iloc[-1] - df["Net Profit"].iloc[0]

if trend > 0:
    st.success("🟢 Positive momentum — business is scaling.")
elif trend == 0:
    st.warning("🟡 Flat momentum — growth levers needed.")
else:
    st.error("🔴 Negative momentum — cost or pricing issues detected.")

# ================= CHARTS =================
c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(
        df,
        x="Month",
        y=["Revenue", "Net Profit"],
        title="Revenue vs Net Profit",
        barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.line(
        df,
        x="Month",
        y=["Gross Margin %", "Net Margin %"],
        markers=True,
        title="Profitability Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ================= BREAK-EVEN =================
st.subheader("🎯 Break-Even Intelligence")

if selling_price > cost_per_unit:
    breakeven_units = fixed_expenses / (selling_price - cost_per_unit)
    st.metric("Break-Even Units / Month", f"{breakeven_units:.0f}")
else:
    st.error("Selling price must exceed unit cost to break even.")

# ================= EXECUTIVE INSIGHTS =================
st.subheader("🧠 Executive Insights")

if net_margin_avg < 0:
    st.write("• Business model is loss-making under current assumptions.")
    st.write("• Consider pricing, volume growth, or expense restructuring.")
elif net_margin_avg < 15:
    st.write("• Margins are thin — operational efficiency is critical.")
else:
    st.write("• Healthy margins suggest scalable unit economics.")

st.caption("Designed for modern founders, analysts & decision-makers")
