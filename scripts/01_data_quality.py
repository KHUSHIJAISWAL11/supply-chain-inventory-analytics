import pandas as pd
from pathlib import Path

#project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

# Load datasets
products = pd.read_csv(RAW_DIR / "products.csv")
suppliers = pd.read_csv(RAW_DIR / "suppliers.csv")
warehouses = pd.read_csv(RAW_DIR / "warehouses.csv")
inventory = pd.read_csv(RAW_DIR / "inventory.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
supplier_orders = pd.read_csv(RAW_DIR / "supplier_orders.csv")

datasets = {
    "Products": products,
    "Suppliers": suppliers,
    "Warehouses": warehouses,
    "Inventory": inventory,
    "Orders": orders,
    "Supplier Orders": supplier_orders
}


print("\n" + "=" * 60)
print("SUPPLY CHAIN DATASET OVERVIEW")
print("=" * 60)


for name, df in datasets.items():

    print(f"\n{name}")
    print("-" * 40)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())


print("\n" + "=" * 60)
print("DATA QUALITY CHECK COMPLETED")
print("=" * 60)