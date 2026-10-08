
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# DATABASE PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "sales_intelligence.db"


# =========================================================
# DATABASE FUNCTION
# =========================================================

@st.cache_data
def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# =========================================================
# LOAD DATA
# =========================================================

sales_df = run_query("""
SELECT *
FROM sales
""")


# =========================================================
# PAGE TITLE
# =========================================================

st.title("📊 Sales Intelligence Dashboard")

st.markdown(
    "Interactive analysis of sales, profit, customers, products, "
    "regions and business performance."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

category_options = ["All"] + sorted(
    sales_df["Category"].dropna().unique().tolist()
)

region_options = ["All"] + sorted(
    sales_df["Region"].dropna().unique().tolist()
)

segment_options = ["All"] + sorted(
    sales_df["Segment"].dropna().unique().tolist()
)

ship_mode_options = ["All"] + sorted(
    sales_df["Ship Mode"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Category",
    category_options
)

selected_region = st.sidebar.selectbox(
    "Region",
    region_options
)

selected_segment = st.sidebar.selectbox(
    "Segment",
    segment_options
)

selected_ship_mode = st.sidebar.selectbox(
    "Ship Mode",
    ship_mode_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = sales_df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_segment != "All":
    filtered_df = filtered_df[
        filtered_df["Segment"] == selected_segment
    ]

if selected_ship_mode != "All":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_ship_mode
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

average_order_value = (
    total_sales / total_orders
    if total_orders != 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📌 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

with kpi2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

with kpi3:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

with kpi4:
    st.metric(
        "Orders",
        f"{total_orders:,}"
    )

with kpi5:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )


# =========================================================
# SECONDARY METRICS
# =========================================================

st.subheader("📈 Additional Metrics")

m1, m2 = st.columns(2)

with m1:
    st.metric(
        "Total Quantity",
        f"{total_quantity:,}"
    )

with m2:
    st.metric(
        "Average Order Value",
        f"${average_order_value:,.2f}"
    )


# =========================================================
# DATE PREPARATION
# =========================================================

filtered_df["Order Date"] = pd.to_datetime(
    filtered_df["Order Date"],
    errors="coerce"
)

filtered_df["Year Month"] = (
    filtered_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)


# =========================================================
# MONTHLY ANALYSIS
# =========================================================

monthly_data = (
    filtered_df
    .groupby("Year Month", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

monthly_data["Year Month"] = pd.to_datetime(
    monthly_data["Year Month"]
)

monthly_data = monthly_data.sort_values(
    "Year Month"
)


# =========================================================
# MONTHLY SALES TREND
# =========================================================

st.subheader("📅 Monthly Sales Trend")

fig_monthly_sales = px.line(
    monthly_data,
    x="Year Month",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

fig_monthly_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly_sales,
    width="stretch"
)


# =========================================================
# CATEGORY & REGION
# =========================================================

col1, col2 = st.columns(2)

with col1:

    category_data = (
        filtered_df
        .groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    fig_category = px.bar(
        category_data,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        width="stretch"
    )


with col2:

    region_data = (
        filtered_df
        .groupby("Region", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    fig_region = px.bar(
        region_data,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig_region,
        width="stretch"
    )


# =========================================================
# PROFIT ANALYSIS
# =========================================================

st.subheader("💰 Profit Analysis")

profit_data = (
    filtered_df
    .groupby("Sub-Category", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Profit", ascending=False)
)

fig_profit = px.bar(
    profit_data,
    x="Sub-Category",
    y="Profit",
    title="Profit by Sub-Category"
)

st.plotly_chart(
    fig_profit,
    width="stretch"
)


# =========================================================
# TOP PRODUCTS
# =========================================================

st.subheader("🏆 Top Products by Profit")

product_data = (
    filtered_df
    .groupby(
        ["Product ID", "Product Name"],
        as_index=False
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values(
        "Profit",
        ascending=False
    )
    .head(10)
)

fig_products = px.bar(
    product_data.sort_values("Profit"),
    x="Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Profit"
)

st.plotly_chart(
    fig_products,
    width="stretch"
)


# =========================================================
# DATA TABLE
# =========================================================

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)


# =========================================================
# DOWNLOAD
# =========================================================

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.subheader("💡 Business Insights")

if not filtered_df.empty:

    best_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    best_region = (
        filtered_df
        .groupby("Region")["Profit"]
        .sum()
        .idxmax()
    )

    best_product_row = (
        filtered_df
        .groupby("Product Name")["Profit"]
        .sum()
        .idxmax()
    )

    worst_product_row = (
        filtered_df
        .groupby("Product Name")["Profit"]
        .sum()
        .idxmin()
    )

    st.write(
        f"• **Most profitable category:** {best_category}"
    )

    st.write(
        f"• **Most profitable region:** {best_region}"
    )

    st.write(
        f"• **Most profitable product:** {best_product_row}"
    )

    st.write(
        f"• **Biggest loss-making product:** {worst_product_row}"
    )

else:

    st.warning(
        "No data available for the selected filters."
    )
