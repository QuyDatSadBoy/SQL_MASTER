-- Migration 002: Sample Data for Testing (2 months of data)
-- This file populates the database with sample data

-- Insert Offices
INSERT INTO offices (name, area, floor, position, base_price) VALUES
('P101', 50.00, 1, 'Góc đẹp, view đường', 15000000),
('P102', 60.00, 1, 'Giữa hành lang', 18000000),
('P201', 80.00, 2, 'View đẹp ra hồ', 25000000),
('P202', 75.00, 2, 'Góc tầng 2', 22000000),
('P301', 100.00, 3, 'Penthouse view đẹp', 35000000),
('P302', 90.00, 3, 'Hành lang tầng 3', 30000000),
('P103', 55.00, 1, 'Cuối hành lang tầng 1', 16000000),
('P203', 70.00, 2, 'View sân trong', 21000000),
('P303', 85.00, 3, 'Góc tầng 3', 28000000);

-- Insert Companies
INSERT INTO companies (name, tax_code, email, address) VALUES
('Công ty TNHH Công Nghệ ABC', '0123456789', 'contact@abc.com', '123 Đường ABC, Hà Nội'),
('Công ty Cổ Phần XYZ', '0987654321', 'info@xyz.com', '456 Đường XYZ, Hà Nội'),
('Startup Innovation Ltd', '0112233445', 'hello@innovation.com', '789 Innovation St, Hanoi'),
('Công ty TNHH Logistics Đông Nam', '0555666777', 'contact@logistics-dn.com', '100 Đường Logistics, Hà Nội'),
('Công ty Cổ Phần Fintech VN', '0888999000', 'support@fintech-vn.com', '200 Tower Fintech, Hà Nội');

-- Insert Rent Contracts (Active contracts + 1 expired for history)
INSERT INTO rent_contracts (office_id, company_id, from_date, end_date, signed_date, rent_price, status) VALUES
(1, 1, '2025-11-01', '2026-10-31', '2025-10-25', 15000000, 'active'),
(2, 1, '2025-11-01', '2026-10-31', '2025-10-25', 18000000, 'active'),
(3, 2, '2025-12-01', '2026-11-30', '2025-11-20', 25000000, 'active'),
(5, 3, '2026-01-01', '2026-12-31', '2025-12-20', 35000000, 'active'),
(7, 4, '2025-10-01', '2026-09-30', '2025-09-15', 16000000, 'active'),
(8, 5, '2026-02-01', '2027-01-31', '2026-01-25', 21000000, 'active'),
(6, 2, '2024-06-01', '2025-05-31', '2024-05-20', 28000000, 'expired');

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
(3, 'Ung Văn CC', 'Product Manager', '0903234571', 'cc.ung@innovation.com', 'working'),

-- Company 4 employees (Logistics - 6 people)
(4, 'Hà Văn DD', 'Giám đốc vận hành', '0904555567', 'dd.ha@logistics-dn.com', 'working'),
(4, 'Khổng Thị EE', 'Trưởng phòng kho', '0904555568', 'ee.khong@logistics-dn.com', 'working'),
(4, 'Lâm Văn FF', 'Nhân viên logistics', '0904555569', 'ff.lam@logistics-dn.com', 'working'),
(4, 'Mạch Thị GG', 'Kế toán', '0904555570', 'gg.mach@logistics-dn.com', 'working'),
(4, 'Ninh Văn HH', 'Tài xế', '0904555571', 'hh.ninh@logistics-dn.com', 'working'),
(4, 'Quách Thị II', 'Customer Service', '0904555572', 'ii.quach@logistics-dn.com', 'working'),

-- Company 5 employees (Fintech - 7 people)
(5, 'Tiêu Văn JJ', 'CEO', '0905666677', 'jj.tieu@fintech-vn.com', 'working'),
(5, 'Vi Thị KK', 'CFO', '0905666678', 'kk.vi@fintech-vn.com', 'working'),
(5, 'Xuyên Văn LL', 'CTO', '0905666679', 'll.xuyen@fintech-vn.com', 'working'),
(5, 'Yên Thị MM', 'Backend Dev', '0905666680', 'mm.yen@fintech-vn.com', 'working'),
(5, 'Zung Văn NN', 'Frontend Dev', '0905666681', 'nn.zung@fintech-vn.com', 'working'),
(5, 'Ân Thị OO', 'Compliance', '0905666682', 'oo.an@fintech-vn.com', 'working'),
(5, 'Bành Văn PP', 'Marketing', '0905666683', 'pp.banh@fintech-vn.com', 'working'),
-- Thêm nhân viên Company 1 (3 người)
(1, 'Cù Văn QQ', 'Intern', '0901234582', 'qq.cu@abc.com', 'working'),
(1, 'Dương Thị RR', 'Lập trình viên', '0901234583', 'rr.duong@abc.com', 'working'),
(1, 'Hứa Văn SS', 'Tester', '0901234584', 'ss.hua@abc.com', 'resigned'),
-- Thêm nhân viên Company 2 (2 người)
(2, 'Kha Thị TT', 'HR', '0902234575', 'tt.kha@xyz.com', 'working'),
(2, 'Lục Văn UU', 'Developer', '0902234576', 'uu.luc@xyz.com', 'working'),
-- Thêm nhân viên Company 3 (2 người)
(3, 'Mã Thị VV', 'Designer', '0903234572', 'vv.ma@innovation.com', 'working'),
(3, 'Ngụy Văn WW', 'DevOps', '0903234573', 'ww.nguy@innovation.com', 'working');

-- Insert Building Employees
INSERT INTO building_employees (first_name, last_name, phone_number, role, email, base_salary, hire_date, status) VALUES
('Nguyễn', 'Minh', '0911111111', 'manager', 'minh.nguyen@building.com', 20000000, '2024-01-01', 'active'),
('Trần', 'Hương', '0911111112', 'staff', 'huong.tran@building.com', 8000000, '2024-02-01', 'active'),
('Lê', 'Bình', '0911111113', 'staff', 'binh.le@building.com', 8000000, '2024-02-01', 'active'),
('Phạm', 'Cường', '0911111114', 'supervisor', 'cuong.pham@building.com', 15000000, '2024-01-15', 'active'),
('Hoàng', 'Lan', '0911111115', 'staff', 'lan.hoang@building.com', 7500000, '2024-03-01', 'active'),
('Đặng', 'Nam', '0911111116', 'staff', 'nam.dang@building.com', 7800000, '2024-04-01', 'active'),
('Vũ', 'Phương', '0911111117', 'supervisor', 'phuong.vu@building.com', 14000000, '2024-02-15', 'active'),
('Bùi', 'Tâm', '0911111118', 'staff', 'tam.bui@building.com', 7600000, '2024-05-01', 'active'),
('Đỗ', 'Hùng', '0911111119', 'staff', 'hung.do@building.com', 7700000, '2024-05-15', 'active'),
('Mai', 'Thảo', '0911111120', 'staff', 'thao.mai@building.com', 7900000, '2024-06-01', 'active');

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
(5, 'manager', 1),   -- Bảo trì - manager - 5%
(3, 'staff', 3),     -- Gửi xe - staff - 2%
(4, 'staff', 3);     -- Ăn trưa - staff - 2%

-- Insert Service Subscribers (Assign employees to services)
INSERT INTO service_subscribers (service_id, employee_id, service_role_rules_id, from_date) VALUES
(1, 1, 1, '2025-11-01'),  -- Manager Minh quản lý vệ sinh
(1, 2, 2, '2025-11-01'),  -- Staff Hương làm vệ sinh
(1, 3, 2, '2025-11-01'),  -- Staff Bình làm vệ sinh
(2, 4, 3, '2025-11-01'),  -- Supervisor Cường quản lý an ninh
(2, 5, 4, '2025-11-01'),  -- Staff Lan làm an ninh
(1, 6, 2, '2025-10-01'),  -- Staff Nam làm vệ sinh (từ tháng 10)
(2, 7, 3, '2026-01-01'),  -- Supervisor Phương quản lý an ninh
(1, 8, 2, '2025-11-01'),  -- Staff Tâm làm vệ sinh
(1, 9, 2, '2025-12-01'),  -- Staff Hùng làm vệ sinh
(2, 10, 4, '2026-02-01'); -- Staff Thảo làm an ninh

-- Insert Company Monthly Usages (December 2025 & January 2026 & February 2026)
-- Company 1 (ABC) - 15 employees, 110 m2 total (P101: 50m2 + P102: 60m2)
INSERT INTO company_monthly_usages (company_id, service_id, from_date, to_date, quantity, price) VALUES
-- December 2025
(1, 1, '2025-12-01', '2025-12-31', 15, 11000000),  -- Vệ sinh (110m2 * 100k)
(1, 2, '2025-12-01', '2025-12-31', 15, 750000),    -- An ninh (15 người * 50k)
-- January 2026
(1, 1, '2026-01-01', '2026-01-31', 15, 11000000),  -- Vệ sinh
(1, 2, '2026-01-01', '2026-01-31', 15, 750000),    -- An ninh
-- February 2026
(1, 1, '2026-02-01', '2026-02-28', 17, 11000000),  -- Vệ sinh (17 người sau khi thêm)
(1, 2, '2026-02-01', '2026-02-28', 17, 850000),    -- An ninh
(1, 5, '2026-02-01', '2026-02-28', 110, 55000000), -- Bảo trì (110m2 * 500k)

-- Company 2 (XYZ) - 8 employees, 80 m2 (P201)
(2, 1, '2025-12-01', '2025-12-31', 8, 8000000),    -- Vệ sinh (80m2 * 100k)
(2, 2, '2025-12-01', '2025-12-31', 8, 400000),     -- An ninh (8 người * 50k)
(2, 1, '2026-01-01', '2026-01-31', 8, 8000000),    -- Vệ sinh
(2, 2, '2026-01-01', '2026-01-31', 8, 400000),     -- An ninh
(2, 1, '2026-02-01', '2026-02-28', 10, 8000000),   -- Vệ sinh (10 người)
(2, 2, '2026-02-01', '2026-02-28', 10, 500000),    -- An ninh
(2, 5, '2026-02-01', '2026-02-28', 80, 40000000),  -- Bảo trì (80m2 * 500k)

-- Company 3 (Innovation) - 5 employees, 100 m2 (P301)
(3, 1, '2026-01-01', '2026-01-31', 5, 10000000),   -- Vệ sinh (100m2 * 100k)
(3, 2, '2026-01-01', '2026-01-31', 5, 250000),     -- An ninh (5 người * 50k)
(3, 1, '2026-02-01', '2026-02-28', 7, 10000000),   -- Vệ sinh (7 người)
(3, 2, '2026-02-01', '2026-02-28', 7, 350000),     -- An ninh
(3, 5, '2026-02-01', '2026-02-28', 100, 50000000), -- Bảo trì (100m2 * 500k)

-- Company 4 (Logistics) - 6 employees, 55 m2 (P103)
(4, 1, '2025-12-01', '2025-12-31', 6, 5500000),   -- Vệ sinh (55m2 * 100k)
(4, 2, '2025-12-01', '2025-12-31', 6, 300000),     -- An ninh (6 người * 50k)
(4, 1, '2026-01-01', '2026-01-31', 6, 5500000),
(4, 2, '2026-01-01', '2026-01-31', 6, 300000),
(4, 1, '2026-02-01', '2026-02-28', 6, 5500000),
(4, 2, '2026-02-01', '2026-02-28', 6, 300000),
(4, 5, '2026-02-01', '2026-02-28', 55, 27500000),  -- Bảo trì (55m2 * 500k)

-- Company 5 (Fintech) - 7 employees, 70 m2 (P203) - từ 02/2026
(5, 1, '2026-02-01', '2026-02-28', 7, 7000000),   -- Vệ sinh (70m2 * 100k)
(5, 2, '2026-02-01', '2026-02-28', 7, 350000);     -- An ninh (7 người * 50k)

-- Insert Employee Daily Usages (Parking & Meals - Dec 2025, Jan–Feb 2026, nhiều nhân viên)
INSERT INTO employee_daily_usages (employee_id, service_id, usage_date, price, service_type) VALUES
-- December 2025 - Company 1 (employees 1-10): parking + meal nhiều ngày
(1, 3, '2025-12-01', 15000, 'parking'), (1, 3, '2025-12-02', 15000, 'parking'), (1, 3, '2025-12-03', 15000, 'parking'), (1, 3, '2025-12-04', 15000, 'parking'), (1, 3, '2025-12-05', 15000, 'parking'), (1, 3, '2025-12-08', 15000, 'parking'), (1, 3, '2025-12-09', 15000, 'parking'), (1, 3, '2025-12-10', 15000, 'parking'),
(1, 4, '2025-12-01', 50000, 'meal'), (1, 4, '2025-12-02', 50000, 'meal'), (1, 4, '2025-12-03', 50000, 'meal'), (1, 4, '2025-12-04', 50000, 'meal'), (1, 4, '2025-12-05', 50000, 'meal'), (1, 4, '2025-12-08', 50000, 'meal'), (1, 4, '2025-12-09', 50000, 'meal'), (1, 4, '2025-12-10', 50000, 'meal'),
(2, 3, '2025-12-01', 15000, 'parking'), (2, 3, '2025-12-02', 15000, 'parking'), (2, 3, '2025-12-03', 15000, 'parking'), (2, 4, '2025-12-01', 50000, 'meal'), (2, 4, '2025-12-02', 50000, 'meal'), (2, 4, '2025-12-03', 50000, 'meal'),
(3, 3, '2025-12-01', 15000, 'parking'), (3, 3, '2025-12-04', 15000, 'parking'), (3, 4, '2025-12-01', 50000, 'meal'), (3, 4, '2025-12-02', 50000, 'meal'), (3, 4, '2025-12-04', 50000, 'meal'), (3, 4, '2025-12-05', 50000, 'meal'),
(4, 4, '2025-12-01', 50000, 'meal'), (4, 4, '2025-12-02', 50000, 'meal'), (4, 4, '2025-12-03', 50000, 'meal'), (5, 4, '2025-12-01', 50000, 'meal'), (5, 4, '2025-12-02', 50000, 'meal'),
(6, 3, '2025-12-02', 15000, 'parking'), (6, 4, '2025-12-02', 50000, 'meal'), (7, 3, '2025-12-03', 15000, 'parking'), (7, 4, '2025-12-03', 50000, 'meal'), (8, 4, '2025-12-04', 50000, 'meal'), (9, 4, '2025-12-05', 50000, 'meal'), (10, 3, '2025-12-05', 15000, 'parking'), (10, 4, '2025-12-05', 50000, 'meal'),
-- December 2025 - Company 2 (employees 16-20)
(16, 3, '2025-12-01', 15000, 'parking'), (16, 4, '2025-12-01', 50000, 'meal'), (16, 3, '2025-12-02', 15000, 'parking'), (16, 4, '2025-12-02', 50000, 'meal'), (17, 3, '2025-12-01', 15000, 'parking'), (17, 4, '2025-12-01', 50000, 'meal'), (18, 4, '2025-12-03', 50000, 'meal'), (19, 4, '2025-12-03', 50000, 'meal'), (20, 3, '2025-12-04', 15000, 'parking'), (20, 4, '2025-12-04', 50000, 'meal'),
-- December 2025 - Company 3 (employees 24-26)
(24, 3, '2025-12-02', 15000, 'parking'), (24, 4, '2025-12-02', 50000, 'meal'), (25, 4, '2025-12-02', 50000, 'meal'), (26, 3, '2025-12-03', 15000, 'parking'), (26, 4, '2025-12-03', 50000, 'meal'),
-- December 2025 - Company 4 (employees 29-34)
(29, 3, '2025-12-01', 15000, 'parking'), (29, 4, '2025-12-01', 50000, 'meal'), (29, 3, '2025-12-02', 15000, 'parking'), (29, 4, '2025-12-02', 50000, 'meal'), (30, 3, '2025-12-01', 15000, 'parking'), (30, 4, '2025-12-01', 50000, 'meal'), (31, 4, '2025-12-03', 50000, 'meal'), (32, 4, '2025-12-03', 50000, 'meal'), (33, 3, '2025-12-04', 15000, 'parking'), (33, 4, '2025-12-04', 50000, 'meal'),
-- January 2026 - Company 1
(1, 3, '2026-01-06', 15000, 'parking'), (1, 4, '2026-01-06', 50000, 'meal'), (1, 3, '2026-01-07', 15000, 'parking'), (1, 4, '2026-01-07', 50000, 'meal'), (1, 3, '2026-01-08', 15000, 'parking'), (1, 4, '2026-01-08', 50000, 'meal'), (1, 3, '2026-01-09', 15000, 'parking'), (1, 4, '2026-01-09', 50000, 'meal'), (1, 3, '2026-01-10', 15000, 'parking'), (1, 4, '2026-01-10', 50000, 'meal'),
(2, 3, '2026-01-06', 15000, 'parking'), (2, 4, '2026-01-06', 50000, 'meal'), (2, 4, '2026-01-07', 50000, 'meal'), (3, 4, '2026-01-08', 50000, 'meal'), (4, 4, '2026-01-08', 50000, 'meal'), (5, 3, '2026-01-09', 15000, 'parking'), (5, 4, '2026-01-09', 50000, 'meal'), (6, 4, '2026-01-10', 50000, 'meal'), (7, 3, '2026-01-10', 15000, 'parking'), (7, 4, '2026-01-10', 50000, 'meal'),
-- January 2026 - Company 2, 3, 4
(16, 3, '2026-01-06', 15000, 'parking'), (16, 4, '2026-01-06', 50000, 'meal'), (17, 4, '2026-01-07', 50000, 'meal'), (24, 3, '2026-01-08', 15000, 'parking'), (24, 4, '2026-01-08', 50000, 'meal'), (29, 3, '2026-01-09', 15000, 'parking'), (29, 4, '2026-01-09', 50000, 'meal'), (30, 4, '2026-01-10', 50000, 'meal'),
-- February 2026 - Company 1, 2, 3, 4, 5
(1, 3, '2026-02-02', 15000, 'parking'), (1, 4, '2026-02-02', 50000, 'meal'), (1, 3, '2026-02-03', 15000, 'parking'), (1, 4, '2026-02-03', 50000, 'meal'), (2, 4, '2026-02-02', 50000, 'meal'), (16, 3, '2026-02-03', 15000, 'parking'), (16, 4, '2026-02-03', 50000, 'meal'), (24, 4, '2026-02-04', 50000, 'meal'), (29, 4, '2026-02-04', 50000, 'meal'), (35, 3, '2026-02-05', 15000, 'parking'), (35, 4, '2026-02-05', 50000, 'meal'), (36, 4, '2026-02-05', 50000, 'meal');

-- Insert sample invoices
INSERT INTO invoices (from_date, to_date, total_amount, status, note) VALUES
('2025-12-01', '2025-12-31', 12500000, 'paid', 'Hóa đơn tháng 12/2025 - Công ty ABC'),
('2025-12-01', '2025-12-31', 8400000, 'paid', 'Hóa đơn tháng 12/2025 - Công ty XYZ'),
('2026-01-01', '2026-01-31', 11750000, 'paid', 'Hóa đơn tháng 01/2026 - Công ty ABC'),
('2026-01-01', '2026-01-31', 8400000, 'paid', 'Hóa đơn tháng 01/2026 - Công ty XYZ'),
('2026-01-01', '2026-01-31', 10250000, 'paid', 'Hóa đơn tháng 01/2026 - Công ty Innovation'),
('2025-12-01', '2025-12-31', 5800000, 'paid', 'Hóa đơn tháng 12/2025 - Công ty Logistics'),
('2026-01-01', '2026-01-31', 5800000, 'paid', 'Hóa đơn tháng 01/2026 - Công ty Logistics'),
('2026-02-01', '2026-02-28', 7350000, 'paid', 'Hóa đơn tháng 02/2026 - Công ty Fintech'),
-- Hóa đơn tháng 02/2026 cho các công ty 1, 2, 3, 4 (có thêm dịch vụ bảo trì)
('2026-02-01', '2026-02-28', 66850000, 'paid', 'Hóa đơn tháng 02/2026 - Công ty ABC (có bảo trì)'),
('2026-02-01', '2026-02-28', 48500000, 'paid', 'Hóa đơn tháng 02/2026 - Công ty XYZ (có bảo trì)'),
('2026-02-01', '2026-02-28', 60350000, 'paid', 'Hóa đơn tháng 02/2026 - Công ty Innovation (có bảo trì)'),
('2026-02-01', '2026-02-28', 33300000, 'paid', 'Hóa đơn tháng 02/2026 - Công ty Logistics (có bảo trì)'),
('2025-11-01', '2025-11-30', 28000000, 'paid', 'Hóa đơn tháng 11/2025 - Công ty XYZ (quá hạn)');

-- Liên kết hóa đơn tháng 2/2026 với hợp đồng thuê (để Chi tiết thu nhập hiển thị đúng tên công ty)
-- Mỗi hợp đồng chỉ lưu 1 invoice_id; gán theo hóa đơn tháng 2/2026 (invoice 8-12) và 1 hóa đơn quá hạn (13)
-- Contract id: 1,2=ABC, 3=XYZ, 4=Innovation, 5=Logistics, 6=Fintech, 7=XYZ (expired)
UPDATE rent_contracts SET invoice_id = 9 WHERE id = 1;   -- Feb 2026 ABC (66.850.000)
UPDATE rent_contracts SET invoice_id = 10 WHERE id = 3;  -- Feb 2026 XYZ (48.500.000)
UPDATE rent_contracts SET invoice_id = 11 WHERE id = 4;  -- Feb 2026 Innovation (60.350.000)
UPDATE rent_contracts SET invoice_id = 12 WHERE id = 5;  -- Feb 2026 Logistics (33.300.000)
UPDATE rent_contracts SET invoice_id = 8 WHERE id = 6;   -- Feb 2026 Fintech (7.350.000)
UPDATE rent_contracts SET invoice_id = 13 WHERE id = 7;  -- Nov 2025 XYZ overdue

DO $$
BEGIN
    RAISE NOTICE '✅ Migration 002: Sample data inserted successfully';
    RAISE NOTICE 'Inserted: 9 offices, 5 companies, 7 contracts, 48 company employees, 10 building employees';
    RAISE NOTICE 'Sample data: company_monthly_usages (incl. Bảo trì), employee_daily_usages (parking/meal), 13 invoices';
    RAISE NOTICE 'Covers December 2025, January 2026, February 2026';
END $$;
