USE supply_chain_analytics;

-- =========================================
-- BUSINESS QUESTION 1
-- Which products need immediate reorder?
-- =========================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(i.closing_stock) AS current_stock,
    p.reorder_level
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.reorder_level
HAVING SUM(i.closing_stock) <= p.reorder_level
ORDER BY current_stock;


-- =========================================
-- BUSINESS QUESTION 2
-- Which suppliers have high defect rates?
-- =========================================

SELECT
    s.supplier_name,
    ROUND(
        100 * SUM(so.defect_quantity)
        / NULLIF(SUM(so.received_quantity), 0),
        2
    ) AS defect_rate
FROM supplier_orders so
JOIN suppliers s
    ON so.supplier_id = s.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name
HAVING defect_rate > 5
ORDER BY defect_rate DESC;


-- =========================================
-- BUSINESS QUESTION 3
-- Which warehouses generate the most revenue?
-- =========================================

SELECT
    w.warehouse_name,
    ROUND(
        SUM(o.quantity * o.unit_price),
        2
    ) AS revenue
FROM orders o
JOIN warehouses w
    ON o.warehouse_id = w.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY revenue DESC;


-- =========================================
-- BUSINESS QUESTION 4
-- Which categories have high damage?
-- =========================================

SELECT
    p.category,
    SUM(i.damaged_quantity) AS damaged_units,
    ROUND(
        100 * SUM(i.damaged_quantity)
        / NULLIF(
            SUM(i.opening_stock + i.received_quantity),
            0
        ),
        2
    ) AS damage_rate
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY damage_rate DESC;