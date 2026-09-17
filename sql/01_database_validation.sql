USE supply_chain_analytics;

-- =========================================
-- 1. TABLE ROW COUNTS
-- =========================================

SELECT 'products' AS table_name, COUNT(*) AS row_count
FROM products

UNION ALL

SELECT 'suppliers', COUNT(*)
FROM suppliers

UNION ALL

SELECT 'warehouses', COUNT(*)
FROM warehouses

UNION ALL

SELECT 'inventory', COUNT(*)
FROM inventory

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'supplier_orders', COUNT(*)
FROM supplier_orders;


-- =========================================
-- 2. ORDERS NULL CHECK
-- =========================================

SELECT
    COUNT(*) AS total_orders,
    SUM(order_date IS NULL) AS missing_order_date,
    SUM(product_id IS NULL) AS missing_product_id,
    SUM(warehouse_id IS NULL) AS missing_warehouse_id,
    SUM(supplier_id IS NULL) AS missing_supplier_id,
    SUM(delivery_date IS NULL) AS missing_delivery_date
FROM orders;


-- =========================================
-- 3. SUPPLIER ORDERS NULL CHECK
-- =========================================

SELECT
    COUNT(*) AS total_supplier_orders,
    SUM(supplier_id IS NULL) AS missing_supplier_id,
    SUM(product_id IS NULL) AS missing_product_id,
    SUM(warehouse_id IS NULL) AS missing_warehouse_id,
    SUM(received_date IS NULL) AS missing_received_date
FROM supplier_orders;


-- =========================================
-- 4. DUPLICATE ORDER IDs
-- =========================================

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- =========================================
-- 5. DUPLICATE PURCHASE ORDER IDs
-- =========================================

SELECT
    purchase_order_id,
    COUNT(*) AS duplicate_count
FROM supplier_orders
GROUP BY purchase_order_id
HAVING COUNT(*) > 1;


-- =========================================
-- 6. INVALID PRODUCT REFERENCES
-- =========================================

SELECT COUNT(*) AS invalid_product_orders
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;


-- =========================================
-- 7. INVALID WAREHOUSE REFERENCES
-- =========================================

SELECT COUNT(*) AS invalid_warehouse_orders
FROM orders o
LEFT JOIN warehouses w
    ON o.warehouse_id = w.warehouse_id
WHERE w.warehouse_id IS NULL;


-- =========================================
-- 8. INVALID SUPPLIER REFERENCES
-- =========================================

SELECT COUNT(*) AS invalid_supplier_orders
FROM orders o
LEFT JOIN suppliers s
    ON o.supplier_id = s.supplier_id
WHERE s.supplier_id IS NULL;

---
products           400
suppliers           40
warehouses          15
inventory       108000
orders           74985
supplier_orders  15000
---
