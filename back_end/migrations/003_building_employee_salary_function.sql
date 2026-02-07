-- Migration 003: Function tính lương nhân viên tòa nhà theo tháng
-- Lương = base_salary + sum(doanh thu dịch vụ × bonus_rate) cho từng dịch vụ nhân viên được phân công

CREATE OR REPLACE FUNCTION get_building_employee_salaries(p_year INT, p_month INT)
RETURNS TABLE (
    employee_id INT,
    full_name TEXT,
    role TEXT,
    base_salary DECIMAL(15,2),
    bonus_rate FLOAT,
    monthly_revenue DECIMAL(15,2),
    total_salary DECIMAL(15,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_month_start DATE;
    v_month_end   DATE;
BEGIN
    v_month_start := MAKE_DATE(p_year, p_month, 1);
    v_month_end   := v_month_start + INTERVAL '1 month' - INTERVAL '1 day';

    RETURN QUERY
    WITH month_bounds AS (
        SELECT v_month_start AS d_start, v_month_end::date AS d_end
    ),
    -- Doanh thu theo dịch vụ trong tháng (service_id -> tổng tiền)
    service_revenue AS (
        SELECT
            cmu.service_id,
            COALESCE(SUM(cmu.price), 0)::DECIMAL(15,2) AS revenue
        FROM company_monthly_usages cmu
        CROSS JOIN month_bounds mb
        WHERE EXTRACT(YEAR FROM cmu.from_date) = p_year
          AND EXTRACT(MONTH FROM cmu.from_date) = p_month
        GROUP BY cmu.service_id
    ),
    -- Phân công nhân viên làm dịch vụ trong tháng + quy tắc lương
    employee_service_bonus AS (
        SELECT
            ss.employee_id,
            srr.service_id,
            sr.bonus_rate,
            COALESCE(srrev.revenue, 0) AS service_revenue,
            (COALESCE(srrev.revenue, 0) * COALESCE(sr.bonus_rate, 0)) AS bonus
        FROM service_subscribers ss
        JOIN service_role_rules srr ON ss.service_role_rules_id = srr.id
        JOIN salary_rules sr ON srr.salary_rule_id = sr.id
        CROSS JOIN month_bounds mb
        LEFT JOIN service_revenue srrev ON srrev.service_id = srr.service_id
        WHERE ss.from_date <= mb.d_end
          AND (ss.end_date IS NULL OR ss.end_date >= mb.d_start)
    ),
    -- Tổng bonus và tổng doanh thu theo từng nhân viên
    employee_totals AS (
        SELECT
            esb.employee_id,
            COALESCE(MAX(esb.bonus_rate), 0)::FLOAT AS bonus_rate_display,
            COALESCE(SUM(esb.service_revenue), 0)::DECIMAL(15,2) AS monthly_revenue,
            COALESCE(SUM(esb.bonus), 0)::DECIMAL(15,2) AS total_bonus
        FROM employee_service_bonus esb
        GROUP BY esb.employee_id
    )
    SELECT
        be.employee_id,
        (TRIM(COALESCE(be.first_name, '') || ' ' || COALESCE(be.last_name, '')))::TEXT AS full_name,
        be.role::TEXT,
        be.base_salary,
        COALESCE(et.bonus_rate_display, 0)::FLOAT AS bonus_rate,
        COALESCE(et.monthly_revenue, 0)::DECIMAL(15,2) AS monthly_revenue,
        (be.base_salary + COALESCE(et.total_bonus, 0))::DECIMAL(15,2) AS total_salary
    FROM building_employees be
    LEFT JOIN employee_totals et ON et.employee_id = be.employee_id
    ORDER BY be.employee_id;
END;
$$;

COMMENT ON FUNCTION get_building_employee_salaries(INT, INT) IS
'Tính lương nhân viên tòa nhà theo tháng: base_salary + sum(doanh thu dịch vụ × bonus_rate) cho các dịch vụ được phân công trong tháng';

DO $$
BEGIN
    RAISE NOTICE 'Migration 003: Function get_building_employee_salaries(p_year, p_month) created';
END $$;
