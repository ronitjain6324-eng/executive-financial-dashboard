import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Business Financial Performance Simulator",
    layout="wide"
)

# ================= CUSTOM STYLING =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
p, label {
    color: #d1d5db;
}
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 12px;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b132b, #1c2541);
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown(
    "<h1>📊 Business Financial Performance Simulator</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p>Interactive, input-driven financial modeling for founders & early-stage businesses</p>",
    unsafe_allow_html=True
)

# ================= SIDEBAR INPUTS =================
st.sidebar.header("🧮 Business Inputs")

selling_price = st.sidebar.number_input(
    "Selling Price per Unit (₹)", min_value=1, value=50
)

cost_per_unit = st.sidebar.number_input(
    "Cost per Unit (₹)", min_value=0, value=20
)

fixed_expenses = st.sidebar.number_input(
    "Fixed Monthly Expenses (₹)", min_value=0, value=20000
)

st.sidebar.subheader("📦 Units Sold per Month")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
units_sold = {}

for m in months:
    units_sold[m] = st.sidebar.number_input(
        f"{m} Units Sold", min_value=0, value=70 if m == "Jan" else 50
    )

# ================= SCENARIO TESTING =================
st.sidebar.subheader("🔁 What-If Scenario")

price_change = st.sidebar.slider(
    "Change Selling Price (%)", -30, 30, 0
)

adjusted_price = selling_price * (1 + price_change / 100)

# ================= FINANCIAL MODEL =================
rows = []

for m in months:
    revenue = units_sold[m] * adjusted_price
    cogs = units_sold[m] * cost_per_unit
    gross_profit = revenue - cogs
    net_profit = gross_profit - fixed_expenses

    gross_margin = (gross_profit / revenue) * 100 if revenue else 0
    net_margin = (net_profit / revenue) * 100 if revenue else 0

    rows.append([
        m,
        units_sold[m],
        revenue,
        cogs,
        gross_profit,
        net_profit,
        gross_margin,
        net_margin
    ])

df = pd.DataFrame(rows, columns=[
    "Month", "Units Sold", "Revenue", "COGS",
    "Gross Profit", "Net Profit",
    "Gross Margin %", "Net Margin %"
])

# ================= KPI CALCULATIONS =================
total_revenue = df["Revenue"].sum()
total_cogs = df["COGS"].sum()
total_gross_profit = df["Gross Profit"].sum()
total_net_profit = df["Net Profit"].sum()

gross_margin_total = (total_gross_profit / total_revenue) * 100 if total_revenue else 0
net_margin_total = (total_net_profit / total_revenue) * 100 if total_revenue else 0

# ================= KPI STRIP =================
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total COGS", f"₹{total_cogs:,.0f}")
k3.metric("Gross Profit", f"₹{total_gross_profit:,.0f}")
k4.metric("Gross Margin %", f"{gross_margin_total:.2f}%")
k5.metric("Net Profit", f"₹{total_net_profit:,.0f}")
k6.metric("Net Margin %", f"{net_margin_total:.2f}%")

st.divider()

# ================= BUSINESS STATUS =================
st.subheader("📍 Business Health Indicator")

if total_net_profit > 0:
    st.success("🟢 Business is PROFITABLE and financially sustainable.")
elif total_net_profit == 0:
    st.warning("🟡 Business is at BREAK-EVEN. Minor changes can impact profitability.")
else:
    st.error("🔴 Business is LOSS-MAKING. Review pricing, volume, or expenses.")

st.divider()

# ================= CHARTS =================
c1, c2 = st.columns(2)

with c1:
    st.subheader("Revenue vs Net Profit")
    fig1 = px.bar(
        df,
        x="Month",
        y=["Revenue", "Net Profit"],
        barmode="group",
        color_discrete_sequence=["#4cc9f0", "#f72585"]
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Profitability Trend")
    fig2 = px.line(
        df,
        x="Month",
        y=["Gross Margin %", "Net Margin %"],
        markers=True,
        color_discrete_sequence=["#90dbf4", "#f77f00"]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ================= BREAK-EVEN =================
st.subheader("📊 Break-Even Analysis")

if selling_price > cost_per_unit:
    breakeven_units = fixed_expenses / (selling_price - cost_per_unit)
    st.metric("Break-Even Units / Month", f"{breakeven_units:.0f}")

    fig3 = px.bar(
        df,
        x="Month",
        y="Units Sold",
        color_discrete_sequence=["#80ffdb"]
    )
    fig3.add_hline(
        y=breakeven_units,
        line_dash="dash",
        annotation_text="Break-Even Level"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.error("Selling price must exceed cost per unit to break even.")

# ================= EXECUTIVE INSIGHTS =================
st.subheader("🧠 Executive Insights")

if net_margin_total < 0:
    st.write(
        "- Net margins are negative due to high fixed expenses.\n"
        "- Increasing sales volume or pricing is required to reach sustainability."
    )
elif net_margin_total < 10:
    st.write(
        "- Margins are positive but thin.\n"
        "- Cost control and pricing discipline are critical at this stage."
    )
else:
    st.write(
        "- Healthy margins indicate strong unit economics.\n"
        "- Business model appears scalable under current assumptions."
    )

st.caption(f"Scenario price applied: ₹{adjusted_price:.2f} per unit")
