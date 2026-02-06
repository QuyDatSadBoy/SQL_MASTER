# BÁO CÁO KIỂM THỬ BACKEND

**Ngày**: 06/02/2026  
**Project**: Office Building Management System  
**Student**: Trần Quý Đạt - PTIT  
**Stack**: FastAPI + PostgreSQL + asyncpg (SQL thuần 100%)

---

## 1. TỔNG QUAN

| Hạng mục | Kết quả |
|----------|---------|
| Tổng số test | 98 |
| PASS | 98 |
| FAIL | 0 |
| Tỉ lệ | 100% |
| Server | http://localhost:8222 |
| Database | PostgreSQL 17.7 |

---

## 2. KẾT QUẢ CHI TIẾT THEO NHÓM API

### Test 1-3: Offices CRUD
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/offices | Danh sách văn phòng | PASS |
| GET /api/offices/:id | Chi tiết văn phòng | PASS |
| POST /api/offices | Tạo văn phòng | PASS |

**Dữ liệu xác minh**: 6 văn phòng (P101, P102, P201, P202, P301, P302)

### Test 4-6: Companies CRUD
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/companies | Danh sách công ty | PASS |
| GET /api/companies/:id | Chi tiết công ty | PASS |
| POST /api/companies | Tạo công ty | PASS |

**Dữ liệu xác minh**: 3 công ty (Công ty TNHH Công Nghệ ABC, Công ty Cổ Phần XYZ, Startup Innovation Ltd)

### Test 7-8: Contracts
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/contracts | Danh sách hợp đồng | PASS |
| Contract fields | Kiểm tra fields | PASS |

### Test 9-11: Monthly Costs
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/companies/:id/monthly-costs | Chi phí tháng | PASS |
| Cost fields | rent_cost, total_service_cost, total_cost | PASS |
| Numeric validation | Giá trị >= 0 | PASS |

### Test 12: Employee Salaries
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/building-employees/salaries/monthly | Lương nhân viên | PASS |
| Salary fields | employee_id, full_name, role, base_salary, total_salary | PASS |
| total_salary >= base_salary | Validation logic | PASS |

**Dữ liệu xác minh**: 5 nhân viên (Nguyễn Minh, Trần Hương, Lê Bình, Phạm Cường, Hoàng Lan)

### Test 13: Pagination
| Test | Mô tả | Kết quả |
|------|--------|---------|
| ?limit=2 | Giới hạn kết quả | PASS |

### Test 14-15: Error Handling
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/offices/99999 | Invalid ID → 404 | PASS |
| POST invalid data | Validation → 422 | PASS |

### Test 16: Service Details
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/companies/:id/service-details | Chi tiết dịch vụ | PASS |
| Response fields | company_id, monthly_services, daily_services, total_service_cost | PASS |

### Test 17: Building Finance
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/reports/building-finance | Báo cáo tài chính | PASS |
| Response fields | total_revenue, total_expense, net_profit, revenue_breakdown | PASS |
| Calculation | net_profit = total_revenue - total_expense | PASS |

**Dữ liệu xác minh** (tháng 1/2026):
- total_revenue: 30,400,000₫
- revenue_breakdown.rent: 19,760,000₫
- revenue_breakdown.services: 10,640,000₫
- total_expense: 0₫
- net_profit: 30,400,000₫

### Test 18: Building Finance Details
| Test | Mô tả | Kết quả |
|------|--------|---------|
| GET /api/reports/building-finance/details | Chi tiết thu chi | PASS |
| Response fields | revenue_details, expense_details | PASS |

---

## 3. API ENDPOINTS TỔNG HỢP

| # | Method | Endpoint | Mô tả | Status |
|---|--------|----------|--------|--------|
| 1 | GET | /api/offices | Danh sách văn phòng | 200 |
| 2 | GET | /api/offices/:id | Chi tiết văn phòng | 200 |
| 3 | POST | /api/offices | Tạo văn phòng | 201 |
| 4 | PUT | /api/offices/:id | Cập nhật văn phòng | 200 |
| 5 | DELETE | /api/offices/:id | Xóa văn phòng | 200 |
| 6 | GET | /api/companies | Danh sách công ty | 200 |
| 7 | GET | /api/companies/:id | Chi tiết công ty | 200 |
| 8 | POST | /api/companies | Tạo công ty | 201 |
| 9 | PUT | /api/companies/:id | Cập nhật công ty | 200 |
| 10 | DELETE | /api/companies/:id | Xóa công ty | 200 |
| 11 | GET | /api/companies/:id/monthly-costs | Chi phí tháng | 200 |
| 12 | GET | /api/companies/:id/service-details | Chi tiết dịch vụ | 200 |
| 13 | GET | /api/contracts | Danh sách hợp đồng | 200 |
| 14 | GET | /api/building-employees | Danh sách NV | 200 |
| 15 | GET | /api/building-employees/salaries/monthly | Lương NV | 200 |
| 16 | GET | /api/reports/building-finance | Báo cáo tài chính | 200 |
| 17 | GET | /api/reports/building-finance/details | Chi tiết thu chi | 200 |

---

## 4. DATABASE SCHEMA

| Bảng | Số records | Mô tả |
|------|-----------|--------|
| offices | 6 | Văn phòng cho thuê |
| companies | 3 | Công ty thuê |
| company_employees | - | Nhân viên công ty |
| building_employees | 5 | Nhân viên tòa nhà |
| rent_contracts | - | Hợp đồng thuê |
| services | - | Dịch vụ |
| monthly_services | - | DV theo tháng |
| daily_services | - | DV theo ngày |
| invoices | - | Hóa đơn |

---

## 5. FILES CLEANUP

### Đã xóa:
- `back_end/test_api_call.py` - Script test thủ công, trùng chức năng với `auto_test/api/test_api.py`
- `back_end/test_endpoint.py` - Script test thủ công, trùng chức năng

### Giữ nguyên:
- `back_end/auto_test/api/test_api.py` - Test suite chính (98 tests)
- `back_end/auto_test/api/api_utils.py` - Utilities cho test
- `back_end/auto_test/script/` - DB management scripts
- `back_end/auto_test/sql/` - SQL migration scripts

---

## 6. TECH STACK

| Component | Version |
|-----------|---------|
| FastAPI | 0.128.1 |
| asyncpg | 0.29.0 |
| PostgreSQL | 17.7 |
| Pydantic | 2.5.3 |
| Uvicorn | 0.27.0 |
| Python | 3.13 |

---

## 7. KẾT LUẬN

Backend hoạt động hoàn hảo:
- 98/98 tests PASSED (100%)
- Tất cả 17 API endpoints hoạt động đúng
- CRUD operations (Create, Read, Update, Delete) hoạt động đúng
- Business logic (chi phí, lương, báo cáo tài chính) tính toán chính xác
- Error handling (404, 422) hoạt động đúng
- Pagination hoạt động đúng
- SQL thuần 100% qua asyncpg (không ORM)
- CORS middleware cho frontend (localhost:5173, :5174)
