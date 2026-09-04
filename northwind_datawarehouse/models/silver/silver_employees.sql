WITH employees AS (
    SELECT * FROM {{ref('bronze_employees')}}
),
direct_reports_count AS (
    SELECT 
        reports_to AS manager_id,
        COUNT(*) AS num_direct_reports
    FROM employees
    GROUP BY reports_to
)
SELECT
    -- Employee Details
    CAST(e.employee_id AS INTEGER) AS employee_id,
    TRIM(e.first_name) || ' ' || TRIM(e.last_name) AS full_name,
    TRIM(e.title) AS title,
    CAST(e.birth_date AS DATE) AS birth_date,
    CAST(e.hire_date AS DATE) AS hire_date,
    COALESCE(TRIM(e.address), 'Unknown') AS employee_address,
    COALESCE(TRIM(e.city), 'Unknown') AS city,
    COALESCE(TRIM(e.region), 'Unknown') AS region,
    COALESCE(TRIM(e.country), 'Unknown') AS country,
    COALESCE(TRIM(e.postal_code), 'Unknown') AS postal_code,

    -- Manager Information
    CAST(e.reports_to AS INTEGER) AS manager_id,
    COALESCE(TRIM(m.first_name) || ' ' || TRIM(m.last_name), 'No Manager') AS manager_full_name,
    COALESCE(TRIM(m.title), 'N/A') AS manager_title,

    -- Number of Direct Reports
    COALESCE(drc.num_direct_reports, 0) AS direct_reports
FROM employees e
LEFT JOIN employees m ON e.reports_to = m.employee_id
LEFT JOIN direct_reports_count drc ON e.employee_id = drc.manager_id