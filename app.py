import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Business Decision Intelligence Simulator",
    layout="wide"
)

# ================= STYLING =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #020617);
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #f8fafc;
}
p, label {
    color: #cbd5f5;
}
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 18px;
    border-left: 6px solid #22c55e;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("## 🧠 Business Decision Intelligence Simulator")
st.caption("Interactive financial modeling built on real business principles")

# ================= SIDEBAR INPUTS =================
st.sidebar.header("📥 Business Configuration")

price = st.sidebar.number_input("Selling Price per Unit (₹)", 1, 100000, 50)
cost = st.sidebar.number_input("Cost per Unit (₹)", 0, 100000, 20)
fixed_cost = st.sidebar.number_input("Fixed Monthly Expenses (₹)", 0, 1000000, 20000)

months = st.sidebar.slider("Business Timeline (Months)", 3, 24, 12)
start_units = st.sidebar.number_input("Units Sold in Month 1", 0, 100000, 70)
growth = st.sidebar.slider("Monthly Sales Growth (%)", -30, 100, 10)

price_change = st.sidebar.slider("Price Change Scenario (%)", -30, 30, 0)
adj_price = price * (1 + price_change / 100)

# ================= DATA GENERATION =================
units = []
current_units = start_units
for _ in range(months):
    units.append(max(0, current_units))
    current_units *= (1 + growth / 100)

df = pd.DataFrame({
    "Month": [f"Month {i+1}" for i in range(months)],
    "Units Sold": units
})

df["Revenue"] = df["Units Sold"] * adj_price
df["COGS"] = df["Units Sold"] * cost
df["Contribution"] = df["Revenue"] - df["COGS"]
df["Net Profit"] = df["Contribution"] - fixed_cost

df["Gross Margin %"] = np.where(df["Revenue"] > 0, (df["Contribution"] / df["Revenue"]) * 100, 0)
df["Net Margin %"] = np.where(df["Revenue"] > 0, (df["Net Profit"] / df["Revenue"]) * 100, 0)

# ================= KPI SUMMARY =================
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Revenue", f"₹{df['Revenue'].sum():,.0f}")
k2.metric("Total Contribution", f"₹{df['Contribution'].sum():,.0f}")
k3.metric("Total Net Profit", f"₹{df['Net Profit'].sum():,.0f}")
k4.metric("Avg Gross Margin", f"{df['Gross Margin %'].mean():.1f}%")
k5.metric("Avg Net Margin", f"{df['Net Margin %'].mean():.1f}%")

st.divider()

# ================= UNIT ECONOMICS =================
st.subheader("📦 Unit Economics")

contribution_per_unit = adj_price - cost

u1, u2, u3 = st.columns(3)
u1.metric("Contribution per Unit", f"₹{contribution_per_unit:.0f}")
u2.metric(
    "Break-even Units / Month",
    f"{fixed_cost / contribution_per_unit:.0f}" if contribution_per_unit > 0 else "❌"
)
u3.metric(
    "Unit Economics Status",
    "Healthy ✅" if contribution_per_unit > 0 else "Broken ❌"
)

st.divider()

# ================= BUSINESS HEALTH SCORE =================
st.subheader("❤️ Business Health Score")

score = 0
if contribution_per_unit > 0:
    score += 30
if df["Net Profit"].mean() > 0:
    score += 30
if growth > 0:
    score += 20
if fixed_cost < df["Revenue"].mean():
    score += 20

st.progress(score / 100)
st.write(f"**Health Score: {score}/100**")

if score >= 80:
    st.success("Strong fundamentals — ready to scale.")
elif score >= 50:
    st.warning("Moderate health — improve efficiency.")
else:
    st.error("Weak fundamentals — fix core issues first.")

st.divider()

# ================= DECISION SIGNAL =================
st.subheader("🚦 Executive Decision Signal")

if contribution_per_unit <= 0:
    st.error("❌ Stop: Unit economics are broken.")
elif df["Net Profit"].mean() < 0:
    st.warning("⚠️ Caution: Growth without profitability.")
else:
    st.success("✅ Go: Business model is scalable.")

st.divider()

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

# ================= EXPORT SECTION =================
st.subheader("📤 Export Business Data")

# Full dataset
st.download_button(
    label="⬇️ Download Full Financial Model (CSV)",
    data=df.to_csv(index=False),
    file_name="business_financial_model.csv",
    mime="text/csv"
)

# Executive summary
summary_df = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Contribution",
        "Total Net Profit",
        "Average Gross Margin %",
        "Average Net Margin %"
    ],
    "Value": [
        df["Revenue"].sum(),
        df["Contribution"].sum(),
        df["Net Profit"].sum(),
        round(df["Gross Margin %"].mean(), 2),
        round(df["Net Margin %"].mean(), 2)
    ]
})

st.download_button(
    label="⬇️ Download Executive Summary (CSV)",
    data=summary_df.to_csv(index=False),
    file_name="executive_summary.csv",
    mime="text/csv"
)

st.caption("Designed for founders, analysts & decision-makers.")
