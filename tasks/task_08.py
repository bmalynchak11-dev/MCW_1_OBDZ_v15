def receive_script() -> str:
    return """
WITH agg_delivery AS (
    SELECT
        sku,
        SUM(qty) AS total_qty,
        MAX(delivered_on) AS latest_delivery
    FROM delivery
    WHERE qty > 0
    GROUP BY sku
),
upserted AS (
    INSERT INTO stock (sku, qty, last_delivery)
    SELECT sku, total_qty, latest_delivery
    FROM agg_delivery
    ON CONFLICT (sku) DO UPDATE
    SET
        qty = stock.qty + EXCLUDED.qty,
        last_delivery = GREATEST(stock.last_delivery, EXCLUDED.last_delivery)
    RETURNING
        sku,
        qty AS qty_after,
        (xmax = 0) AS is_insert
)
INSERT INTO stock_log (sku, action, qty_after)
SELECT
    sku,
    CASE WHEN is_insert THEN 'insert' ELSE 'update' END AS action,
    qty_after
FROM upserted;
""".strip()