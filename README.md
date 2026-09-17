# Supply Chain & Inventory Analytics

An end-to-end Data Analytics project focused on analyzing inventory,
warehouse operations, supplier performance, order fulfillment, and
supply-chain risks.

The project combines Python, MySQL, and Power BI to transform raw
operational data into interactive dashboards and actionable business
insights.

---

## 📌 Project Overview

Supply chain teams need to maintain the right inventory levels,
monitor warehouse capacity, evaluate supplier performance, and
identify operational risks.

This project analyzes multiple supply-chain datasets to answer
important business questions such as:

- How much inventory value is being held?
- Which categories and warehouses have higher stockout exposure?
- How are suppliers performing in terms of lead time and defect rate?
- What is the overall order fulfillment performance?
- Which suppliers require further investigation?
- Where are inventory damage and stockout risks concentrated?
- How can operational data be converted into useful management insights?

The project follows a complete analytics workflow from raw data
preparation to business intelligence reporting.

---

# 🎯 Business Objectives

The main objectives of the project are to:

- Analyze inventory levels and inventory value
- Monitor warehouse utilization and capacity
- Identify stockout patterns
- Analyze damaged inventory
- Evaluate supplier lead time
- Monitor supplier defect rates
- Measure purchase-order fulfillment
- Analyze order status and purchasing activity
- Identify potential supplier and inventory risks
- Provide interactive dashboards for business users

---

# 📊 Dataset

The project contains multiple related datasets representing different
areas of the supply chain.

| Dataset | Records |
|---|---:|
| Products | 400 |
| Suppliers | 40 |
| Warehouses | 15 |
| Inventory | 108,000 |
| Orders | 74,985 |
| Supplier Orders | 15,000 |

### Main Data Entities

#### Products
Contains product information including:

- Product ID
- Product Name
- Category
- Subcategory
- Unit Cost
- Selling Price
- Reorder Level

#### Suppliers
Contains supplier-level information including:

- Supplier ID
- Supplier Name
- Supplier Region
- Average Lead Time
- Defect Rate

#### Warehouses
Contains warehouse information such as:

- Warehouse ID
- Warehouse Name
- Region
- Capacity

#### Inventory
Contains inventory-level operational data including stock,
sales, damage, warehouse and product information.

#### Orders
Contains customer/order transaction information including:

- Order Date
- Product
- Warehouse
- Supplier
- Quantity
- Unit Price
- Order Status
- Shipping Method
- Promised Date
- Delivery Date

#### Supplier Orders
Contains purchase-order information including:

- Purchase Order ID
- Supplier
- Product
- Warehouse
- Order Date
- Expected Date
- Received Date
- Ordered Quantity
- Received Quantity
- Defect Quantity

---

# 🛠️ Technology Stack

### Data Analysis
- Python
- Pandas
- NumPy

### Data Visualization
- Matplotlib
- Seaborn
- Power BI

### Database & SQL
- MySQL
- Advanced SQL
- Joins
- Aggregations
- CTEs
- Window Functions
- Subqueries
- KPI analysis

### Business Intelligence
- Power BI
- DAX
- Data Modeling
- Relationships
- Slicers
- Interactive Navigation
- KPI Cards
- Drill-down analysis
- Conditional formatting

### Development
- VS Code
- Git
- GitHub

---

# 🔄 Project Workflow

```text
Raw CSV Data
      ↓
Data Quality Checks
      ↓
Python Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Cleaned CSV Files
      ↓
MySQL Database
      ↓
SQL Analysis
      ↓
Advanced SQL Analysis
      ↓
Power BI Data Model
      ↓
DAX Measures
      ↓
Interactive Dashboards
      ↓
Business & Risk Insights
