USE supply_chain_analytics;

-- =========================================
-- 1. CTE
-- Top 10 Products by Revenue
-- =========================================

WITH product_revenue AS (
    SELECT
        product_id,
        SUM(quantity * unit_price) AS revenue
    FROM orders
    GROUP BY product_id
)
SELECT
    p.product_id,
    p.product_name,
    ROUND(pr.revenue, 2) AS revenue
FROM product_revenue pr
JOIN products p
    ON pr.product_id = p.product_id
ORDER BY revenue DESC
LIMIT 10;


-- =========================================
-- 2. RANK()
-- =========================================

SELECT
    product_id,
    revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM (
    SELECT
        product_id,
        SUM(quantity * unit_price) AS revenue
    FROM orders
    GROUP BY product_id
) x;


-- =========================================
-- 3. RUNNING REVENUE
-- =========================================

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(quantity * unit_price) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(
        SUM(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS running_revenue
FROM monthly_sales
ORDER BY month;


-- =========================================
-- 4. MONTH-OVER-MONTH REVENUE
-- =========================================

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        SUM(quantity * unit_price) AS revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        LAG(revenue) OVER (
            ORDER BY month
        ),
        2
    ) AS previous_month_revenue,
    ROUND(
        100 * (
            revenue -
            LAG(revenue) OVER (
                ORDER BY month
            )
        )
        / NULLIF(
            LAG(revenue) OVER (
                ORDER BY month
            ),
            0
        ),
        2
    ) AS mom_growth_percentage
FROM monthly_sales
ORDER BY month;


-- =========================================
-- 5. TOP PRODUCT WITHIN EACH CATEGORY
-- =========================================

WITH product_sales AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(o.quantity * o.unit_price) AS revenue
    FROM orders o
    JOIN products p
        ON o.product_id = p.product_id
    GROUP BY
        p.category,
        p.product_id,
        p.product_name
),
ranked_products AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS product_rank
    FROM product_sales
)
SELECT
    category,
    product_id,
    product_name,
    ROUND(revenue, 2) AS revenue
FROM ranked_products
WHERE product_rank = 1
ORDER BY revenue DESC;