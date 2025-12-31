import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Business Financial Performance Simulator",
    layout="wide"
)

st.title("📊 Business Financial Performance Simulator")
st.caption("Input-driven financial modeling for early-stage businesses")

# ================= SIDEBAR: BUSINESS INPUTS =================
st.sidebar.header("🧮 Business Inputs")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

selling_price = st.sidebar.number_input(
    "Selling Price per Unit (₹)",
    min_value=1,
    value=1000
)

cost_per_unit = st.sidebar.number_input(
    "Cost per Unit (₹)",
    min_value=0,
    value=600
)

fixed_expenses = st.sidebar.number_input(
    "Fixed Monthly Expenses (₹)",
    min_value=0,
    value=20000
)

st.sidebar.subheader("📦 Units Sold per Month")

units_sold = {}
for month in months:
    units_sold[month] = st.sidebar.number_input(
        f"{month} Units Sold",
        min_value=0,
        value=50
    )

# ================= FINANCIAL MODEL =================
data = []

for month in months:
    revenue = units_sold[month] * selling_price
    cogs = units_sold[month] * cost_per_unit
    gross_profit = revenue - cogs
    net_profit = gross_profit - fixed_expenses

    gross_margin = (gross_profit / revenue) * 100 if revenue else 0
    net_margin = (net_profit / revenue) * 100 if revenue else 0

    data.append([
        month,
        units_sold[month],
        revenue,
        cogs,
        gross_profit,
        net_profit,
        gross_margin,
        net_margin
    ])

df = pd.DataFrame(
    data,
    columns=[
        "Month",
        "Units Sold",
        "Revenue",
        "COGS",
        "Gross Profit",
        "Net Profit",
        "Gross Margin %",
        "Net Margin %"
    ]
)

# ================= KPI AGGREGATION =================
total_revenue = df["Revenue"].sum()
total_cogs = df["COGS"].sum()
total_gross_profit = df["Gross Profit"].sum()
total_net_profit = df["Net Profit"].sum()

overall_gross_margin = (total_gross_profit / total_revenue) * 100 if total_revenue else 0
overall_net_margin = (total_net_profit / total_revenue) * 100 if total_revenue else 0

# ================= KPI ROW =================
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total COGS", f"₹{total_cogs:,.0f}")
k3.metric("Gross Profit", f"₹{total_gross_profit:,.0f}")
k4.metric("Gross Margin %", f"{overall_gross_margin:.2f}%")
k5.metric("Net Profit", f"₹{total_net_profit:,.0f}")
k6.metric("Net Margin %", f"{overall_net_margin:.2f}%")

st.divider()

# ================= CHARTS =================
c1, c2 = st.columns(2)

with c1:
    st.subheader("Revenue vs Net Profit")
    fig1 = px.bar(
        df,
        x="Month",
        y=["Revenue", "Net Profit"],
        barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Profitability Trend")
    fig2 = px.line(
        df,
        x="Month",
        y=["Gross Margin %", "Net Margin %"],
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ================= UNIT ECONOMICS =================
st.subheader("📈 Unit Economics Insight")

st.write(
    f"""
    - Selling Price per Unit: ₹{selling_price}
    - Cost per Unit: ₹{cost_per_unit}
    - Contribution Margin per Unit: ₹{selling_price - cost_per_unit}
    - Break-even Units per Month: 
      {int(fixed_expenses / (selling_price - cost_per_unit)) if selling_price > cost_per_unit else "Not achievable"}
    """
)

# ================= EXECUTIVE SUMMARY =================
st.subheader("📌 Business Insight Summary")

st.write(
    """
    This simulator helps founders understand how sales volume, pricing, and cost structure
    impact profitability. By adjusting units sold and costs, decision-makers can evaluate
    scalability, pricing strategies, and break-even feasibility before committing capital.
    """
)
