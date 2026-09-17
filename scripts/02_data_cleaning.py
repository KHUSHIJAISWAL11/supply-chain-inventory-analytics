import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

products = pd.read_csv(RAW_DIR / "products.csv")
suppliers = pd.read_csv(RAW_DIR / "suppliers.csv")
warehouses = pd.read_csv(RAW_DIR / "warehouses.csv")
inventory = pd.read_csv(RAW_DIR / "inventory.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
supplier_orders = pd.read_csv(RAW_DIR / "supplier_orders.csv")


print("=" * 70)
print("STARTING DATA CLEANING")
print("=" * 70)


# ============================================================
# 3. PRODUCTS CLEANING
# ============================================================

print("\nCleaning Products...")

# Fill missing subcategory
products["subcategory"] = products["subcategory"].fillna("Unknown")

# Remove duplicate product IDs
products = products.drop_duplicates(subset="product_id")

# Ensure numeric columns are numeric
products["unit_cost"] = pd.to_numeric(products["unit_cost"], errors="coerce")
products["selling_price"] = pd.to_numeric(products["selling_price"], errors="coerce")
products["reorder_level"] = pd.to_numeric(products["reorder_level"], errors="coerce")

# Remove invalid prices
products = products[
    (products["unit_cost"] > 0) &
    (products["selling_price"] > 0)
]

# Remove invalid reorder levels
products = products[products["reorder_level"] >= 0]


# ============================================================
# 4. SUPPLIERS CLEANING
# ============================================================

print("Cleaning Suppliers...")

suppliers = suppliers.drop_duplicates(subset="supplier_id")

suppliers["average_lead_time"] = pd.to_numeric(
    suppliers["average_lead_time"],
    errors="coerce"
)

suppliers["defect_rate"] = pd.to_numeric(
    suppliers["defect_rate"],
    errors="coerce"
)

# Keep valid lead times
suppliers = suppliers[suppliers["average_lead_time"] > 0]

# Defect rate should be between 0 and 1
suppliers = suppliers[
    (suppliers["defect_rate"] >= 0) &
    (suppliers["defect_rate"] <= 1)
]


# ============================================================
# 5. WAREHOUSE CLEANING
# ============================================================

print("Cleaning Warehouses...")

warehouses = warehouses.drop_duplicates(subset="warehouse_id")

warehouses["warehouse_capacity"] = pd.to_numeric(
    warehouses["warehouse_capacity"],
    errors="coerce"
)

warehouses = warehouses[
    warehouses["warehouse_capacity"] > 0
]


# ============================================================
# 6. INVENTORY CLEANING
# ============================================================

print("Cleaning Inventory...")

# Convert date
inventory["inventory_date"] = pd.to_datetime(
    inventory["inventory_date"],
    errors="coerce"
)

# Convert numerical columns
inventory_columns = [
    "opening_stock",
    "received_quantity",
    "sold_quantity",
    "closing_stock",
    "damaged_quantity"
]

for column in inventory_columns:
    inventory[column] = pd.to_numeric(
        inventory[column],
        errors="coerce"
    )

# Remove duplicate inventory records
inventory = inventory.drop_duplicates()

# Remove invalid negative quantities
for column in inventory_columns:
    inventory = inventory[inventory[column] >= 0]

# Validate inventory calculation
inventory["calculated_closing_stock"] = (
    inventory["opening_stock"]
    + inventory["received_quantity"]
    - inventory["sold_quantity"]
    - inventory["damaged_quantity"]
)

# Flag calculation mismatches
inventory["inventory_calculation_check"] = (
    inventory["closing_stock"]
    == inventory["calculated_closing_stock"]
)

print(
    "Inventory calculation mismatches:",
    (~inventory["inventory_calculation_check"]).sum()
)

# Remove helper columns after validation
inventory = inventory.drop(
    columns=[
        "calculated_closing_stock",
        "inventory_calculation_check"
    ]
)


# ============================================================
# 7. ORDERS CLEANING
# ============================================================

print("Cleaning Orders...")

# Remove duplicate orders
orders = orders.drop_duplicates(subset="order_id")

# Convert dates
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

# Convert numeric columns
orders["quantity"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
)

orders["unit_price"] = pd.to_numeric(
    orders["unit_price"],
    errors="coerce"
)

# Remove invalid quantity and price
orders = orders[
    (orders["quantity"] > 0) &
    (orders["unit_price"] > 0)
]

# Missing shipping method
orders["shipping_method"] = orders["shipping_method"].fillna(
    "Unknown"
)

# Check invalid delivery dates
invalid_delivery = (
    orders["delivery_date"].notna()
    & (orders["delivery_date"] < orders["order_date"])
)

print(
    "Invalid delivery dates:",
    invalid_delivery.sum()
)

# For cancelled orders delivery date should be blank
orders.loc[
    orders["order_status"] == "Cancelled",
    "delivery_date"
] = pd.NaT


# ============================================================
# 8. SUPPLIER ORDERS CLEANING
# ============================================================

print("Cleaning Supplier Orders...")

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

numeric_columns = [
    "ordered_quantity",
    "received_quantity",
    "defect_quantity"
]

for column in numeric_columns:
    supplier_orders[column] = pd.to_numeric(
        supplier_orders[column],
        errors="coerce"
    )

# Remove duplicates
supplier_orders = supplier_orders.drop_duplicates(
    subset="purchase_order_id"
)

# Remove invalid quantities
supplier_orders = supplier_orders[
    (supplier_orders["ordered_quantity"] > 0) &
    (supplier_orders["received_quantity"] >= 0) &
    (supplier_orders["defect_quantity"] >= 0)
]

# Received quantity cannot exceed ordered quantity
supplier_orders.loc[
    supplier_orders["received_quantity"]
    > supplier_orders["ordered_quantity"],
    "received_quantity"
] = supplier_orders["ordered_quantity"]


# ============================================================
# 9. SAVE CLEANED DATA
# ============================================================

products.to_csv(
    CLEANED_DIR / "products_cleaned.csv",
    index=False
)

suppliers.to_csv(
    CLEANED_DIR / "suppliers_cleaned.csv",
    index=False
)

warehouses.to_csv(
    CLEANED_DIR / "warehouses_cleaned.csv",
    index=False
)

inventory.to_csv(
    CLEANED_DIR / "inventory_cleaned.csv",
    index=False
)

orders.to_csv(
    CLEANED_DIR / "orders_cleaned.csv",
    index=False
)

supplier_orders.to_csv(
    CLEANED_DIR / "supplier_orders_cleaned.csv",
    index=False
)


# ============================================================
# 10. FINAL SUMMARY
# ============================================================

datasets = {
    "Products": products,
    "Suppliers": suppliers,
    "Warehouses": warehouses,
    "Inventory": inventory,
    "Orders": orders,
    "Supplier Orders": supplier_orders
}

print("\n" + "=" * 70)
print("CLEANING COMPLETED")
print("=" * 70)

for name, df in datasets.items():
    print(
        f"{name:<20} Rows: {len(df):>8} | "
        f"Columns: {len(df.columns):>2} | "
        f"Missing Values: {df.isnull().sum().sum():>5}"
    )

print("\nCleaned files saved to:")
print(CLEANED_DIR)