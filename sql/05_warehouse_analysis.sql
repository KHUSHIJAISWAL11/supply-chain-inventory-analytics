USE supply_chain_analytics;

-- =========================================
-- 1. REVENUE BY WAREHOUSE
-- =========================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN warehouses w
    ON o.warehouse_id = w.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.region
ORDER BY revenue DESC;


-- =========================================
-- 2. INVENTORY BY WAREHOUSE
-- =========================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    SUM(i.closing_stock) AS closing_stock
FROM inventory i
JOIN warehouses w
    ON i.warehouse_id = w.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY closing_stock DESC;


-- =========================================
-- 3. DAMAGED STOCK BY WAREHOUSE
-- =========================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    SUM(i.damaged_quantity) AS damaged_units
FROM inventory i
JOIN warehouses w
    ON i.warehouse_id = w.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY damaged_units DESC;


-- =========================================
-- 4. WAREHOUSE ORDER PERFORMANCE
-- =========================================

SELECT
    w.warehouse_name,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    ROUND(AVG(o.quantity), 2) AS avg_order_quantity
FROM orders o
JOIN warehouses w
    ON o.warehouse_id = w.warehouse_id
GROUP BY w.warehouse_name
ORDER BY revenue DESC;