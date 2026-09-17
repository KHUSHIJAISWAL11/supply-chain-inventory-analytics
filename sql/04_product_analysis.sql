USE supply_chain_analytics;

-- =========================================
-- 1. TOP PRODUCTS BY REVENUE
-- =========================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- =========================================
-- 2. REVENUE BY CATEGORY
-- =========================================

SELECT
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- =========================================
-- 3. PRODUCT MARGIN
-- =========================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.selling_price,
    p.unit_cost,
    ROUND(p.selling_price - p.unit_cost, 2) AS unit_margin,
    ROUND(
        100 * (p.selling_price - p.unit_cost)
        / NULLIF(p.selling_price, 0),
        2
    ) AS margin_percentage
FROM products p
ORDER BY margin_percentage DESC;


-- =========================================
-- 4. LOW-SELLING PRODUCTS
-- =========================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COALESCE(SUM(o.quantity), 0) AS units_sold
FROM products p
LEFT JOIN orders o
    ON p.product_id = o.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY units_sold ASC
LIMIT 10;