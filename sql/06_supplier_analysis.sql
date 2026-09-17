USE supply_chain_analytics;

-- =========================================
-- 1. SUPPLIER ORDER PERFORMANCE
-- =========================================

SELECT
    s.supplier_id,
    s.supplier_name,
    COUNT(so.purchase_order_id) AS purchase_orders,
    SUM(so.ordered_quantity) AS ordered_quantity,
    SUM(so.received_quantity) AS received_quantity,
    SUM(so.defect_quantity) AS defect_quantity
FROM supplier_orders so
JOIN suppliers s
    ON so.supplier_id = s.supplier_id
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY purchase_orders DESC;


-- =========================================
-- 2. SUPPLIER DEFECT RATE
-- =========================================

SELECT
    s.supplier_id,
    s.supplier_name,
    SUM(so.received_quantity) AS received_quantity,
    SUM(so.defect_quantity) AS defect_quantity,
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
ORDER BY defect_rate DESC;


-- =========================================
-- 3. SUPPLIER LEAD TIME
-- =========================================

SELECT
    s.supplier_id,
    s.supplier_name,
    ROUND(
        AVG(
            DATEDIFF(
                so.received_date,
                so.order_date
            )
        ),
        2
    ) AS avg_actual_lead_time
FROM supplier_orders so
JOIN suppliers s
    ON so.supplier_id = s.supplier_id
WHERE so.received_date IS NOT NULL
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY avg_actual_lead_time DESC;


-- =========================================
-- 4. SUPPLIER ON-TIME DELIVERY
-- =========================================

SELECT
    s.supplier_id,
    s.supplier_name,
    SUM(
        CASE
            WHEN so.received_date <= so.expected_date
            THEN 1
            ELSE 0
        END
    ) AS on_time_orders,
    COUNT(so.purchase_order_id) AS delivered_orders,
    ROUND(
        100 * SUM(
            CASE
                WHEN so.received_date <= so.expected_date
                THEN 1
                ELSE 0
            END
        ) / NULLIF(
            COUNT(so.purchase_order_id),
            0
        ),
        2
    ) AS on_time_percentage
FROM supplier_orders so
JOIN suppliers s
    ON so.supplier_id = s.supplier_id
WHERE so.received_date IS NOT NULL
GROUP BY
    s.supplier_id,
    s.supplier_name
ORDER BY on_time_percentage DESC;