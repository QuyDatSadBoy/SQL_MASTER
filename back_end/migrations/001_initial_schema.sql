-- Migration 001: Initial Schema for Office Building Management System
-- Student: Tran Quy Dat - PTIT
-- Date: 2026-02-06

-- Enable UUID extension if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Quản lý Văn phòng
CREATE TABLE IF NOT EXISTS offices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    area DECIMAL(10,2) NOT NULL CHECK (area > 0),
    floor INT NOT NULL,
    position VARCHAR(100),
    base_price DECIMAL(15,2) NOT NULL CHECK (base_price > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Quản lý Công ty khách thuê
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tax_code VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Hóa đơn (tách ra trước vì được reference bởi nhiều bảng)
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    created_date DATE DEFAULT CURRENT_DATE,
    pay_day DATE,
    from_date DATE,
    to_date DATE,
    total_amount DECIMAL(15,2),
    status VARCHAR(20) DEFAULT 'unpaid' CHECK (status IN ('paid', 'unpaid', 'overdue')),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Hợp đồng thuê
CREATE TABLE IF NOT EXISTS rent_contracts (
    id SERIAL PRIMARY KEY,
    office_id INT NOT NULL REFERENCES offices(id) ON DELETE CASCADE,
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    invoice_id INT REFERENCES invoices(id) ON DELETE SET NULL,
    from_date DATE NOT NULL,
    end_date DATE NOT NULL,
    signed_date DATE DEFAULT CURRENT_DATE,
    rent_price DECIMAL(15,2) NOT NULL CHECK (rent_price > 0),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'terminated')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT date_range_check CHECK (end_date > from_date)
);

-- Create index for checking office availability
CREATE INDEX IF NOT EXISTS idx_rent_contracts_office_dates 
ON rent_contracts(office_id, from_date, end_date, status);

-- 5. Nhân viên công ty
CREATE TABLE IF NOT EXISTS company_employees (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'working' CHECK (status IN ('working', 'resigned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Nhân viên tòa nhà
CREATE TABLE IF NOT EXISTS building_employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    role VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255),
    date_of_birth DATE,
    base_salary DECIMAL(15,2),
    hire_date DATE,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Dịch vụ
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(15,2),
    price_method VARCHAR(50) CHECK (price_method IN ('per_sqm', 'per_head', 'fixed', 'custom')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Quy tắc lương
CREATE TABLE IF NOT EXISTS salary_rules (
    id SERIAL PRIMARY KEY,
    bonus_rate FLOAT DEFAULT 0 CHECK (bonus_rate >= 0 AND bonus_rate <= 1),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Quy định lương theo Vai trò & Dịch vụ (BCNF)
CREATE TABLE IF NOT EXISTS service_role_rules (
    id SERIAL PRIMARY KEY,
    service_id INT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    salary_rule_id INT NOT NULL REFERENCES salary_rules(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(service_id, role)
);

-- 10. Phân công nhân viên tòa nhà làm dịch vụ (BCNF)
CREATE TABLE IF NOT EXISTS service_subscribers (
    id SERIAL PRIMARY KEY,
    service_id INT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    employee_id INT NOT NULL REFERENCES building_employees(employee_id) ON DELETE CASCADE,
    service_role_rules_id INT NOT NULL REFERENCES service_role_rules(id) ON DELETE CASCADE,
    from_date DATE NOT NULL,
    end_date DATE,
    invoice_id INT REFERENCES invoices(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT subscriber_date_check CHECK (end_date IS NULL OR end_date > from_date)
);

-- 11. Dịch vụ dùng theo tháng (Công ty)
CREATE TABLE IF NOT EXISTS company_monthly_usages (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    service_id INT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    invoice_id INT REFERENCES invoices(id) ON DELETE SET NULL,
    from_date DATE,
    to_date DATE,
    quantity INT,
    price DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_company_monthly_usages_company_date 
ON company_monthly_usages(company_id, from_date);

-- 12. Dịch vụ dùng theo ngày (Nhân viên công ty)
CREATE TABLE IF NOT EXISTS employee_daily_usages (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES company_employees(id) ON DELETE CASCADE,
    invoice_id INT REFERENCES invoices(id) ON DELETE SET NULL,
    service_id INT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    usage_date DATE NOT NULL,
    price DECIMAL(15,2),
    service_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_employee_daily_usages_date 
ON employee_daily_usages(employee_id, usage_date);

-- Create trigger function for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables
CREATE TRIGGER update_offices_updated_at BEFORE UPDATE ON offices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rent_contracts_updated_at BEFORE UPDATE ON rent_contracts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_company_employees_updated_at BEFORE UPDATE ON company_employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_building_employees_updated_at BEFORE UPDATE ON building_employees
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_salary_rules_updated_at BEFORE UPDATE ON salary_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_role_rules_updated_at BEFORE UPDATE ON service_role_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_service_subscribers_updated_at BEFORE UPDATE ON service_subscribers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_company_monthly_usages_updated_at BEFORE UPDATE ON company_monthly_usages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_employee_daily_usages_updated_at BEFORE UPDATE ON employee_daily_usages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Migration 001: Initial schema created successfully';
END $$;
