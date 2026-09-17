import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_DIR = BASE_DIR / "outputs" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("STARTING EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# ============================================================
# LOAD DATA
# ============================================================

products = pd.read_csv(CLEANED_DIR / "products_cleaned.csv")
suppliers = pd.read_csv(CLEANED_DIR / "suppliers_cleaned.csv")
warehouses = pd.read_csv(CLEANED_DIR / "warehouses_cleaned.csv")
inventory = pd.read_csv(CLEANED_DIR / "inventory_cleaned.csv")
orders = pd.read_csv(CLEANED_DIR / "orders_cleaned.csv")
supplier_orders = pd.read_csv(CLEANED_DIR / "supplier_orders_cleaned.csv")

print("\nDatasets loaded successfully.")


# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

datasets = {
    "Products": products,
    "Suppliers": suppliers,
    "Warehouses": warehouses,
    "Inventory": inventory,
    "Orders": orders,
    "Supplier Orders": supplier_orders
}

for name, df in datasets.items():
    print(f"\n{name}")
    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")


# ============================================================
# PRODUCTS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PRODUCT ANALYSIS")
print("=" * 70)

print("\nProducts by Category:")
print(products["category"].value_counts())

print("\nAverage Selling Price by Category:")
print(
    products.groupby("category")["selling_price"]
    .mean()
    .sort_values(ascending=False)
)

print("\nMost Expensive Products:")
print(
    products[
        ["product_name", "category", "unit_cost", "selling_price"]
    ]
    .sort_values("selling_price", ascending=False)
    .head(10)
)


# ============================================================
# SUPPLIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SUPPLIER ANALYSIS")
print("=" * 70)

print("\nAverage Lead Time:")
print(suppliers["average_lead_time"].mean())

print("\nAverage Defect Rate:")
print(suppliers["defect_rate"].mean())

print("\nTop 10 Suppliers by Lead Time:")
print(
    suppliers[
        ["supplier_name", "supplier_region", "average_lead_time"]
    ]
    .sort_values("average_lead_time", ascending=False)
    .head(10)
)

print("\nTop 10 Suppliers by Defect Rate:")
print(
    suppliers[
        ["supplier_name", "supplier_region", "defect_rate"]
    ]
    .sort_values("defect_rate", ascending=False)
    .head(10)
)


# ============================================================
# WAREHOUSE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("WAREHOUSE ANALYSIS")
print("=" * 70)

print("\nWarehouses by Region:")
print(warehouses["region"].value_counts())

print("\nWarehouse Capacity:")
print(
    warehouses[
        ["warehouse_name", "city", "region", "warehouse_capacity"]
    ]
    .sort_values("warehouse_capacity", ascending=False)
)


# ============================================================
# INVENTORY ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("INVENTORY ANALYSIS")
print("=" * 70)

inventory["inventory_value"] = (
    inventory["closing_stock"] *
    inventory["product_id"].map(
        products.set_index("product_id")["unit_cost"]
    )
)

print("\nTotal Inventory Value:")
print(f"${inventory['inventory_value'].sum():,.2f}")

print("\nTotal Units Sold:")
print(f"{inventory['sold_quantity'].sum():,.0f}")

print("\nTotal Damaged Units:")
print(f"{inventory['damaged_quantity'].sum():,.0f}")

print("\nStockout Records:")
stockouts = inventory[inventory["closing_stock"] <= 0]
print(f"{len(stockouts):,}")


# ============================================================
# ORDERS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("ORDER ANALYSIS")
print("=" * 70)

orders["revenue"] = (
    orders["quantity"] *
    orders["unit_price"]
)

print("\nTotal Revenue:")
print(f"${orders['revenue'].sum():,.2f}")

print("\nTotal Orders:")
print(f"{orders['order_id'].nunique():,}")

print("\nOrder Status:")
print(orders["order_status"].value_counts())

print("\nShipping Method:")
print(orders["shipping_method"].value_counts())

print("\nRevenue by Order Status:")
print(
    orders.groupby("order_status")["revenue"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# SUPPLIER ORDER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SUPPLIER ORDER ANALYSIS")
print("=" * 70)

supplier_orders["fulfillment_rate"] = (
    supplier_orders["received_quantity"] /
    supplier_orders["ordered_quantity"]
)

print("\nAverage Fulfillment Rate:")
print(
    supplier_orders["fulfillment_rate"].mean()
)

print("\nTotal Ordered Quantity:")
print(
    f"{supplier_orders['ordered_quantity'].sum():,.0f}"
)

print("\nTotal Received Quantity:")
print(
    f"{supplier_orders['received_quantity'].sum():,.0f}"
)

print("\nTotal Defective Quantity:")
print(
    f"{supplier_orders['defect_quantity'].sum():,.0f}"
)


# ============================================================
# BASIC VISUALIZATION
# ============================================================

# Revenue by category
category_revenue = (
    orders.merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left"
    )
    .groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

category_revenue.plot(kind="bar")

plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "revenue_by_category.png",
    dpi=300
)

plt.close()


# ============================================================
# TOP PRODUCTS
# ============================================================

product_revenue = (
    orders.merge(
        products[["product_id", "product_name"]],
        on="product_id",
        how="left"
    )
    .groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

product_revenue.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_10_products.png",
    dpi=300
)

plt.close()


print("\n" + "=" * 70)
print("EDA COMPLETED")
print("=" * 70)

print(f"\nCharts saved to:")
print(OUTPUT_DIR)