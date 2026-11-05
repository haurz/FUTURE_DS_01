import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Load Data
df = pd.read_csv("data/samplesuperstore.csv", encoding="latin1")

# 2. Data Cleaning & Parsing
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100

# 3. Calculate Core Business KPIs
total_revenue = df["Sales"].sum()
total_profit = df["Profit"].sum()
avg_margin = (total_profit / total_revenue) * 100
total_orders = df["Order ID"].nunique()
aov = total_revenue / total_orders

print(f"--- BUSINESS KPI SUMMARY ---")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit:  ${total_profit:,.2f}")
print(f"Net Margin:    {avg_margin:.2f}%")
print(f"Total Orders:  {total_orders:,}")
print(f"Avg Order Val: ${aov:,.2f}")

# 4. Generate Visualizations
# Chart A: Monthly Revenue & Profit Trend
monthly_df = df.groupby("YearMonth")[["Sales", "Profit"]].sum().reset_index()
fig_trend = px.line(
    monthly_df, 
    x="YearMonth", 
    y=["Sales", "Profit"],
    title="Monthly Revenue & Profit Growth Trends",
    labels={"value": "USD ($)", "YearMonth": "Month"},
    template="plotly_dark",
    color_discrete_sequence=["#10B981", "#3B82F6"]
)

# Chart B: Category & Sub-Category Performance
cat_df = df.groupby(["Category", "Sub-Category"])[["Sales", "Profit"]].sum().reset_index()
fig_cat = px.bar(
    cat_df, 
    x="Sub-Category", 
    y="Sales", 
    color="Category",
    title="Revenue Distribution by Sub-Category",
    template="plotly_dark"
)

# Chart C: Regional Profit Margin Breakdown
region_df = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
region_df["Margin %"] = (region_df["Profit"] / region_df["Sales"]) * 100
fig_region = px.bar(
    region_df, 
    x="Region", 
    y="Margin %", 
    color="Margin %",
    title="Profitability Margin (%) across Geographic Regions",
    template="plotly_dark",
    color_continuous_scale="Viridis"
)

# Save Interactive HTML Dashboard Report
with open("dashboard/sales_report.html", "w") as f:
    f.write(fig_trend.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_cat.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig_region.to_html(full_html=False, include_plotlyjs='cdn'))

print("\nDashboard saved successfully to dashboard/sales_report.html")