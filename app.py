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
    background: rgba(255,255,255,0.08);
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
st.caption("A Power BI–style system that explains *what*, *why*, and *what to do next*")

# ================= SIDEBAR INPUTS =================
st.sidebar.header("📥 Business Inputs")

price = st.sidebar.number_input("Selling Price per Unit (₹)", 1, 100000, 50)
cost = st.sidebar.number_input("Cost per Unit (₹)", 0, 100000, 20)
fixed_cost = st.sidebar.number_input("Fixed Monthly Expenses (₹)", 0, 1000000, 20000)

months = st.sidebar.slider("Business Timeline (Months)", 3, 24, 12)
start_units = st.sidebar.number_input("Units Sold (Month 1)", 0, 100000, 70)
growth = st.sidebar.slider("Monthly Sales Growth (%)", -30, 100, 10)

price_change = st.sidebar.slider("Price Change Scenario (%)", -30, 30, 0)
adj_price = price * (1 + price_change / 100)

# ================= TARGETS =================
st.sidebar.header("🎯 Business Targets")

target_revenue = st.sidebar.number_input("Target Monthly Revenue (₹)", 0, 1000000, 100000)
target_net_margin = st.sidebar.slider("Target Net Margin (%)", 0, 50, 20)

# ================= BENCHMARKS =================
INDUSTRY_GROSS_MARGIN = 40
INDUSTRY_NET_MARGIN = 15

# ================= DATA =================
units = []
current = start_units
for _ in range(months):
    units.append(max(0, current))
    current *= (1 + growth / 100)

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

# ================= STORY MODE =================
st.subheader("🩺 1. Business Health Overview")

avg_net_profit = df["Net Profit"].mean()
contribution_per_unit = adj_price - cost

health_score = 0
health_score += 30 if contribution_per_unit > 0 else 0
health_score += 30 if avg_net_profit > 0 else 0
health_score += 20 if growth > 0 else 0
health_score += 20 if fixed_cost < df["Revenue"].mean() else 0

st.progress(health_score / 100)
st.write(f"**Health Score: {health_score}/100**")

if health_score >= 80:
    st.success("Business fundamentals are strong.")
elif health_score >= 50:
    st.warning("Business is survivable but needs optimization.")
else:
    st.error("Core business model is at risk.")

# ================= UNIT ECONOMICS =================
st.subheader("📦 2. Unit Economics")

u1, u2, u3 = st.columns(3)
u1.metric("Contribution / Unit", f"₹{contribution_per_unit:.0f}")
u2.metric("Break-even Units / Month",
          f"{fixed_cost / contribution_per_unit:.0f}" if contribution_per_unit > 0 else "❌")
u3.metric("Unit Economics Status",
          "Healthy ✅" if contribution_per_unit > 0 else "Broken ❌")

# ================= TARGET TRACKING =================
st.subheader("🎯 3. Target vs Actual")

actual_avg_revenue = df["Revenue"].mean()
actual_net_margin = df["Net Margin %"].mean()

t1, t2 = st.columns(2)
t1.metric("Avg Revenue vs Target",
          f"₹{actual_avg_revenue:,.0f}",
          delta=f"{actual_avg_revenue - target_revenue:,.0f}")

t2.metric("Net Margin vs Target",
          f"{actual_net_margin:.1f}%",
          delta=f"{actual_net_margin - target_net_margin:.1f}%")

# ================= BENCHMARK COMPARISON =================
st.subheader("📊 4. Industry Benchmark Comparison")

b1, b2 = st.columns(2)
b1.metric("Gross Margin vs Industry",
          f"{df['Gross Margin %'].mean():.1f}%",
          delta=f"{df['Gross Margin %'].mean() - INDUSTRY_GROSS_MARGIN:.1f}%")

b2.metric("Net Margin vs Industry",
          f"{df['Net Margin %'].mean():.1f}%",
          delta=f"{df['Net Margin %'].mean() - INDUSTRY_NET_MARGIN:.1f}%")

# ================= CHARTS =================
st.subheader("📈 5. Financial Trends")

c1, c2 = st.columns(2)

with c1:
    fig1 = px.bar(df, x="Month", y=["Revenue", "Net Profit"],
                  title="Revenue vs Net Profit", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.line(df, x="Month",
                   y=["Gross Margin %", "Net Margin %"],
                   markers=True,
                   title="Margin Trend")
    st.plotly_chart(fig2, use_container_width=True)

# ================= SMART RECOMMENDATIONS =================
st.subheader("🧠 6. Executive Recommendations")

if contribution_per_unit <= 0:
    st.error("Fix pricing or reduce variable costs — unit economics are broken.")
elif avg_net_profit < 0:
    st.warning("Reduce fixed costs or delay scaling until profitable.")
elif actual_net_margin < target_net_margin:
    st.info("Focus on margin expansion — pricing or cost optimization needed.")
else:
    st.success("Business is on track. Consider scaling or adding new products.")

# ================= EXPORT =================
st.subheader("📤 Export Insights")

st.download_button(
    "⬇️ Download Full Financial Model (CSV)",
    df.to_csv(index=False),
    "business_financial_model.csv",
    "text/csv"
)

summary = pd.DataFrame({
    "Metric": [
        "Health Score",
        "Avg Revenue",
        "Avg Net Profit",
        "Avg Gross Margin %",
        "Avg Net Margin %"
    ],
    "Value": [
        health_score,
        actual_avg_revenue,
        avg_net_profit,
        df["Gross Margin %"].mean(),
        df["Net Margin %"].mean()
    ]
})

st.download_button(
    "⬇️ Download Executive Summary (CSV)",
    summary.to_csv(index=False),
    "executive_summary.csv",
    "text/csv"
)

st.caption("This system converts numbers into decisions — like real BI tools.")
