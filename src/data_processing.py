from pathlib import Path
import pandas as pd


def load_data(file_path):
    """Load the Superstore dataset."""
    return pd.read_excel(file_path)


def calculate_kpis(data):
    """Calculate key business KPIs."""
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    total_quantity = data["Quantity"].sum()
    total_orders = data["Order ID"].nunique()
    total_customers = data["Customer ID"].nunique()

    profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0 else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0 else 0
    )

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Quantity": total_quantity,
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Profit Margin (%)": profit_margin,
        "Average Order Value": average_order_value
    }


def category_performance(data):
    """Generate category-level analysis."""
    result = (
        data.groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Sales", ascending=False)


def region_performance(data):
    """Generate region-level analysis."""
    result = (
        data.groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Sales", ascending=False)


def monthly_performance(data):
    """Generate monthly performance analysis."""
    result = (
        data.groupby(data["Order Date"].dt.to_period("M"))
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Order Date"] = result["Order Date"].astype(str)

    return result


def subcategory_performance(data):
    """Generate sub-category analysis."""
    result = (
        data.groupby("Sub-Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Profit", ascending=False)


def discount_performance(data):
    """Generate discount profitability analysis."""
    result = (
        data.groupby("Discount")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Discount")


def product_performance(data):
    """Generate product-level analysis."""
    result = (
        data.groupby(["Product ID", "Product Name"])
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order ID", "nunique"),
            Avg_Discount=("Discount", "mean")
        )
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Profit", ascending=False)


def customer_performance(data):
    """Generate customer-level analysis."""
    result = (
        data.groupby(["Customer ID", "Customer Name"])
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum"),
            Avg_Discount=("Discount", "mean")
        )
    )

    result["Profit Margin (%)"] = (
        result["Profit"] / result["Sales"] * 100
    ).round(2)

    return result.sort_values("Sales", ascending=False)


def get_top_products(data, n=10):
    """Return the most profitable products."""
    return product_performance(data).head(n)


def get_loss_making_products(data, n=10):
    """Return the most loss-making products."""
    result = product_performance(data)

    return (
        result[result["Profit"] < 0]
        .sort_values("Profit")
        .head(n)
    )


def get_top_customers_by_profit(data, n=10):
    """Return customers ranked by profit."""
    return (
        customer_performance(data)
        .sort_values("Profit", ascending=False)
        .head(n)
    )


def export_analysis(result, file_path):
    """Export an analysis DataFrame to CSV."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(file_path, index=False)