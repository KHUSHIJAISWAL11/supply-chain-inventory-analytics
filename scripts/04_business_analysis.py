import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CLEANED_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("STARTING BUSINESS ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

products = pd.read_csv(CLEANED_DIR / "products_cleaned.csv")
suppliers = pd.read_csv(CLEANED_DIR / "suppliers_cleaned.csv")
warehouses = pd.read_csv(CLEANED_DIR / "warehouses_cleaned.csv")
inventory = pd.read_csv(CLEANED_DIR / "inventory_cleaned.csv")
orders = pd.read_csv(CLEANED_DIR / "orders_cleaned.csv")
supplier_orders = pd.read_csv(
    CLEANED_DIR / "supplier_orders_cleaned.csv"
)

# Convert dates
inventory["inventory_date"] = pd.to_datetime(
    inventory["inventory_date"],
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders["promised_date"] = pd.to_datetime(
    orders["promised_date"],
    errors="coerce"
)

orders["delivery_date"] = pd.to_datetime(
    orders["delivery_date"],
    errors="coerce"
)

supplier_orders["order_date"] = pd.to_datetime(
    supplier_orders["order_date"],
    errors="coerce"
)

supplier_orders["expected_date"] = pd.to_datetime(
    supplier_orders["expected_date"],
    errors="coerce"
)

supplier_orders["received_date"] = pd.to_datetime(
    supplier_orders["received_date"],
    errors="coerce"
)

print("\nDatasets loaded successfully.")


# ============================================================
# 1. ORDER-LEVEL METRICS
# ============================================================

print("\n" + "=" * 70)
print("1. ORDER & REVENUE ANALYSIS")
print("=" * 70)

# Revenue
orders["revenue"] = (
    orders["quantity"] *
    orders["unit_price"]
)

# Product cost
orders = orders.merge(
    products[
        ["product_id", "product_name", "category",
         "unit_cost", "selling_price"]
    ],
    on="product_id",
    how="left"
)

# Cost and profit
orders["cost"] = (
    orders["quantity"] *
    orders["unit_cost"]
)

orders["gross_profit"] = (
    orders["revenue"] -
    orders["cost"]
)

orders["profit_margin"] = np.where(
    orders["revenue"] != 0,
    orders["gross_profit"] / orders["revenue"],
    0
)

# Delivery days
orders["delivery_days"] = np.where(
    orders["delivery_date"].notna(),
    (
        orders["delivery_date"] -
        orders["order_date"]
    ).dt.days,
    np.nan
)

# Delay days
orders["delay_days"] = np.where(
    orders["delivery_date"].notna() &
    orders["promised_date"].notna(),
    (
        orders["delivery_date"] -
        orders["promised_date"]
    ).dt.days,
    np.nan
)

# On-time delivery
orders["on_time"] = np.where(
    orders["delivery_date"].notna() &
    orders["promised_date"].notna(),
    orders["delivery_date"] <= orders["promised_date"],
    np.nan
)


# ============================================================
# OVERALL KPIs
# ============================================================

total_revenue = orders["revenue"].sum()

total_cost = orders["cost"].sum()

total_profit = orders["gross_profit"].sum()

overall_margin = (
    total_profit / total_revenue
    if total_revenue != 0
    else 0
)

total_orders = orders["order_id"].nunique()

delivered_orders = (
    orders["order_status"] == "Delivered"
).sum()

cancelled_orders = (
    orders["order_status"] == "Cancelled"
).sum()

returned_orders = (
    orders["order_status"] == "Returned"
).sum()


print("\nOverall KPIs")

print(f"Total Revenue       : ${total_revenue:,.2f}")
print(f"Total Cost          : ${total_cost:,.2f}")
print(f"Gross Profit        : ${total_profit:,.2f}")
print(f"Profit Margin       : {overall_margin:.2%}")
print(f"Total Orders        : {total_orders:,}")
print(f"Delivered Orders    : {delivered_orders:,}")
print(f"Cancelled Orders    : {cancelled_orders:,}")
print(f"Returned Orders     : {returned_orders:,}")


# ============================================================
# 2. ON-TIME DELIVERY
# ============================================================

print("\n" + "=" * 70)
print("2. DELIVERY PERFORMANCE")
print("=" * 70)

delivery_data = orders[
    orders["delivery_date"].notna() &
    orders["promised_date"].notna()
].copy()

if len(delivery_data) > 0:

    on_time_delivery = (
        delivery_data["on_time"].mean()
    )

    average_delivery_days = (
        delivery_data["delivery_days"].mean()
    )

    average_delay = (
        delivery_data["delay_days"]
        .clip(lower=0)
        .mean()
    )

    delayed_orders = (
        delivery_data["on_time"] == False
    ).sum()

else:

    on_time_delivery = 0
    average_delivery_days = 0
    average_delay = 0
    delayed_orders = 0


print(f"On-Time Delivery % : {on_time_delivery:.2%}")
print(f"Delayed Orders     : {delayed_orders:,}")
print(f"Avg Delivery Days  : {average_delivery_days:.2f}")
print(f"Avg Delay Days     : {average_delay:.2f}")


# ============================================================
# 3. SHIPPING METHOD PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("3. SHIPPING METHOD PERFORMANCE")
print("=" * 70)

shipping_analysis = (
    delivery_data
    .groupby("shipping_method")
    .agg(
        orders=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delay_days", lambda x: x.clip(lower=0).mean()),
        on_time_rate=("on_time", "mean")
    )
    .sort_values("on_time_rate", ascending=False)
)

print(shipping_analysis)

shipping_analysis.to_csv(
    OUTPUT_DIR / "shipping_method_performance.csv"
)


# ============================================================
# 4. PRODUCT PROFITABILITY
# ============================================================

print("\n" + "=" * 70)
print("4. PRODUCT PROFITABILITY")
print("=" * 70)

product_analysis = (
    orders
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        total_orders=("order_id", "count"),
        total_quantity=("quantity", "sum"),
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        gross_profit=("gross_profit", "sum")
    )
    .reset_index()
)

product_analysis["profit_margin"] = np.where(
    product_analysis["revenue"] != 0,
    product_analysis["gross_profit"] /
    product_analysis["revenue"],
    0
)

print("\nTop 10 Products by Revenue")

print(
    product_analysis
    .sort_values("revenue", ascending=False)
    .head(10)
    [
        [
            "product_name",
            "category",
            "revenue",
            "gross_profit",
            "profit_margin"
        ]
    ]
)

print("\nTop 10 Products by Gross Profit")

print(
    product_analysis
    .sort_values("gross_profit", ascending=False)
    .head(10)
    [
        [
            "product_name",
            "category",
            "revenue",
            "gross_profit",
            "profit_margin"
        ]
    ]
)

product_analysis.to_csv(
    OUTPUT_DIR / "product_profitability.csv",
    index=False
)


# ============================================================
# 5. CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("5. CATEGORY PERFORMANCE")
print("=" * 70)

category_analysis = (
    orders
    .groupby("category")
    .agg(
        orders=("order_id", "count"),
        quantity_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    )
    .reset_index()
)

category_analysis["profit_margin"] = (
    category_analysis["gross_profit"] /
    category_analysis["revenue"]
)

category_analysis = category_analysis.sort_values(
    "revenue",
    ascending=False
)

print(category_analysis)

category_analysis.to_csv(
    OUTPUT_DIR / "category_performance.csv",
    index=False
)


# ============================================================
# 6. INVENTORY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("6. INVENTORY PERFORMANCE")
print("=" * 70)

# Add product information
inventory = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "unit_cost",
            "reorder_level"
        ]
    ],
    on="product_id",
    how="left"
)

# Inventory value
inventory["inventory_value"] = (
    inventory["closing_stock"] *
    inventory["unit_cost"]
)

# Stockout flag
inventory["stockout"] = np.where(
    inventory["closing_stock"] <= 0,
    1,
    0
)

# Excess stock flag
inventory["excess_stock"] = np.where(
    inventory["closing_stock"] >
    inventory["reorder_level"] * 3,
    1,
    0
)

total_inventory_value = (
    inventory["inventory_value"].sum()
)

stockout_records = (
    inventory["stockout"].sum()
)

total_inventory_records = len(inventory)

stockout_rate = (
    stockout_records /
    total_inventory_records
)

excess_stock_records = (
    inventory["excess_stock"].sum()
)


print(f"Total Inventory Value : ${total_inventory_value:,.2f}")
print(f"Stockout Records      : {stockout_records:,}")
print(f"Stockout Rate         : {stockout_rate:.2%}")
print(f"Excess Stock Records  : {excess_stock_records:,}")


# ============================================================
# 7. WAREHOUSE PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("7. WAREHOUSE PERFORMANCE")
print("=" * 70)

warehouse_inventory = (
    inventory
    .groupby("warehouse_id")
    .agg(
        inventory_value=("inventory_value", "sum"),
        units_sold=("sold_quantity", "sum"),
        damaged_units=("damaged_quantity", "sum"),
        stockout_records=("stockout", "sum"),
        excess_stock_records=("excess_stock", "sum")
    )
    .reset_index()
)

warehouse_inventory["stockout_rate"] = (
    warehouse_inventory["stockout_records"] /
    total_inventory_records
)

warehouse_analysis = warehouse_inventory.merge(
    warehouses[
        [
            "warehouse_id",
            "warehouse_name",
            "city",
            "state",
            "region",
            "warehouse_capacity"
        ]
    ],
    on="warehouse_id",
    how="left"
)

warehouse_analysis = warehouse_analysis[
    [
        "warehouse_id",
        "warehouse_name",
        "city",
        "state",
        "region",
        "warehouse_capacity",
        "inventory_value",
        "units_sold",
        "damaged_units",
        "stockout_records",
        "excess_stock_records"
    ]
]

print("\nWarehouse Inventory Performance")

print(
    warehouse_analysis
    .sort_values(
        "inventory_value",
        ascending=False
    )
)

warehouse_analysis.to_csv(
    OUTPUT_DIR / "warehouse_performance.csv",
    index=False
)


# ============================================================
# 8. SUPPLIER PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("8. SUPPLIER PERFORMANCE")
print("=" * 70)

supplier_orders["fulfillment_rate"] = np.where(
    supplier_orders["ordered_quantity"] != 0,
    supplier_orders["received_quantity"] /
    supplier_orders["ordered_quantity"],
    0
)

supplier_orders["defect_rate_actual"] = np.where(
    supplier_orders["received_quantity"] != 0,
    supplier_orders["defect_quantity"] /
    supplier_orders["received_quantity"],
    0
)

# Supplier delivery days
supplier_orders["lead_time_actual"] = np.where(
    supplier_orders["received_date"].notna(),
    (
        supplier_orders["received_date"] -
        supplier_orders["order_date"]
    ).dt.days,
    np.nan
)

supplier_orders["on_time"] = np.where(
    supplier_orders["received_date"].notna() &
    supplier_orders["expected_date"].notna(),
    supplier_orders["received_date"] <=
    supplier_orders["expected_date"],
    np.nan
)

supplier_analysis = (
    supplier_orders
    .groupby("supplier_id")
    .agg(
        purchase_orders=("purchase_order_id", "count"),
        ordered_quantity=("ordered_quantity", "sum"),
        received_quantity=("received_quantity", "sum"),
        defect_quantity=("defect_quantity", "sum"),
        avg_lead_time=("lead_time_actual", "mean"),
        on_time_rate=("on_time", "mean")
    )
    .reset_index()
)

supplier_analysis["fulfillment_rate"] = (
    supplier_analysis["received_quantity"] /
    supplier_analysis["ordered_quantity"]
)

supplier_analysis["defect_rate"] = (
    supplier_analysis["defect_quantity"] /
    supplier_analysis["received_quantity"]
)

# ============================================================
# SUPPLIER SCORE
# ============================================================

# Project-defined scoring model:
# On-time delivery      = 40%
# Fulfillment           = 25%
# Lead-time performance = 20%
# Quality               = 15%

supplier_analysis["on_time_score"] = (
    supplier_analysis["on_time_rate"].fillna(0)
)

supplier_analysis["fulfillment_score"] = (
    supplier_analysis["fulfillment_rate"]
    .clip(0, 1)
)

# Lower lead time is better.
max_lead_time = supplier_analysis["avg_lead_time"].max()

supplier_analysis["lead_time_score"] = np.where(
    max_lead_time > 0,
    1 -
    (
        supplier_analysis["avg_lead_time"] /
        max_lead_time
    ),
    0
)

# Lower defect rate is better.
supplier_analysis["quality_score"] = (
    1 -
    supplier_analysis["defect_rate"]
).clip(0, 1)

supplier_analysis["supplier_score"] = (
    supplier_analysis["on_time_score"] * 0.40 +
    supplier_analysis["fulfillment_score"] * 0.25 +
    supplier_analysis["lead_time_score"] * 0.20 +
    supplier_analysis["quality_score"] * 0.15
)

supplier_analysis["supplier_score"] = (
    supplier_analysis["supplier_score"] * 100
)

# Supplier category
def classify_supplier(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Needs Improvement"

    else:
        return "Critical"


supplier_analysis["performance_category"] = (
    supplier_analysis["supplier_score"]
    .apply(classify_supplier)
)

# Add supplier names
supplier_analysis = supplier_analysis.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "supplier_region"
        ]
    ],
    on="supplier_id",
    how="left"
)

supplier_analysis = supplier_analysis[
    [
        "supplier_id",
        "supplier_name",
        "supplier_region",
        "purchase_orders",
        "ordered_quantity",
        "received_quantity",
        "defect_quantity",
        "fulfillment_rate",
        "defect_rate",
        "avg_lead_time",
        "on_time_rate",
        "supplier_score",
        "performance_category"
    ]
]

print("\nTop 10 Suppliers")

print(
    supplier_analysis
    .sort_values(
        "supplier_score",
        ascending=False
    )
    .head(10)
)

print("\nBottom 10 Suppliers")

print(
    supplier_analysis
    .sort_values(
        "supplier_score",
        ascending=True
    )
    .head(10)
)

supplier_analysis.to_csv(
    OUTPUT_DIR / "supplier_performance.csv",
    index=False
)


# ============================================================
# 9. MONTHLY REVENUE TREND
# ============================================================

print("\n" + "=" * 70)
print("9. MONTHLY SALES TREND")
print("=" * 70)

orders["month"] = (
    orders["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    orders
    .groupby("month")
    .agg(
        orders=("order_id", "count"),
        revenue=("revenue", "sum"),
        gross_profit=("gross_profit", "sum")
    )
    .reset_index()
)

print(monthly_sales)

monthly_sales.to_csv(
    OUTPUT_DIR / "monthly_sales.csv",
    index=False
)


# ============================================================
# 10. HIGH-DEMAND / LOW-STOCK PRODUCTS
# ============================================================

print("\n" + "=" * 70)
print("10. HIGH-DEMAND / LOW-STOCK PRODUCTS")
print("=" * 70)

product_demand = (
    inventory
    .groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .agg(
        total_sold=("sold_quantity", "sum"),
        average_stock=("closing_stock", "mean"),
        stockout_records=("stockout", "sum")
    )
    .reset_index()
)

# High demand = above median sales
# Low stock = below median average stock

demand_threshold = (
    product_demand["total_sold"].median()
)

stock_threshold = (
    product_demand["average_stock"].median()
)

high_demand_low_stock = product_demand[
    (
        product_demand["total_sold"] >
        demand_threshold
    )
    &
    (
        product_demand["average_stock"] <
        stock_threshold
    )
].copy()

high_demand_low_stock = (
    high_demand_low_stock
    .sort_values(
        "total_sold",
        ascending=False
    )
)

print("\nHigh-Demand / Low-Stock Products:")

print(high_demand_low_stock.head(20))

high_demand_low_stock.to_csv(
    OUTPUT_DIR / "high_demand_low_stock.csv",
    index=False
)


# ============================================================
# 11. BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("11. KEY BUSINESS INSIGHTS")
print("=" * 70)

# Best category
best_category = (
    category_analysis
    .sort_values("revenue", ascending=False)
    .iloc[0]
)

# Most profitable category
best_profit_category = (
    category_analysis
    .sort_values("gross_profit", ascending=False)
    .iloc[0]
)

# Best supplier
best_supplier = (
    supplier_analysis
    .sort_values("supplier_score", ascending=False)
    .iloc[0]
)

# Worst supplier
worst_supplier = (
    supplier_analysis
    .sort_values("supplier_score", ascending=True)
    .iloc[0]
)

# Highest stockout warehouse
warehouse_stockout = (
    inventory
    .groupby("warehouse_id")
    .agg(
        stockout_records=("stockout", "sum"),
        total_records=("stockout", "count")
    )
    .reset_index()
)

warehouse_stockout["stockout_rate"] = (
    warehouse_stockout["stockout_records"] /
    warehouse_stockout["total_records"]
)

worst_warehouse_id = (
    warehouse_stockout
    .sort_values(
        "stockout_rate",
        ascending=False
    )
    .iloc[0]["warehouse_id"]
)

worst_warehouse = warehouses[
    warehouses["warehouse_id"] ==
    worst_warehouse_id
].iloc[0]


print(
    f"\n1. Highest Revenue Category: "
    f"{best_category['category']} "
    f"(${best_category['revenue']:,.2f})"
)

print(
    f"\n2. Highest Profit Category: "
    f"{best_profit_category['category']} "
    f"(${best_profit_category['gross_profit']:,.2f})"
)

print(
    f"\n3. Overall On-Time Delivery: "
    f"{on_time_delivery:.2%}"
)

print(
    f"\n4. Average Delivery Time: "
    f"{average_delivery_days:.2f} days"
)

print(
    f"\n5. Average Delivery Delay: "
    f"{average_delay:.2f} days"
)

print(
    f"\n6. Stockout Rate: "
    f"{stockout_rate:.2%}"
)

print(
    f"\n7. Best Supplier: "
    f"{best_supplier['supplier_name']} "
    f"({best_supplier['supplier_score']:.2f}/100)"
)

print(
    f"\n8. Supplier Requiring Attention: "
    f"{worst_supplier['supplier_name']} "
    f"({worst_supplier['supplier_score']:.2f}/100)"
)

print(
    f"\n9. Warehouse with Highest Stockout Rate: "
    f"{worst_warehouse['warehouse_name']} "
    f"({worst_warehouse['city']})"
)

print(
    f"\n10. High-Demand / Low-Stock Products: "
    f"{len(high_demand_low_stock):,}"
)


# ============================================================
# SAVE KPI SUMMARY
# ============================================================

kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Revenue",
        "Total Cost",
        "Gross Profit",
        "Profit Margin",
        "Total Orders",
        "Delivered Orders",
        "Cancelled Orders",
        "Returned Orders",
        "On-Time Delivery %",
        "Average Delivery Days",
        "Average Delay Days",
        "Total Inventory Value",
        "Stockout Rate",
        "Excess Stock Records",
        "Average Supplier Fulfillment",
        "Average Supplier Defect Rate"
    ],

    "Value": [
        total_revenue,
        total_cost,
        total_profit,
        overall_margin,
        total_orders,
        delivered_orders,
        cancelled_orders,
        returned_orders,
        on_time_delivery,
        average_delivery_days,
        average_delay,
        total_inventory_value,
        stockout_rate,
        excess_stock_records,
        supplier_analysis["fulfillment_rate"].mean(),
        supplier_analysis["defect_rate"].mean()
    ]
})

kpi_summary.to_csv(
    OUTPUT_DIR / "kpi_summary.csv",
    index=False
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED")
print("=" * 70)

print("\nReports saved to:")
print(OUTPUT_DIR)

print("\nGenerated reports:")

for file in OUTPUT_DIR.glob("*.csv"):
    print(" -", file.name)