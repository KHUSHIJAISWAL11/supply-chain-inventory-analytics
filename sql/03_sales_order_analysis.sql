USE supply_chain_analytics;

-- =========================================
-- 1. TOTAL REVENUE
-- =========================================

SELECT
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue
FROM orders;


-- =========================================
-- 2. TOTAL ORDERS
-- =========================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- =========================================
-- 3. AVERAGE ORDER VALUE
-- =========================================

SELECT
    ROUND(
        SUM(quantity * unit_price)
        / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM orders;


-- =========================================
-- 4. MONTHLY REVENUE
-- =========================================

SELECT
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY
    YEAR(order_date),
    MONTH(order_date)
ORDER BY
    order_year,
    order_month;


-- =========================================
-- 5. REVENUE BY ORDER STATUS
-- =========================================

SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY order_status
ORDER BY revenue DESC;


-- =========================================
-- 6. SHIPPING METHOD PERFORMANCE
-- =========================================

SELECT
    shipping_method,
    COUNT(*) AS orders,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY shipping_method
ORDER BY revenue DESC;


-- =========================================
-- 7. ON-TIME VS LATE DELIVERY
-- =========================================

SELECT
    CASE
        WHEN delivery_date IS NULL THEN 'Not Delivered'
        WHEN delivery_date <= promised_date THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY delivery_status
ORDER BY order_count DESC;