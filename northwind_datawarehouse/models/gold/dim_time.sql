WITH date_bounds AS (
    SELECT
        MIN(order_date)::DATE AS start_date,
        MAX(
            GREATEST(
                order_date::DATE,
                required_date::DATE,
                COALESCE(shipped_date::DATE, order_date::DATE)
            )
        ) AS end_date
    FROM {{ ref('silver_orders') }}
),

calendar AS (
    SELECT calendar_date::DATE AS date_day
    FROM date_bounds,
    generate_series(
        start_date,
        end_date,
        INTERVAL 1 DAY
    ) AS dates(calendar_date)
)

SELECT
    CAST(strftime(date_day, '%Y%m%d') AS INTEGER) AS date_key,
    date_day,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(QUARTER FROM date_day) AS quarter,
    EXTRACT(MONTH FROM date_day) AS month_number,
    strftime(date_day, '%B') AS month_name,
    EXTRACT(WEEK FROM date_day) AS week_number,
    EXTRACT(ISODOW FROM date_day) AS day_of_week_number,
    strftime(date_day, '%A') AS day_name,
    CASE
        WHEN EXTRACT(ISODOW FROM date_day) IN (6, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend
FROM calendar