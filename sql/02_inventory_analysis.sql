USE supply_chain_analytics;

-- =========================================
-- 1. INVENTORY KPIs
-- =========================================

SELECT
    COUNT(*) AS inventory_records,
    SUM(opening_stock) AS total_opening_stock,
    SUM(received_quantity) AS total_received_quantity,
    SUM(sold_quantity) AS total_sold_quantity,
    SUM(closing_stock) AS total_closing_stock,
    SUM(damaged_quantity) AS total_damaged_stock
FROM inventory;


-- =========================================
-- 2. INVENTORY VALUE
-- =========================================

SELECT
    ROUND(
        SUM(i.closing_stock * p.unit_cost),
        2
    ) AS total_inventory_value
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id;


-- =========================================
-- 3. STOCK STATUS
-- =========================================

SELECT
    i.product_id,
    p.product_name,
    p.category,
    SUM(i.closing_stock) AS current_stock,
    p.reorder_level,
    CASE
        WHEN SUM(i.closing_stock) <= p.reorder_level
            THEN 'Reorder Required'
        ELSE 'Sufficient Stock'
    END AS stock_status
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY
    i.product_id,
    p.product_name,
    p.category,
    p.reorder_level
ORDER BY current_stock ASC;


-- =========================================
-- 4. DAMAGE BY CATEGORY
-- =========================================

SELECT
    p.category,
    SUM(i.damaged_quantity) AS damaged_units
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY damaged_units DESC;


-- =========================================
-- 5. DAMAGE RATE
-- =========================================

SELECT
    p.category,
    SUM(i.damaged_quantity) AS damaged_units,
    SUM(i.opening_stock + i.received_quantity) AS available_units,
    ROUND(
        100 * SUM(i.damaged_quantity)
        / NULLIF(
            SUM(i.opening_stock + i.received_quantity),
            0
        ),
        2
    ) AS damage_rate_percentage
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY damage_rate_percentage DESC;


-- =========================================
-- 6. CATEGORY INVENTORY PERFORMANCE
-- =========================================

SELECT
    p.category,
    SUM(i.sold_quantity) AS units_sold,
    SUM(i.closing_stock) AS closing_stock,
    SUM(i.damaged_quantity) AS damaged_units
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY units_sold DESC;