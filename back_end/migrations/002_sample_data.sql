-- Migration 002: Sample Data for Testing (2 months of data)
-- This file populates the database with sample data

-- Insert Offices
INSERT INTO offices (name, area, floor, position, base_price) VALUES
('P101', 50.00, 1, 'Góc đẹp, view đường', 15000000),
('P102', 60.00, 1, 'Giữa hành lang', 18000000),
('P201', 80.00, 2, 'View đẹp ra hồ', 25000000),
('P202', 75.00, 2, 'Góc tầng 2', 22000000),
('P301', 100.00, 3, 'Penthouse view đẹp', 35000000),
('P302', 90.00, 3, 'Hành lang tầng 3', 30000000);

-- Insert Companies
INSERT INTO companies (name, tax_code, email, address) VALUES
('Công ty TNHH Công Nghệ ABC', '0123456789', 'contact@abc.com', '123 Đường ABC, Hà Nội'),
('Công ty Cổ Phần XYZ', '0987654321', 'info@xyz.com', '456 Đường XYZ, Hà Nội'),
('Startup Innovation Ltd', '0112233445', 'hello@innovation.com', '789 Innovation St, Hanoi');

-- Insert Rent Contracts (Active contracts)
INSERT INTO rent_contracts (office_id, company_id, from_date, end_date, signed_date, rent_price, status) VALUES
(1, 1, '2025-11-01', '2026-10-31', '2025-10-25', 15000000, 'active'),
(2, 1, '2025-11-01', '2026-10-31', '2025-10-25', 18000000, 'active'),
(3, 2, '2025-12-01', '2026-11-30', '2025-11-20', 25000000, 'active'),
(5, 3, '2026-01-01', '2026-12-31', '2025-12-20', 35000000, 'active');

-- Insert Company Employees
INSERT INTO company_employees (company_id, full_name, job_title, phone_number, email, status) VALUES
-- Company 1 employees (15 people)
(1, 'Nguyễn Văn A', 'Giám đốc', '0901234567', 'a.nguyen@abc.com', 'working'),
(1, 'Trần Thị B', 'Trưởng phòng IT', '0901234568', 'b.tran@abc.com', 'working'),
(1, 'Lê Văn C', 'Lập trình viên', '0901234569', 'c.le@abc.com', 'working'),
(1, 'Phạm Thị D', 'Lập trình viên', '0901234570', 'd.pham@abc.com', 'working'),
(1, 'Hoàng Văn E', 'Designer', '0901234571', 'e.hoang@abc.com', 'working'),
(1, 'Đặng Thị F', 'Kế toán', '0901234572', 'f.dang@abc.com', 'working'),
(1, 'Vũ Văn G', 'Marketing', '0901234573', 'g.vu@abc.com', 'working'),
(1, 'Bùi Thị H', 'HR', '0901234574', 'h.bui@abc.com', 'working'),
(1, 'Đỗ Văn I', 'Sales', '0901234575', 'i.do@abc.com', 'working'),
(1, 'Mai Thị K', 'Sales', '0901234576', 'k.mai@abc.com', 'working'),
(1, 'Lý Văn L', 'Lập trình viên', '0901234577', 'l.ly@abc.com', 'working'),
(1, 'Trịnh Thị M', 'Tester', '0901234578', 'm.trinh@abc.com', 'working'),
(1, 'Phan Văn N', 'DevOps', '0901234579', 'n.phan@abc.com', 'working'),
(1, 'Đinh Thị O', 'Business Analyst', '0901234580', 'o.dinh@abc.com', 'working'),
(1, 'Dương Văn P', 'Project Manager', '0901234581', 'p.duong@abc.com', 'working'),

-- Company 2 employees (8 people)
(2, 'Võ Văn Q', 'CEO', '0902234567', 'q.vo@xyz.com', 'working'),
(2, 'Tô Thị R', 'CFO', '0902234568', 'r.to@xyz.com', 'working'),
(2, 'Lưu Văn S', 'CTO', '0902234569', 's.luu@xyz.com', 'working'),
(2, 'Hồ Thị T', 'Developer', '0902234570', 't.ho@xyz.com', 'working'),
(2, 'Châu Văn U', 'Developer', '0902234571', 'u.chau@xyz.com', 'working'),
(2, 'Cao Thị V', 'Designer', '0902234572', 'v.cao@xyz.com', 'working'),
(2, 'Tạ Văn W', 'Marketing', '0902234573', 'w.ta@xyz.com', 'working'),
(2, 'Ông Thị X', 'Accountant', '0902234574', 'x.ong@xyz.com', 'working'),

-- Company 3 employees (5 people)
(3, 'La Văn Y', 'Founder', '0903234567', 'y.la@innovation.com', 'working'),
(3, 'Nghiêm Thị Z', 'Co-founder', '0903234568', 'z.nghiem@innovation.com', 'working'),
(3, 'Từ Văn AA', 'Tech Lead', '0903234569', 'aa.tu@innovation.com', 'working'),
(3, 'Sầm Thị BB', 'Full-stack Dev', '0903234570', 'bb.sam@innovation.com', 'working'),
(3, 'Ung Văn CC', 'Product Manager', '0903234571', 'cc.ung@innovation.com', 'working');

-- Insert Building Employees
INSERT INTO building_employees (first_name, last_name, phone_number, role, email, base_salary, hire_date, status) VALUES
('Nguyễn', 'Minh', '0911111111', 'manager', 'minh.nguyen@building.com', 20000000, '2024-01-01', 'active'),
('Trần', 'Hương', '0911111112', 'staff', 'huong.tran@building.com', 8000000, '2024-02-01', 'active'),
('Lê', 'Bình', '0911111113', 'staff', 'binh.le@building.com', 8000000, '2024-02-01', 'active'),
('Phạm', 'Cường', '0911111114', 'supervisor', 'cuong.pham@building.com', 15000000, '2024-01-15', 'active'),
('Hoàng', 'Lan', '0911111115', 'staff', 'lan.hoang@building.com', 7500000, '2024-03-01', 'active');

-- Insert Services
INSERT INTO services (name, description, base_price, price_method) VALUES
('Vệ sinh', 'Dịch vụ vệ sinh văn phòng hàng ngày', 100000, 'per_sqm'),
('An ninh', 'Dịch vụ bảo vệ 24/7', 50000, 'per_head'),
('Gửi xe', 'Dịch vụ gửi xe theo ngày', 15000, 'fixed'),
('Ăn trưa', 'Suất cơm văn phòng', 50000, 'fixed'),
('Bảo trì thiết bị', 'Bảo trì hệ thống điện, nước, điều hòa', 500000, 'per_sqm');

-- Insert Salary Rules
INSERT INTO salary_rules (bonus_rate, status) VALUES
(0.05, 'active'),  -- 5% bonus for managers
(0.03, 'active'),  -- 3% bonus for supervisors
(0.02, 'active');  -- 2% bonus for staff

-- Insert Service Role Rules
INSERT INTO service_role_rules (service_id, role, salary_rule_id) VALUES
(1, 'manager', 1),   -- Vệ sinh - manager - 5%
(1, 'staff', 3),     -- Vệ sinh - staff - 2%
(2, 'supervisor', 2), -- An ninh - supervisor - 3%
(2, 'staff', 3),     -- An ninh - staff - 2%
(5, 'manager', 1);   -- Bảo trì - manager - 5%

-- Insert Service Subscribers (Assign employees to services)
INSERT INTO service_subscribers (service_id, employee_id, service_role_rules_id, from_date) VALUES
(1, 1, 1, '2025-11-01'),  -- Manager Minh quản lý vệ sinh
(1, 2, 2, '2025-11-01'),  -- Staff Hương làm vệ sinh
(1, 3, 2, '2025-11-01'),  -- Staff Bình làm vệ sinh
(2, 4, 3, '2025-11-01'),  -- Supervisor Cường quản lý an ninh
(2, 5, 4, '2025-11-01');  -- Staff Lan làm an ninh

-- Insert Company Monthly Usages (December 2025 & January 2026)
-- Company 1 (ABC) - 15 employees, 110 m2 total (P101: 50m2 + P102: 60m2)
INSERT INTO company_monthly_usages (company_id, service_id, from_date, to_date, quantity, price) VALUES
-- December 2025
(1, 1, '2025-12-01', '2025-12-31', 15, 11000000),  -- Vệ sinh (110m2 * 100k)
(1, 2, '2025-12-01', '2025-12-31', 15, 750000),    -- An ninh (15 người * 50k)
-- January 2026
(1, 1, '2026-01-01', '2026-01-31', 15, 11000000),  -- Vệ sinh
(1, 2, '2026-01-01', '2026-01-31', 15, 750000),    -- An ninh

-- Company 2 (XYZ) - 8 employees, 80 m2 (P201)
(2, 1, '2025-12-01', '2025-12-31', 8, 8000000),    -- Vệ sinh (80m2 * 100k)
(2, 2, '2025-12-01', '2025-12-31', 8, 400000),     -- An ninh (8 người * 50k)
(2, 1, '2026-01-01', '2026-01-31', 8, 8000000),    -- Vệ sinh
(2, 2, '2026-01-01', '2026-01-31', 8, 400000),     -- An ninh

-- Company 3 (Innovation) - 5 employees, 100 m2 (P301)
(3, 1, '2026-01-01', '2026-01-31', 5, 10000000),   -- Vệ sinh (100m2 * 100k)
(3, 2, '2026-01-01', '2026-01-31', 5, 250000);     -- An ninh (5 người * 50k)

-- Insert Employee Daily Usages (Parking & Meals for December 2025 - sample 10 days)
-- Company 1 employees
INSERT INTO employee_daily_usages (employee_id, service_id, usage_date, price, service_type) VALUES
-- Parking (service_id: 3)
(1, 3, '2025-12-01', 15000, 'parking'),
(1, 3, '2025-12-02', 15000, 'parking'),
(2, 3, '2025-12-01', 15000, 'parking'),
(3, 3, '2025-12-01', 15000, 'parking'),
-- Meals (service_id: 4)
(1, 4, '2025-12-01', 50000, 'meal'),
(1, 4, '2025-12-02', 50000, 'meal'),
(2, 4, '2025-12-01', 50000, 'meal'),
(3, 4, '2025-12-01', 50000, 'meal'),
(4, 4, '2025-12-01', 50000, 'meal'),
(5, 4, '2025-12-01', 50000, 'meal');

-- Insert sample invoices
INSERT INTO invoices (from_date, to_date, total_amount, status, note) VALUES
('2025-12-01', '2025-12-31', 12500000, 'paid', 'Hóa đơn tháng 12/2025 - Công ty ABC'),
('2025-12-01', '2025-12-31', 8400000, 'paid', 'Hóa đơn tháng 12/2025 - Công ty XYZ'),
('2026-01-01', '2026-01-31', 11750000, 'unpaid', 'Hóa đơn tháng 01/2026 - Công ty ABC'),
('2026-01-01', '2026-01-31', 8400000, 'unpaid', 'Hóa đơn tháng 01/2026 - Công ty XYZ'),
('2026-01-01', '2026-01-31', 10250000, 'unpaid', 'Hóa đơn tháng 01/2026 - Công ty Innovation');

DO $$
BEGIN
    RAISE NOTICE '✅ Migration 002: Sample data inserted successfully';
    RAISE NOTICE 'Inserted: 6 offices, 3 companies, 4 contracts, 28 employees';
    RAISE NOTICE 'Sample data covers December 2025 and January 2026';
END $$;
