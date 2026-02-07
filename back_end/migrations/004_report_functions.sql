-- Migration 004: Các function PostgreSQL cho báo cáo và chi phí
-- 1. get_company_monthly_costs   - Chi phí tháng của công ty (tiền thuê + dịch vụ)
-- 2. get_company_service_details - Chi tiết dịch vụ theo công ty/tháng
-- 3. get_building_finance        - Tổng thu chi tòa nhà theo tháng
-- 4. get_building_finance_details - Chi tiết thu chi tòa nhà theo tháng

-- =============================================================================
-- 1. Chi phí tháng của công ty (tiền thuê + từng loại dịch vụ)
-- =============================================================================
CREATE OR REPLACE FUNCTION get_company_monthly_costs(
    p_company_id INT,
    p_year INT,
    p_month INT
)
RETURNS TABLE (
    company_id INT,
    month INT,
    year INT,
    rent_cost DECIMAL(15,2),
    total_area DECIMAL(10,2),
    service_costs JSONB,
    total_service_cost DECIMAL(15,2),
    total_cost DECIMAL(15,2)
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
    WITH
    -- Tiền thuê (hợp đồng active trong tháng)
    rent AS (
        SELECT
            COALESCE(SUM(rc.rent_price), 0)::DECIMAL(15,2) AS rent_cost,
            COALESCE(SUM(o.area), 0)::DECIMAL(10,2) AS total_area
        FROM rent_contracts rc
        JOIN offices o ON rc.office_id = o.id
        WHERE rc.company_id = p_company_id
          AND rc.status = 'active'
          AND rc.from_date <= v_month_end
          AND rc.end_date >= v_month_start
    ),
    -- Dịch vụ theo tháng (company_monthly_usages)
    svc_monthly AS (
        SELECT
            s.name AS service_name,
            COALESCE(SUM(cmu.price), 0)::DECIMAL(15,2) AS service_cost
        FROM company_monthly_usages cmu
        JOIN services s ON cmu.service_id = s.id
        WHERE cmu.company_id = p_company_id
          AND EXTRACT(YEAR FROM cmu.from_date) = p_year
          AND EXTRACT(MONTH FROM cmu.from_date) = p_month
        GROUP BY s.id, s.name
    ),
    -- Dịch vụ theo ngày (gửi xe, ăn trưa)
    svc_daily AS (
        SELECT
            s.name AS service_name,
            COALESCE(SUM(edu.price), 0)::DECIMAL(15,2) AS service_cost
        FROM employee_daily_usages edu
        JOIN company_employees ce ON edu.employee_id = ce.id
        JOIN services s ON edu.service_id = s.id
        WHERE ce.company_id = p_company_id
          AND EXTRACT(YEAR FROM edu.usage_date) = p_year
          AND EXTRACT(MONTH FROM edu.usage_date) = p_month
        GROUP BY s.id, s.name
    ),
    all_services AS (
        SELECT service_name, service_cost FROM svc_monthly
        UNION ALL
        SELECT service_name, service_cost FROM svc_daily
    ),
    service_agg AS (
        SELECT COALESCE(jsonb_agg(jsonb_build_object('service_name', service_name, 'service_cost', service_cost)), '[]'::jsonb) AS arr,
               COALESCE(SUM(service_cost), 0)::DECIMAL(15,2) AS total
        FROM all_services
    )
    SELECT
        p_company_id,
        p_month,
        p_year,
        r.rent_cost,
        r.total_area,
        sa.arr,
        sa.total,
        (r.rent_cost + sa.total)
    FROM rent r
    CROSS JOIN service_agg sa;
END;
$$;

COMMENT ON FUNCTION get_company_monthly_costs(INT, INT, INT) IS
'Chi phí tháng của công ty: tiền thuê + tổng tiền từng loại dịch vụ (theo tháng + theo ngày)';

-- =============================================================================
-- 2. Chi tiết dịch vụ của công ty theo tháng (từng lần sử dụng / đơn giá)
-- =============================================================================
CREATE OR REPLACE FUNCTION get_company_service_details(
    p_company_id INT,
    p_year INT,
    p_month INT
)
RETURNS TABLE (
    company_id INT,
    company_name TEXT,
    month INT,
    year INT,
    monthly_services JSONB,
    daily_services JSONB,
    total_service_cost DECIMAL(15,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_cname TEXT;
BEGIN
    SELECT c.name INTO v_cname FROM companies c WHERE c.id = p_company_id;
    v_cname := COALESCE(v_cname, 'Company ' || p_company_id);

    RETURN QUERY
    WITH
    monthly AS (
        SELECT jsonb_agg(
            jsonb_build_object(
                'service_name', s.name,
                'quantity', cmu.quantity,
                'unit_price', (cmu.price / NULLIF(cmu.quantity, 0)),
                'total_cost', cmu.price
            )
        ) AS arr
        FROM company_monthly_usages cmu
        JOIN services s ON cmu.service_id = s.id
        WHERE cmu.company_id = p_company_id
          AND EXTRACT(YEAR FROM cmu.from_date) = p_year
          AND EXTRACT(MONTH FROM cmu.from_date) = p_month
    ),
    daily AS (
        SELECT jsonb_agg(
            jsonb_build_object(
                'employee_name', ce.full_name,
                'service_name', s.name,
                'usage_date', edu.usage_date,
                'price', edu.price
            )
        ) AS arr
        FROM employee_daily_usages edu
        JOIN company_employees ce ON edu.employee_id = ce.id
        JOIN services s ON edu.service_id = s.id
        WHERE ce.company_id = p_company_id
          AND EXTRACT(YEAR FROM edu.usage_date) = p_year
          AND EXTRACT(MONTH FROM edu.usage_date) = p_month
    ),
    monthly_total AS (
        SELECT COALESCE(SUM(cmu.price), 0)::DECIMAL(15,2) AS t
        FROM company_monthly_usages cmu
        WHERE cmu.company_id = p_company_id
          AND EXTRACT(YEAR FROM cmu.from_date) = p_year
          AND EXTRACT(MONTH FROM cmu.from_date) = p_month
    ),
    daily_total AS (
        SELECT COALESCE(SUM(edu.price), 0)::DECIMAL(15,2) AS t
        FROM employee_daily_usages edu
        JOIN company_employees ce ON edu.employee_id = ce.id
        WHERE ce.company_id = p_company_id
          AND EXTRACT(YEAR FROM edu.usage_date) = p_year
          AND EXTRACT(MONTH FROM edu.usage_date) = p_month
    )
    SELECT
        p_company_id,
        v_cname,
        p_month,
        p_year,
        COALESCE(m.arr, '[]'::jsonb),
        COALESCE(d.arr, '[]'::jsonb),
        (COALESCE(mt.t, 0) + COALESCE(dt.t, 0))
    FROM monthly m
    CROSS JOIN daily d
    CROSS JOIN monthly_total mt
    CROSS JOIN daily_total dt;
END;
$$;

COMMENT ON FUNCTION get_company_service_details(INT, INT, INT) IS
'Chi tiết dịch vụ công ty theo tháng: dịch vụ theo tháng + theo ngày (từng lần sử dụng)';

-- =============================================================================
-- 3. Tổng thu chi tòa nhà theo tháng
-- =============================================================================
CREATE OR REPLACE FUNCTION get_building_finance(
    p_year INT,
    p_month INT
)
RETURNS TABLE (
    month INT,
    year INT,
    total_revenue DECIMAL(15,2),
    total_expense DECIMAL(15,2),
    net_profit DECIMAL(15,2),
    revenue_rent DECIMAL(15,2),
    revenue_services DECIMAL(15,2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH
    rev AS (
        SELECT COALESCE(SUM(i.total_amount), 0)::DECIMAL(15,2) AS total_revenue
        FROM invoices i
        WHERE EXTRACT(YEAR FROM i.from_date) = p_year
          AND EXTRACT(MONTH FROM i.from_date) = p_month
    ),
    -- Chi = tổng lương tháng (dùng function lương nhân viên tòa nhà)
    sal AS (
        SELECT COALESCE(SUM(s.total_salary), 0)::DECIMAL(15,2) AS total_expense
        FROM get_building_employee_salaries(p_year, p_month) s
    )
    SELECT
        p_month,
        p_year,
        r.total_revenue,
        s.total_expense,
        (r.total_revenue - s.total_expense),
        (r.total_revenue * 0.65),
        (r.total_revenue * 0.35)
    FROM rev r
    CROSS JOIN sal s;
END;
$$;

COMMENT ON FUNCTION get_building_finance(INT, INT) IS
'Tổng thu chi tòa nhà theo tháng: doanh thu từ hóa đơn, chi = tổng lương nhân viên tòa nhà trong tháng';

-- =============================================================================
-- 4. Chi tiết thu chi tòa nhà theo tháng (từng hóa đơn, từng nhân viên)
-- Thu: tất cả hóa đơn trong tháng (LEFT JOIN contract/company để có tên công ty khi có)
-- Chi: từng nhân viên tòa nhà và lương (get_building_employee_salaries)
-- =============================================================================
CREATE OR REPLACE FUNCTION get_building_finance_details(
    p_year INT,
    p_month INT
)
RETURNS TABLE (
    month INT,
    year INT,
    total_revenue DECIMAL(15,2),
    total_expense DECIMAL(15,2),
    net_profit DECIMAL(15,2),
    revenue_details JSONB,
    expense_details JSONB
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH
    -- Thu: tất cả hóa đơn trong tháng, có company khi rent_contracts.invoice_id = i.id
    rev_rows AS (
        SELECT
            COALESCE((
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'invoice_id', i.id,
                        'company_name', COALESCE(c.name, 'Không xác định'),
                        'tax_code', c.tax_code,
                        'total_amount', i.total_amount,
                        'from_date', i.from_date,
                        'to_date', i.to_date,
                        'status', i.status
                    )
                    ORDER BY i.from_date DESC
                )
                FROM invoices i
                LEFT JOIN (
                    SELECT DISTINCT ON (invoice_id) invoice_id, company_id
                    FROM rent_contracts
                    WHERE invoice_id IS NOT NULL
                    ORDER BY invoice_id
                ) rc ON rc.invoice_id = i.id
                LEFT JOIN companies c ON c.id = rc.company_id
                WHERE EXTRACT(YEAR FROM i.from_date) = p_year
                  AND EXTRACT(MONTH FROM i.from_date) = p_month
            ), '[]'::jsonb) AS arr,
            COALESCE((
                SELECT SUM(i.total_amount)
                FROM invoices i
                WHERE EXTRACT(YEAR FROM i.from_date) = p_year
                  AND EXTRACT(MONTH FROM i.from_date) = p_month
            ), 0)::DECIMAL(15,2) AS total_revenue
        FROM (SELECT 1) _one
    ),
    exp_rows AS (
        SELECT
            COALESCE((
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'employee_id', s.employee_id,
                        'full_name', s.full_name,
                        'position', s.role,
                        'base_salary', s.base_salary,
                        'bonus_rate', s.bonus_rate,
                        'service_revenue', s.monthly_revenue,
                        'total_salary', s.total_salary
                    )
                    ORDER BY s.total_salary DESC NULLS LAST
                )
                FROM get_building_employee_salaries(p_year, p_month) s
            ), '[]'::jsonb) AS arr,
            COALESCE((
                SELECT SUM(s.total_salary)
                FROM get_building_employee_salaries(p_year, p_month) s
            ), 0)::DECIMAL(15,2) AS total_expense
        FROM (SELECT 1) _one
    )
    SELECT
        p_month,
        p_year,
        rr.total_revenue,
        er.total_expense,
        (rr.total_revenue - er.total_expense),
        COALESCE(rr.arr, '[]'::jsonb),
        COALESCE(er.arr, '[]'::jsonb)
    FROM rev_rows rr
    CROSS JOIN exp_rows er;
END;
$$;

COMMENT ON FUNCTION get_building_finance_details(INT, INT) IS
'Chi tiết thu chi tòa nhà: từng hóa đơn (thu), từng nhân viên tòa nhà và lương (chi)';

DO $$
BEGIN
    RAISE NOTICE 'Migration 004: Functions get_company_monthly_costs, get_company_service_details, get_building_finance, get_building_finance_details created';
END $$;
